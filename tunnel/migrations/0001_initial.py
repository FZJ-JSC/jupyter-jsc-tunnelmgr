# Generated by Django 3.2.10 on 2021-12-16 14:27
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TunnelModel",
            fields=[
                ("backend_id", models.IntegerField(primary_key=True, serialize=False)),
                ("hostname", models.TextField(max_length=32)),
                ("local_port", models.IntegerField()),
                ("target_node", models.TextField(max_length=32)),
                ("target_port", models.IntegerField()),
                ("date", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
