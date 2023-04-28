from ast import Del
import copy
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from web.functions import *
from web.views import setting
from web.models import Image, Participant, Block, Trial, Login, Delete, Flag, Results
from django.core.mail import send_mail
from datetime import datetime
from PIL import Image as imgs
import random
from melipayamak.melipayamak import Api as meliApi

localization = {}
app_lang = ""
gender_types = {"male", "female", "notsay"}

response_namespace = ["nothing", "hit", "false alarm", "miss", "correct rejection"]


class ImageBlock:
    def __init__(self, name, source, types):
        self.name = name
        self.source = source
        self.types = types


# constructor ====


def construction(request):
    global localization
    global app_lang
    if "langcode" in request.session:
        app_lang = str(request.session["langcode"])
    else:
        app_lang = str(settings.APP_LANGUAGE)
    localization = read_generalization_json(settings.BASE_DIR, app_lang)

    if request.method != "POST":
        return returnform(request.session, localization["form_error"])

    add_image_to_database(request)


# respond function ====
def registerform(request):
    if not is_login(request.session):
        return redirect("task")
    construction(request)
    fieldlist = {"csrfmiddlewaretoken", "emailmobile", "age", "gender", "country"}
    if not is_valid_recived_field(request.POST, fieldlist):
        return returnform(request.session, localization["form_error"])

    csrfmiddlewaretoken_input = request.POST["csrfmiddlewaretoken"]
    emailmobile_input = request.POST["emailmobile"]
    age_input = request.POST["age"]
    gender_input = request.POST["gender"]
    country_input = request.POST["country"]

    if csrfmiddlewaretoken_input == "":
        return returnform(request.session, localization["form_error"])

    if not (
        emailmobile_input is not ""
        and len(emailmobile_input) <= 255
        and (is_valid_mobile(emailmobile_input) or is_valid_email(emailmobile_input))
    ):
        return returnform(request.session, localization["emailmobile_error"])

    if age_input is not "":  # age field is optional
        age_input = int(age_input)
        if age_input < settings.LOW_BOUND_AGE or age_input > settings.HIGH_BOUND_AGE:
            return returnform(request.session, localization["age_error"])
    else:
        age_input = 0

    if gender_input is not "":  # gender field is optional
        if gender_input not in gender_types:
            return returnform(request.session, localization["gender_error"])
    else:
        gender_input = "empty"

    if country_input is not "":  # nationality field is optional
        if not is_valid_country_code(settings.BASE_DIR, country_input):
            return returnform(request.session, localization["country_error"])
    else:
        country_input = "empty"

    participant = Participant.objects.filter(pr_username=emailmobile_input)

    if participant.count() != 0:
        return returnform(request.session, localization["duplicate_error"])

    participant = Participant(
        pr_age=age_input,
        pr_gender=gender_input,
        pr_country=country_input,
        pr_lang=app_lang,
        pr_username=emailmobile_input,
        pr_description=request.META["HTTP_USER_AGENT"],
    )
    participant.save()
    participant = Participant.objects.filter(pr_username=emailmobile_input)
    if participant.count() == 0:
        return returnform(request.session, localization["form_error"])

    target = list(Image.objects.exclude(im_cat="fillers"))
    fillers = list(Image.objects.filter(im_cat="fillers"))
    counter = 1

    for i in range(settings.BLOCK_PER_PARTICIPANT):
        block = Block(
            bl_participant=participant[0].id,
            bl_block=i + 1,
            bl_status=0,
            bl_width=0,
            bl_height=0,
            bl_ip=request.META.get("REMOTE_ADDR"),
            bl_description=request.META["HTTP_USER_AGENT"],
        )
        block.save()

        target_per_block = int(settings.TARGET_PER_BLOCK)
        fillers_per_block = int(settings.FILLERS_PER_BLOCK)
        vigilance_per_block = int(settings.VIGILANCE_PER_BLOCK)

        sum_image_per_block = (
            target_per_block * 2 + fillers_per_block + vigilance_per_block * 2
        )

        images_block = list([])

        target_image = random.sample(target, target_per_block)
        for img in target_image:
            target.remove(img)
            new_item = ImageBlock(img.im_name, img.im_source, "target")
            images_block.append(copy.copy(new_item))
            images_block.append(copy.copy(new_item))

        fillers_image = random.sample(fillers, fillers_per_block)
        for img in fillers_image:
            fillers.remove(img)
            new_item = ImageBlock(img.im_name, img.im_source, "fillers")
            images_block.append(copy.copy(new_item))

        vigilance_image = random.sample(fillers, vigilance_per_block)
        for img in vigilance_image:
            fillers.remove(img)
            new_item = ImageBlock(img.im_name, img.im_source, "vigilance")
            images_block.append(copy.copy(new_item))
            images_block.append(copy.copy(new_item))

        final_block = list([])

        for j in range(len(images_block)):
            img = random.choice(images_block)
            for temp_img in final_block:
                if temp_img.name is img.name and temp_img.types is img.types:
                    img.types = img.types + " repeat"
                    break
            images_block.remove(img)
            final_block.append(img)

        for img in final_block:
            trial = Trial(
                tr_index=counter,
                tr_block=i + 1,
                tr_participant=participant[0].id,
                tr_image=img.name,
                tr_source=img.source,
                tr_type=img.types,
                tr_response="nothing",
            )
            trial.save()
            counter += 1

        final_block.clear()

        counter = 1

    request.session["verify"] = 1
    request.session["verify_code"] = generate_verify_code(settings.VERIFY_CODE_LENGTH)
    request.session["user_id"] = participant[0].id

    target = Image.objects.exclude(im_cat="fillers")
    fillers = Image.objects.filter(im_cat="fillers")

    if is_valid_mobile(emailmobile_input):
        request.session["verify_type"] = "mobile"
        send_mobile_verify_code(emailmobile_input, request.session["verify_code"])
    elif is_valid_email(emailmobile_input):
        request.session["verify_type"] = "email"
        send_mail_verify_code(emailmobile_input, request.session["verify_code"])

    return redirect("verify")


