# Generated by Django 3.2.9 on 2021-12-04 02:51

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ("email_signals", "0003_auto_20211204_0211"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signal",
            name="html_email",
            field=tinymce.models.HTMLField(
                blank=True, null=True, verbose_name="HTML email"
            ),
        ),
    ]
