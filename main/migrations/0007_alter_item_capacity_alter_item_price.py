# Generated by Django 4.1.7 on 2023-04-08 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0006_item_seller"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="capacity",
            field=models.BigIntegerField(default=0, verbose_name="容量"),
        ),
        migrations.AlterField(
            model_name="item",
            name="price",
            field=models.BigIntegerField(verbose_name="価格"),
        ),
    ]