def verifyform(request):
    if not is_login(request.session):
        return redirect("task")
    if not (
        "verify" in request.session
        and "verify_code" in request.session
        and "user_id" in request.session
        and request.session["verify"] == 1
    ):
        if "last_url" in request.session:
            if request.session["last_url"] != "":
                return redirect(request.session["last_url"])
        return redirect("login")

    participant = Participant.objects.filter(id=request.session["user_id"])
    if participant.count() == 0:
        if "last_url" in request.session:
            if request.session["last_url"] != "":
                return redirect(request.session["last_url"])
        return redirect("login")

    construction(request)
    fieldlist = {"csrfmiddlewaretoken", "verifycode"}
    if not is_valid_recived_field(request.POST, fieldlist):
        return returnform(request.session, localization["form_error"])

    csrfmiddlewaretoken_input = request.POST["csrfmiddlewaretoken"]
    verifycode_input = request.POST["verifycode"]

    if csrfmiddlewaretoken_input == "":
        return returnform(request.session, localization["form_error"])

    if not (
        verifycode_input is not ""
        and len(verifycode_input) <= settings.VERIFY_CODE_LENGTH
        and verifycode_input.isnumeric()
    ):
        return returnform(request.session, localization["verifycode_error"])

    if request.session["verify_code"] != int(verifycode_input):
        return returnform(request.session, localization["verifycode_error"])

    login = Login(
        lo_participant=request.session["user_id"],
        lo_ip=request.META.get("REMOTE_ADDR"),
        lo_description=request.META["HTTP_USER_AGENT"],
    )
    login.save()

    request.session["login"] = 1
    return redirect("task")


def loginform(request):
    if not is_login(request.session):
        return redirect("task")
    construction(request)
    fieldlist = {"csrfmiddlewaretoken", "emailmobile"}
    if not is_valid_recived_field(request.POST, fieldlist):
        return returnform(request.session, localization["form_error"])

    csrfmiddlewaretoken_input = request.POST["csrfmiddlewaretoken"]
    emailmobile_input = request.POST["emailmobile"]

    if csrfmiddlewaretoken_input == "":
        return returnform(request.session, localization["form_error"])

    if not (
        emailmobile_input is not ""
        and len(emailmobile_input) <= 255
        and (is_valid_mobile(emailmobile_input) or is_valid_email(emailmobile_input))
    ):
        return returnform(request.session, localization["emailmobile_error"])

    participant = Participant.objects.filter(pr_username=emailmobile_input)
    if participant.count() == 0:
        return returnform(request.session, localization["non_register_error"])

    request.session["verify"] = 1
    request.session["verify_code"] = generate_verify_code(settings.VERIFY_CODE_LENGTH)
    request.session["user_id"] = participant[0].id

    if is_valid_mobile(emailmobile_input):
        request.session["verify_type"] = "mobile"
        send_mobile_verify_code(emailmobile_input, request.session["verify_code"])
    elif is_valid_email(emailmobile_input):
        request.session["verify_type"] = "email"
        send_mail_verify_code(emailmobile_input, request.session["verify_code"])

    return redirect("verify")


