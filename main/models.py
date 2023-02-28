from django.db import models


# Create your models here.
class Item(models.Model):
    name = models.CharField(verbose_name="商品名", max_length=500)
    price = models.IntegerField(verbose_name="価格")
    caption = models.TextField(verbose_name="商品紹介", max_length=1000)
    item_url = models.CharField(verbose_name="商品URL", max_length=500)
    hash = models.CharField(verbose_name="ハッシュ値", max_length=500)
    image = models.ImageField(verbose_name="商品画像", upload_to="item_images/")

    def __str__(self):
        return self.hash

    class Meta:
        db_table = "items"
        verbose_name = verbose_name_plural = "商品"
