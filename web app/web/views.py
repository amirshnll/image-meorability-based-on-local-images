import random
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from web.functions import *
from django.shortcuts import render
from web.models import Image, Participant, Block, Trial, Login, Delete, Flag, Results
from datetime import datetime
from PIL import Image as imgs
import os
from django.core.mail import send_mail
from melipayamak.melipayamak import Api as meliApi

localization = {}
app_lang = ""


class ImageBlock:
    def __init__(self, name, source, types):
        self.name = name
        self.source = source
        self.types = types


class ImageGame:
    def __init__(self, id, source, hit, vigilance):
        self.id = id
        self.source = source
        self.hit = hit
        self.vigilance = vigilance


# constructor ====


def construction(request):
    request.session["last_url"] = request.resolver_match.url_name

    global localization
    global app_lang
    if "langcode" in request.session:
        app_lang = str(request.session["langcode"])
    else:
        app_lang = str(settings.APP_LANGUAGE)
    localization = read_generalization_json(settings.BASE_DIR, app_lang)

    add_image_to_database(request)


# view ====
def home(request):
    if not is_login(request.session):
        return redirect("task")
    global app_lang
    construction(request)

    # render
    context = {
        "lang": app_lang,
        "static": settings.STATIC_URL,
        "available_language": settings.AVAILABLE_LANGUAGE,
        "page_title": localization["home_title"],
        "layout": "layout-" + localization["site_direction"] + ".css",
        "check_js": 1,
        "game_page": 0,
    }
    context.update(localization)
    return render(request, localization["site_direction"] + "/home.html", context)


def register(request):
    if not is_login(request.session):
        return redirect("task")
    global app_lang
    construction(request)
    country_list = read_country(settings.BASE_DIR, app_lang)

    # form result
    if "form_result" in request.session:
        form_result = str(request.session["form_result"])
        del request.session["form_result"]
    else:
        form_result = ""

    # render
    context = {
        "lang": app_lang,
        "static": settings.STATIC_URL,
        "available_language": settings.AVAILABLE_LANGUAGE,
        "country_list": country_list["country"],
        "page_title": localization["register_title"],
        "layout": "layout-" + localization["site_direction"] + ".css",
        "form_result": form_result,
        "success": localization["success"],
        "email_mobile_len": settings.EMAIL_MOBILE_MAX_LENGTH,
        "check_js": 1,
        "game_page": 0,
    }
    context.update(localization)
    return render(request, localization["site_direction"] + "/register.html", context)


def verify(request):
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

    global app_lang
    construction(request)

    if request.session["verify_type"] == "email":
        verify_code_messages = localization["email_verify_spam"]
    else:
        verify_code_messages = localization["verify_code_message"]

    # form result
    if "form_result" in request.session:
        form_result = str(request.session["form_result"])
        del request.session["form_result"]
    else:
        form_result = ""

    # render
    context = {
        "lang": app_lang,
        "static": settings.STATIC_URL,
        "available_language": settings.AVAILABLE_LANGUAGE,
        "page_title": localization["verify_title"],
        "layout": "layout-" + localization["site_direction"] + ".css",
        "form_result": form_result,
        "success": localization["success"],
        "verify_len": settings.VERIFY_CODE_LENGTH,
        "verify_code_number": request.session["verify_code"],
        "check_js": 1,
        "game_page": 0,
        "verify_code_messages": verify_code_messages,
    }
    context.update(localization)
    return render(request, localization["site_direction"] + "/verify.html", context)


def login(request):
    if not is_login(request.session):
        return redirect("task")
    global app_lang
    construction(request)

    # form result
    if "form_result" in request.session:
        form_result = str(request.session["form_result"])
        del request.session["form_result"]
    else:
        form_result = ""

    # render
    context = {
        "lang": app_lang,
        "static": settings.STATIC_URL,
        "available_language": settings.AVAILABLE_LANGUAGE,
        "page_title": localization["login_title"],
        "layout": "layout-" + localization["site_direction"] + ".css",
        "form_result": form_result,
        "success": localization["success"],
        "email_mobile_len": settings.EMAIL_MOBILE_MAX_LENGTH,
        "check_js": 1,
        "game_page": 0,
    }
    context.update(localization)
    return render(request, localization["site_direction"] + "/login.html", context)


def setting(request):
    if is_login(request.session):
        for key in list(request.session.keys()):
            del request.session[key]
        return redirect("login")
    global app_lang
    construction(request)
    country_list = read_country(settings.BASE_DIR, app_lang)

    participant = Participant.objects.filter(id=request.session["user_id"])
    if participant.count() == 0:
        return redirect("task")

    # form result
    if "form_result" in request.session:
        form_result = str(request.session["form_result"])
        del request.session["form_result"]
    else:
        form_result = ""

    # render
    context = {
        "lang": app_lang,
        "static": settings.STATIC_URL,
        "available_language": settings.AVAILABLE_LANGUAGE,
        "country_list": country_list["country"],
        "page_title": localization["setting_title"],
        "layout": "layout-" + localization["site_direction"] + ".css",
        "form_result": form_result,
        "success": localization["success"],
        "age_value": int(participant[0].pr_age),
        "gender_value": participant[0].pr_gender,
        "country_value": participant[0].pr_country,
        "check_js": 1,
        "game_page": 0,
    }
    context.update(localization)
    return render(request, localization["site_direction"] + "/setting.html", context)