def settingform(request):
    if is_login(request.session):
        for key in list(request.session.keys()):
            del request.session[key]
        return redirect("login")
    construction(request)
    fieldlist = {"csrfmiddlewaretoken", "age", "gender", "country"}
    if not is_valid_recived_field(request.POST, fieldlist):
        return returnform(request.session, localization["form_error"])

    csrfmiddlewaretoken_input = request.POST["csrfmiddlewaretoken"]
    age_input = request.POST["age"]
    gender_input = request.POST["gender"]
    country_input = request.POST["country"]

    if csrfmiddlewaretoken_input == "":
        return returnform(request.session, localization["form_error"])

    if age_input is not "":  # age field is optional
        age_input = int(age_input)
        if age_input < settings.LOW_BOUND_AGE or age_input > settings.HIGH_BOUND_AGE:
            return returnform(request.session, localization["age_error"])
    else:
        age_input = 0

    if gender_input is not "":  # gender field is optional
        if gender_input not in gender_types:
            return returnform(request.session, localization["gender_error"])
    else:
        gender_input = "empty"

    if country_input is not "":  # nationality field is optional
        if not is_valid_country_code(settings.BASE_DIR, country_input):
            return returnform(request.session, localization["country_error"])
    else:
        country_input = "empty"

    participant = Participant.objects.filter(id=request.session["user_id"])
    if participant.count() == 0:
        return redirect("task")

    participant = Participant.objects.filter(id=request.session["user_id"]).update(
        pr_age=age_input,
        pr_gender=gender_input,
        pr_country=country_input,
        pr_updated=datetime.now(),
    )

    return returnform(request.session, localization["success_error"])


def deleteform(request):
    if is_login(request.session):
        for key in list(request.session.keys()):
            del request.session[key]
        return redirect("login")
    construction(request)
    fieldlist = {"csrfmiddlewaretoken", "reason"}
    if not is_valid_recived_field(request.POST, fieldlist):
        return returnform(request.session, localization["form_error"])

    csrfmiddlewaretoken_input = request.POST["csrfmiddlewaretoken"]
    reason_input = request.POST["reason"]

    if csrfmiddlewaretoken_input == "":
        return returnform(request.session, localization["form_error"])

    if reason_input is not "":  # delete account reason field is optional
        if not (len(reason_input) <= settings.DELETE_ACCOUNT_REASON_MAX_LENGTH):
            return returnform(request.session, localization["reason_error"])

    Participant.objects.filter(id=request.session["user_id"]).delete()
    Login.objects.filter(lo_participant=request.session["user_id"]).delete()
    Block.objects.filter(bl_participant=request.session["user_id"]).delete()
    Trial.objects.filter(tr_participant=request.session["user_id"]).delete()
    Flag.objects.filter(fl_participant=request.session["user_id"]).delete()

    delete = Delete(
        dt_reason=reason_input,
        dt_ip=request.META.get("REMOTE_ADDR"),
        dt_description=request.META["HTTP_USER_AGENT"],
    )
    delete.save()

    for key in list(request.session.keys()):
        del request.session[key]
    request.session["last_url"] = "login"
    return returnform(request.session, localization["delete_account_error"])


