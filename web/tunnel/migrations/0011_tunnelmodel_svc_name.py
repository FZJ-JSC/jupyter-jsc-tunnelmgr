# Generated by Django 3.2.12 on 2022-04-04 09:08
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("tunnel", "0010_rename_startuuidcode_tunnelmodel_servername"),
    ]

    operations = [
        migrations.AddField(
            model_name="tunnelmodel",
            name="svc_name",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
    ]
