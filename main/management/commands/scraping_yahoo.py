import io
import time
from main.models import Item
from PIL import Image
from io import BytesIO
import requests
from django.core.management.base import BaseCommand
from main.management.commands.ProductClass import Product
from django.conf import settings
import logging
from django.core.files.base import ContentFile

SEARCH_WORDS = ["マグカップ", "グラス", "コップ"]
SEARCH_PAGES = 5
YAHOO_ID = settings.YAHOO_ID
AFFILIATE_ID = settings.AFFILIATE_ID_YAHOO
URL_YAHOO_API = "https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch"


class YahooProduct(Product):

    def resize_image(self, content):
        pilImage = Image.open(BytesIO(content))
        resize_image = pilImage.resize((400, 400), Image.ANTIALIAS)
        byte_image = io.BytesIO()
        resize_image.save(byte_image, "JPEG")
        return byte_image.getvalue()

    def check_none_data(self):
        ''' yahooの場合、値がNoneになる商品がいくつかあるので、validationを実施'''
        check_data = [self.itemName, self.itemPrice, self.itemCaption, self.affiliateUrl, self.itemCode,
                      self.imageUrlRow, self.seller]
        # 取得した情報でvalidation
        for data in check_data:
            if not data:
                return True

        # capacityがNoneなどになっていないかvalidation
        for data in self.dictInfo.values():
            if not data:
                return True


def fetchYahooData(keywords: list, pages: int):
    logger = logging.Logger("django")
    for keyword in keywords:
        for i in range(pages):
            # API制限にかからないよう1眇以上リクエストを待つ
            time.sleep(1.5)

            params = {
                "appid": YAHOO_ID,
                "query": keyword,
                "affiliate_id": AFFILIATE_ID,
                "affiliate_type": "vc",
                "start": int(1 + 100 * i),  # 返却結果の先頭
                "results": 100,
                "sort": "-score",
                "in_stock": "true",
                "image_size": 600,
            }

            response = requests.get(URL_YAHOO_API, params=params)

            if response.status_code != 200:
                logger.error(f"{params['start']}から{params['results']}件の取得を失敗しました。")
                continue

            json_data = response.json()
            for product in json_data["hits"]:
                yahoo_product = YahooProduct(itemName=product["name"], itemPrice=product["price"],
                                             itemCaption=product["description"], affiliateUrl=product["url"],
                                             itemCode=product["code"], imageUrlRow=product["exImage"]["url"],
                                             seller="yahoo")

                if yahoo_product.check_none_data():
                    continue

                image_response = requests.get(yahoo_product.imageUrlRow)
                if image_response.status_code != 200:
                    logger.error(f"{yahoo_product.imageUrlRow}から画像のダウンロードに失敗しました。")
                    continue
                image = ContentFile(yahoo_product.resize_image(image_response.content))

                model_item, created = Item.objects.update_or_create(item_code=yahoo_product.itemCode,
                                                                    defaults=yahoo_product.dictInfo)
                if not created:
                    # 既に作成済みであれば既存の画像を削除する
                    model_item.image.delete()
                model_item.image.save(f'{yahoo_product.itemCode}.jpg', image, save=True)


class Command(BaseCommand):

    def handle(self, *args, **options):
        fetchYahooData(SEARCH_WORDS, SEARCH_PAGES)