def settingform(request):
    if is_login(request.session):
        for key in list(request.session.keys()):
            del request.session[key]
        return redirect("login")
    construction(request)
    fieldlist = {"csrfmiddlewaretoken", "age", "gender", "country"}
    if not is_valid_recived_field(request.POST, fieldlist):
        return returnform(request.session, localization["form_error"])

    csrfmiddlewaretoken_input = request.POST["csrfmiddlewaretoken"]
    age_input = request.POST["age"]
    gender_input = request.POST["gender"]
    country_input = request.POST["country"]

    if csrfmiddlewaretoken_input == "":
        return returnform(request.session, localization["form_error"])

    if age_input is not "":  # age field is optional
        age_input = int(age_input)
        if age_input < settings.LOW_BOUND_AGE or age_input > settings.HIGH_BOUND_AGE:
            return returnform(request.session, localization["age_error"])
    else:
        age_input = 0

    if gender_input is not "":  # gender field is optional
        if gender_input not in gender_types:
            return returnform(request.session, localization["gender_error"])
    else:
        gender_input = "empty"

    if country_input is not "":  # nationality field is optional
        if not is_valid_country_code(settings.BASE_DIR, country_input):
            return returnform(request.session, localization["country_error"])
    else:
        country_input = "empty"

    participant = Participant.objects.filter(id=request.session["user_id"])
    if participant.count() == 0:
        return redirect("task")

    participant = Participant.objects.filter(id=request.session["user_id"]).update(
        pr_age=age_input,
        pr_gender=gender_input,
        pr_country=country_input,
        pr_updated=datetime.now(),
    )

    return returnform(request.session, localization["success_error"])


def startgameform(request):
    if is_login(request.session):
        for key in list(request.session.keys()):
            del request.session[key]
        return redirect("login")
    construction(request)
    fieldlist = {"csrfmiddlewaretoken", "screen_width", "screen_height"}
    if not is_valid_recived_field(request.POST, fieldlist):
        return returnform(request.session, localization["form_error"])

    csrfmiddlewaretoken_input = request.POST["csrfmiddlewaretoken"]
    screen_width_input = request.POST["screen_width"]
    screen_height_input = request.POST["screen_height"]

    flag = Flag.objects.filter(fl_participant=request.session["user_id"])
    if flag.count() >= settings.MAX_FLAG:
        return returnform(request.session, localization["max_flag_error"])

    block = Block.objects.filter(bl_participant=request.session["user_id"], bl_status=1)
    if int(settings.BLOCK_PER_PARTICIPANT) == block.count():
        return returnform(request.session, localization["max_block_error"])

    block = Block.objects.filter(
        bl_participant=request.session["user_id"], bl_block=block.count() + 1
    ).update(
        bl_width=int(screen_width_input),
        bl_height=int(screen_height_input),
        bl_updated=datetime.now(),
    )

    request.session["game"] = 1
    return redirect("game")


def completeform(request, result):
    """if is_login(request.session):
        for key in list(request.session.keys()):
            del request.session[key]
        return redirect("login")
    construction(request)
    if not ("proccess" in request.session and request.session["proccess"] == 1):
        return redirect("task")
    else:
        del request.session["proccess"]"""
    construction(request)

    flag = Flag.objects.filter(fl_participant=request.session["user_id"])
    if flag.count() >= settings.MAX_FLAG:
        return returnform(request.session, localization["max_flag_error"])

    block = Block.objects.filter(bl_participant=request.session["user_id"], bl_status=1)
    if int(settings.BLOCK_PER_PARTICIPANT) == block.count():
        return returnform(request.session, localization["max_block_error"])

    target_per_block = int(settings.TARGET_PER_BLOCK)
    fillers_per_block = int(settings.FILLERS_PER_BLOCK)
    vigilance_per_block = int(settings.VIGILANCE_PER_BLOCK)
    sum_image_per_block = (
        target_per_block * 2 + fillers_per_block + vigilance_per_block * 2
    )

    try:
        results = Results(
            r_block=block.count() + 1,
            r_result=result,
        )
        results.save()
    except:
        pass

    result = result.split(",")

    if len(result) > sum_image_per_block:
        result = result[0:sum_image_per_block]
    elif len(result) < sum_image_per_block:
        return returncontroller(request.session, "/task", localization["form_error"])

    for i in range(len(result)):
        if int(result[i]) > 0 or result[i] < len(response_namespace) - 1:
            result[i] = response_namespace[int(result[i])]
        else:
            result[i] = response_namespace[0]

    for i in range(len(result)):
        trial = Trial.objects.filter(
            tr_participant=request.session["user_id"], tr_block=block.count() + 1
        ).update(
            tr_response=result[i],
            tr_updated=datetime.now(),
        )

    hit_trial = Trial.objects.filter(
        tr_participant=request.session["user_id"],
        tr_type="vigilance repeat",
        tr_response="hit",
        tr_block=block.count() + 1,
    )
    correct_rejection_trial = Trial.objects.filter(
        tr_participant=request.session["user_id"],
        tr_type="vigilance repeat",
        tr_response="correct rejection",
        tr_block=block.count() + 1,
    )
    if (
        vigilance_per_block - (hit_trial.count() + correct_rejection_trial.count())
        >= vigilance_per_block - 1
    ):
        trial = Trial.objects.filter(
            tr_participant=request.session["user_id"], tr_block=block.count() + 1
        ).update(
            tr_response=response_namespace[0],
            tr_updated=datetime.now(),
        )

        flag = Flag(
            fl_participant=request.session["user_id"],
            fl_ip=request.META.get("REMOTE_ADDR"),
            fl_description=request.META["HTTP_USER_AGENT"],
        )
        flag.save()

        return returncontroller(
            request.session, "/task", localization["failed_message"]
        )

    error_count = 0
    for i in range(len(result)):
        if result[i] == 2 or result[i] == 3:
            error_count += 1

        if (
            i > 30
            and error_count - (hit_trial.count() + correct_rejection_trial.count()) > 0
            and error_count > round(sum_image_per_block / 2)
        ):
            trial = Trial.objects.filter(
                tr_participant=request.session["user_id"], tr_block=block.count() + 1
            ).update(
                tr_response=response_namespace[0],
                tr_updated=datetime.now(),
            )

            flag = Flag(
                fl_participant=request.session["user_id"],
                fl_ip=request.META.get("REMOTE_ADDR"),
                fl_description=request.META["HTTP_USER_AGENT"],
            )
            flag.save()

            return returncontroller(
                request.session, "/task", localization["failed_message"]
            )

    block = Block.objects.filter(
        bl_participant=request.session["user_id"], bl_block=block.count() + 1
    ).update(
        bl_status=1,
        bl_updated=datetime.now(),
    )

    return returncontroller(request.session, "/task", localization["success_message"])


