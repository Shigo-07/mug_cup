# Generated by Django 4.1.7 on 2023-03-04 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_remove_item_hash_item_item_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="capacity",
            field=models.ImageField(default=0, upload_to="", verbose_name="容量"),
        ),
    ]
