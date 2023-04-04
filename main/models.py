from django.db import models
from django.core.exceptions import ValidationError


def validate_value(value):
    if value not in ['rakuten', 'yahoo']:
        raise ValidationError(f"{value} is not a valid value.")


# Create your models here.
class Item(models.Model):
    name = models.CharField(verbose_name="商品名", max_length=500)
    price = models.IntegerField(verbose_name="価格")
    caption = models.TextField(verbose_name="商品紹介", max_length=1000)
    item_url = models.CharField(verbose_name="商品URL", max_length=500)
    item_code = models.CharField(verbose_name="アイテムコード", max_length=500)
    image_url = models.CharField(verbose_name="画像URL", max_length=500)
    image = models.ImageField(verbose_name="商品画像", upload_to="item_images/")
    capacity = models.IntegerField(verbose_name="容量", default=0)
    seller = models.CharField(verbose_name="販売サイト", max_length=100, validators=[validate_value])

    def __str__(self):
        return self.name

    class Meta:
        db_table = "items"
        verbose_name = verbose_name_plural = "商品"