# non-respond function ====
def returnform(session, result):
    session["form_result"] = result
    if "last_url" in session:
        if session["last_url"] != "":
            return redirect(session["last_url"])
    return redirect("/notfound")


def returncontroller(session, controller, result):
    session["form_result"] = result
    return redirect(controller)


def csrf_failure(request, reason=""):
    construction(request)
    return returnform(request.session, localization["form_error"])


def is_login(sessions):
    if not ("login" in sessions and "user_id" in sessions and sessions["login"] == 1):
        return True
    participant = Participant.objects.filter(id=sessions["user_id"])
    if participant.count() < 1:
        return True
    return False


def send_mobile_verify_code(mobile, verify_code):
    username = settings.SMS_USERNAME
    password = settings.SMS_PASSWORD
    pattern = settings.SMS_PATTERN
    api = meliApi(username, password)
    sms_soap = api.sms("soap")
    to = mobile
    sms_soap.send_by_base_number(verify_code, to, pattern)
    return True


def send_mail_verify_code(email, verify_code):
    subject = (
        localization["email_subject"]
        + "("
        + str(verify_code)
        + ") - "
        + localization["site_title"]
    )
    message = localization["email_text"] + str(verify_code)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True


def add_image_to_database(request):
    image = Image.objects.filter()
    if image.count() > 0:
        return False

    target_path = str(settings.BASE_DIR) + str(settings.STATIC_URL) + "dataset/target"
    fillers_path = str(settings.BASE_DIR) + str(settings.STATIC_URL) + "dataset/fillers"

    category = os.listdir(target_path)
    for cat in category:
        cat_images = os.listdir(target_path + "/" + str(cat))
        for cat_image in cat_images:
            image_path = target_path + "/" + str(cat) + "/" + str(cat_image)
            img = imgs.open(image_path)
            image = Image(
                im_name=str(cat_image),
                im_cat=str(cat),
                im_width=int(img.width),
                im_height=int(img.height),
                im_source=str(image_path),
            )
            image.save()

    fillers_images = os.listdir(fillers_path)
    for fillers_image in fillers_images:
        image_path = fillers_path + "/" + str(fillers_image)
        img = imgs.open(image_path)
        image = Image(
            im_name=str(fillers_image),
            im_cat=str("fillers"),
            im_width=int(img.width),
            im_height=int(img.height),
            im_source=str(image_path),
        )
        image.save()

    return True
