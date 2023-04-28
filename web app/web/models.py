from django.db import models
from django.conf import settings


class Participant(models.Model):
    id = models.BigAutoField(primary_key=True)
    pr_age = models.FloatField()
    pr_gender = models.CharField(max_length=20)  # male, female, not to say
    pr_lang = models.CharField(max_length=2)
    pr_country = models.CharField(max_length=5)
    pr_username = models.CharField(
        max_length=settings.EMAIL_MOBILE_MAX_LENGTH, unique=True
    )
    pr_created = models.DateTimeField(auto_now_add=True)
    pr_updated = models.DateTimeField(auto_now=True)
    pr_description = models.TextField(null=True, blank=True)


class Login(models.Model):
    id = models.BigAutoField(primary_key=True)
    lo_participant = models.IntegerField()
    lo_ip = models.CharField(max_length=50)
    lo_created = models.DateTimeField(auto_now_add=True)
    lo_updated = models.DateTimeField(auto_now=True)
    lo_description = models.TextField(null=True, blank=True)


class Delete(models.Model):
    id = models.BigAutoField(primary_key=True)
    dt_reason = models.TextField(max_length=settings.DELETE_ACCOUNT_REASON_MAX_LENGTH)
    dt_ip = models.CharField(max_length=50)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)
    dt_description = models.TextField(null=True, blank=True)


class Block(models.Model):  # 8
    id = models.BigAutoField(primary_key=True)
    bl_participant = models.IntegerField()
    bl_block = models.IntegerField()
    bl_width = models.FloatField()
    bl_height = models.FloatField()
    bl_created = models.DateTimeField(auto_now_add=True)
    bl_updated = models.DateTimeField(auto_now=True)
    bl_status = models.BooleanField()
    bl_ip = models.CharField(max_length=50)
    bl_description = models.TextField(null=True, blank=True)


class Image(models.Model):
    id = models.BigAutoField(primary_key=True)
    im_name = models.CharField(max_length=255)
    im_cat = models.CharField(max_length=100)
    im_width = models.IntegerField()
    im_height = models.IntegerField()
    im_source = models.TextField()
    im_created = models.DateTimeField(auto_now_add=True)
    im_updated = models.DateTimeField(auto_now=True)


class Trial(models.Model):
    id = models.BigAutoField(primary_key=True)
    tr_index = models.BigIntegerField()
    tr_block = models.BigIntegerField()
    tr_participant = models.IntegerField()
    tr_image = models.CharField(max_length=255)
    tr_source = models.TextField()
    tr_type = models.CharField(
        max_length=20
    )  # target, target repeat, filler, vigilance, vigilance repeat
    tr_response = models.CharField(
        max_length=20
    )  # nothing, hit:1, false alarm: 2, miss: 3, correct rejection: 4
    tr_created = models.DateTimeField(auto_now_add=True)
    tr_updated = models.DateTimeField(auto_now=True)


class Flag(models.Model):
    id = models.BigAutoField(primary_key=True)
    fl_participant = models.IntegerField()
    fl_created = models.DateTimeField(auto_now_add=True)
    fl_updated = models.DateTimeField(auto_now=True)
    fl_ip = models.CharField(max_length=50)
    fl_description = models.TextField(null=True, blank=True)


class Results(models.Model):
    id = models.BigAutoField(primary_key=True)
    r_block = models.BigIntegerField()
    r_result = models.TextField(null=True, blank=True)