def delete(request):
    if is_login(request.session):
        for key in list(request.session.keys()):
            del request.session[key]
        return redirect("login")
    global app_lang
    construction(request)
    country_list = read_country(settings.BASE_DIR, app_lang)

    # form result
    if "form_result" in request.session:
        form_result = str(request.session["form_result"])
        del request.session["form_result"]
    else:
        form_result = ""

    # render
    context = {
        "lang": app_lang,
        "static": settings.STATIC_URL,
        "available_language": settings.AVAILABLE_LANGUAGE,
        "country_list": country_list["country"],
        "page_title": localization["delete_title"],
        "layout": "layout-" + localization["site_direction"] + ".css",
        "form_result": form_result,
        "success": localization["success"],
        "reason_len": settings.DELETE_ACCOUNT_REASON_MAX_LENGTH,
        "check_js": 1,
        "game_page": 0,
    }
    context.update(localization)
    return render(request, localization["site_direction"] + "/delete.html", context)


def task(request):
    if is_login(request.session):
        for key in list(request.session.keys()):
            del request.session[key]
        return redirect("login")
    global app_lang
    construction(request)

    # form result
    if "form_result" in request.session:
        form_result = str(request.session["form_result"])
        del request.session["form_result"]
    else:
        form_result = ""

    block = Block.objects.filter(bl_participant=request.session["user_id"], bl_status=1)

    level_list = []
    for i in range(int(settings.BLOCK_PER_PARTICIPANT)):
        level_list.append(i + 1)

    if int(settings.BLOCK_PER_PARTICIPANT) == block.count():
        task_end = 1
    else:
        task_end = 0

    participant = Participant.objects.filter(id=request.session["user_id"])

    user_age = int(participant[0].pr_age)
    if participant[0].pr_age == 0:
        user_age = localization["empty"]

    user_country = participant[0].pr_country
    if user_country == "empty":
        user_country = localization["empty"]
    else:
        user_country = code_to_country(settings.BASE_DIR, user_country, app_lang)

    user_gender = participant[0].pr_gender
    if user_gender == "empty":
        user_gender = localization["empty"]
    else:
        if user_gender == "male":
            user_gender = localization["male"]
        elif user_gender == "female":
            user_gender = localization["female"]
        elif user_gender == "notsay":
            user_gender = localization["notsay"]

    flag = Flag.objects.filter(fl_participant=request.session["user_id"])

    target_per_block = int(settings.TARGET_PER_BLOCK)
    fillers_per_block = int(settings.FILLERS_PER_BLOCK)
    vigilance_per_block = int(settings.VIGILANCE_PER_BLOCK)

    sum_image_per_block = (
        target_per_block * 2 + fillers_per_block + vigilance_per_block * 2
    )

    hit_trial = Trial.objects.filter(
        tr_participant=request.session["user_id"], tr_response="hit"
    )
    false_alarm_trial = Trial.objects.filter(
        tr_participant=request.session["user_id"], tr_response="false alarm"
    )
    miss_trial = Trial.objects.filter(
        tr_participant=request.session["user_id"], tr_response="fmiss"
    )

    # render
    context = {
        "lang": app_lang,
        "static": settings.STATIC_URL,
        "available_language": settings.AVAILABLE_LANGUAGE,
        "page_title": localization["task_title"],
        "test_completed": block.count(),
        "image_shown": block.count() * sum_image_per_block,
        "hit_count": hit_trial.count(),
        "far_count": false_alarm_trial.count() + miss_trial.count(),
        "flag_count": flag.count(),
        "user_gender": user_gender,
        "user_age": user_age,
        "user_country": user_country,
        "layout": "layout-" + localization["site_direction"] + ".css",
        "form_result": form_result,
        "success": localization["success"],
        "check_js": 1,
        "taskscript": "task.js",
        "level_list": level_list,
        "task_end": task_end,
        "level_participant": block.count(),
        "flag_max": settings.MAX_FLAG,
        "game_page": 0,
    }
    context.update(localization)
    return render(request, localization["site_direction"] + "/task.html", context)


def game(request):
    if is_login(request.session):
        for key in list(request.session.keys()):
            del request.session[key]
        return redirect("login")
    if not ("game" in request.session and request.session["game"] == 1):
        return redirect("task")
    else:
        request.session["game"] = 2

    request.session["proccess"] = 1

    global app_lang
    construction(request)

    block = Block.objects.filter(bl_participant=request.session["user_id"], bl_status=1)
    trial = Trial.objects.filter(
        tr_participant=request.session["user_id"], tr_block=int(block.count()) + 1
    )
    image_trial = list()

    for i in range(trial.count()):
        new_item = ImageGame(i + 1, trial[i].tr_source, 0, 0)
        if (
            trial[i].tr_type == "target repeat"
            or trial[i].tr_type == "vigilance repeat"
        ):
            new_item.hit = 1
        if trial[i].tr_type == "vigilance repeat":
            new_item.vigilance = 1
        image_trial.append(new_item)

    # render
    context = {
        "lang": app_lang,
        "page_title": localization["game_title"],
        "layout": "layout-" + localization["site_direction"] + ".css",
        "gamescript": "game.js",
        "check_js": 1,
        "images": image_trial,
        "images_count": len(image_trial),
        "vigilance_count": settings.VIGILANCE_PER_BLOCK,
        "game_page": 1,
        "show_time": int(settings.SHOW_TIME),
        "rest_time": int(settings.REST_TIME),
        "loading_data": localization["loading_data"],
    }
    context.update(localization)
    return render(request, localization["site_direction"] + "/game.html", context)


