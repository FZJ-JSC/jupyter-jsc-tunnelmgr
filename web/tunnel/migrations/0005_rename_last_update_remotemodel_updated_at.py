# Generated by Django 3.2.10 on 2021-12-22 11:10
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tunnel", "0004_alter_tunnelmodel_date"),
    ]

    operations = [
        migrations.RenameField(
            model_name="remotemodel",
            old_name="last_update",
            new_name="updated_at",
        ),
    ]
