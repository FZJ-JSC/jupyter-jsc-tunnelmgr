# Generated by Django 4.1.6 on 2023-02-10 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tunnel", "0011_tunnelmodel_svc_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="tunnelmodel",
            name="tunnel_pod",
            field=models.TextField(default="drf-tunnel-0"),
        ),
    ]