def notfound(request):
    global app_lang
    construction(request)

    # render
    context = {
        "lang": app_lang,
        "page_title": localization["notfound_title"],
        "layout": "layout-" + localization["site_direction"] + ".css",
        "check_js": 1,
        "available_language": settings.AVAILABLE_LANGUAGE,
        "static": settings.STATIC_URL,
        "game_page": 0,
    }
    context.update(localization)
    return render(request, localization["site_direction"] + "/notfound.html", context)


def javascript(request):
    global app_lang
    construction(request)

    # render
    context = {
        "lang": app_lang,
        "page_title": localization["javascript_title"],
        "layout": "layout-" + localization["site_direction"] + ".css",
        "check_js": 0,
        "available_language": settings.AVAILABLE_LANGUAGE,
        "static": settings.STATIC_URL,
        "game_page": 0,
    }
    context.update(localization)
    return render(request, localization["site_direction"] + "/javascript.html", context)


# not view ====
def returncontroller(session, controller, result):
    session["form_result"] = result
    return redirect(controller)


def change_language(request, langcode):
    request.session["langcode"] = langcode

    if "last_url" in request.session:
        if request.session["last_url"] != "":
            return redirect(request.session["last_url"])
    return redirect("home")


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


def robots(request):
    robots_file = read_robots(settings.BASE_DIR)
    context = robots_file
    return HttpResponse(context, content_type="text/plain")


def logout(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return redirect("home")


def is_login(sessions):
    if not ("login" in sessions and "user_id" in sessions and sessions["login"] == 1):
        return True
    participant = Participant.objects.filter(id=sessions["user_id"])
    if participant.count() < 1:
        return True
    return False


def add_image_to_database(request):
    image = Image.objects.filter()
    if image.count() > 0:
        return redirect("home")

    target_path = str(settings.BASE_DIR) + str(settings.STATIC_URL) + "dataset/target"
    fillers_path = str(settings.BASE_DIR) + str(settings.STATIC_URL) + "dataset/fillers"

    category = os.listdir(target_path)
    for cat in category:
        cat_images = os.listdir(target_path + "/" + str(cat))
        for cat_image in cat_images:
            image_path = target_path + "/" + str(cat) + "/" + str(cat_image)
            image_source = (
                str(settings.STATIC_URL)
                + "dataset/target/"
                + str(cat)
                + "/"
                + str(cat_image)
            )
            img = imgs.open(image_path)
            image = Image(
                im_name=str(cat_image),
                im_cat=str(cat),
                im_width=int(img.width),
                im_height=int(img.height),
                im_source=str(image_source),
            )
            image.save()

    fillers_images = os.listdir(fillers_path)
    for fillers_image in fillers_images:
        image_path = fillers_path + "/" + str(fillers_image)
        image_source = (
            str(settings.STATIC_URL) + "dataset/fillers/" + str(fillers_image)
        )
        img = imgs.open(image_path)
        image = Image(
            im_name=str(fillers_image),
            im_cat=str("fillers"),
            im_width=int(img.width),
            im_height=int(img.height),
            im_source=str(image_source),
        )
        image.save()

    return redirect("home")


def getflag(request, result):
    if "game" in request.session:
        del request.session["game"]
    else:
        return redirect("home")
    if is_login(request.session):
        for key in list(request.session.keys()):
            del request.session[key]
        return redirect("login")
    global app_lang
    construction(request)

    flag = Flag.objects.filter(fl_participant=request.session["user_id"])
    if flag.count() >= settings.MAX_FLAG:
        return returncontroller(
            request.session, "/task", localization["failed_message"]
        )

    block = Block.objects.filter(bl_participant=request.session["user_id"], bl_status=1)

    if int(settings.BLOCK_PER_PARTICIPANT) == block.count():
        return returncontroller(
            request.session, "/task", localization["failed_message"]
        )

    try:
        results = Results(
            r_block=block.count() + 1,
            r_result=result,
        )
        results.save()

        block = Block.objects.filter(
            bl_participant=request.session["user_id"], bl_block=block.count() + 1
        ).update(
            bl_status=1,
            bl_updated=datetime.now(),
        )
    except:
        pass

    flag = Flag(
        fl_participant=request.session["user_id"],
        fl_ip=request.META.get("REMOTE_ADDR"),
        fl_description=request.META["HTTP_USER_AGENT"],
    )
    flag.save()
    return returncontroller(request.session, "/task", localization["failed_message"])
