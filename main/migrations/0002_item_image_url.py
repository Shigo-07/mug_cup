# Generated by Django 4.1.7 on 2023-03-01 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="image_url",
            field=models.CharField(default=1, max_length=500, verbose_name="画像URL"),
            preserve_default=False,
        ),
    ]
