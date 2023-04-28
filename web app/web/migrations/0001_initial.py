# Generated by Django 4.0.4 on 2022-07-18 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('bl_participant', models.IntegerField()),
                ('bl_block', models.IntegerField()),
                ('bl_width', models.FloatField()),
                ('bl_height', models.FloatField()),
                ('bl_created', models.DateTimeField(auto_now_add=True)),
                ('bl_updated', models.DateTimeField(auto_now=True)),
                ('bl_status', models.BooleanField()),
                ('bl_ip', models.CharField(max_length=50)),
                ('bl_description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Delete',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('dt_reason', models.TextField(max_length=5000)),
                ('dt_ip', models.CharField(max_length=50)),
                ('dt_created', models.DateTimeField(auto_now_add=True)),
                ('dt_updated', models.DateTimeField(auto_now=True)),
                ('dt_description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('fl_participant', models.IntegerField()),
                ('fl_created', models.DateTimeField(auto_now_add=True)),
                ('fl_updated', models.DateTimeField(auto_now=True)),
                ('fl_ip', models.CharField(max_length=50)),
                ('fl_description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('im_name', models.CharField(max_length=255)),
                ('im_cat', models.CharField(max_length=100)),
                ('im_width', models.IntegerField()),
                ('im_height', models.IntegerField()),
                ('im_source', models.TextField()),
                ('im_created', models.DateTimeField(auto_now_add=True)),
                ('im_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('lo_participant', models.IntegerField()),
                ('lo_ip', models.CharField(max_length=50)),
                ('lo_created', models.DateTimeField(auto_now_add=True)),
                ('lo_updated', models.DateTimeField(auto_now=True)),
                ('lo_description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('pr_age', models.FloatField()),
                ('pr_gender', models.CharField(max_length=20)),
                ('pr_lang', models.CharField(max_length=2)),
                ('pr_country', models.CharField(max_length=5)),
                ('pr_username', models.CharField(max_length=255, unique=True)),
                ('pr_created', models.DateTimeField(auto_now_add=True)),
                ('pr_updated', models.DateTimeField(auto_now=True)),
                ('pr_description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('r_block', models.BigIntegerField()),
                ('r_result', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trial',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('tr_index', models.BigIntegerField()),
                ('tr_block', models.BigIntegerField()),
                ('tr_participant', models.IntegerField()),
                ('tr_image', models.CharField(max_length=255)),
                ('tr_source', models.TextField()),
                ('tr_type', models.CharField(max_length=20)),
                ('tr_response', models.CharField(max_length=20)),
                ('tr_created', models.DateTimeField(auto_now_add=True)),
                ('tr_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]