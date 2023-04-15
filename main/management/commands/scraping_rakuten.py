from django.core.management.base import BaseCommand
from urllib.parse import urlparse
from main.models import Item
from django.conf import settings
from django.core.files.base import ContentFile
import requests
import json
import time
from main.management.commands.ProductClass import Product
import logging

REQ_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
PATTERN = "[0-9]+\.?[0-9]*ml|[0-9]+\.?[0-9]*cc|[0-9]+\.?[0-9]*l"
SEARCH_WORDS = ["マグカップ", "グラス", "コップ"]
SEARCH_PAGES = 30
IMAGE_RESIZE = "_ex=400x400"
RAKUTEN_ID = settings.RAKUTEN_ID
AFFILIATE_ID = settings.AFFILIATE_ID


class RakutenItem(Product):

    @property
    def imageUrl(self):
        ''' 取得する画像がデフォルトだと小さいため、URLのサイズクエリを書き換えする'''
        imageUrls = json.loads(self.imageUrlRow)
        return urlparse(imageUrls[0]["imageUrl"])._replace(query=IMAGE_RESIZE).geturl()


def fetchRakutenData(keywords: list, pages: int):
    logger = logging.Logger("django")
    for keyword in keywords:
        # 商品順位を設定するための変数を用意
        rank = 1
        for i in range(pages):
            # API制限にかからないよう1眇以上リクエストを待つ
            time.sleep(1.5)

            parameter = {"format": "json", "keyword": keyword, "applicationId": RAKUTEN_ID, "page": str(i + 1),
                         "affiliateId": AFFILIATE_ID}
            request = requests.get(REQ_URL, parameter)

            if request.status_code != 200:
                logger.error(f"rakuten:{parameter['page']}の取得に失敗しました。error内容{request.content}")
                continue

            json_data = request.json()
            for item in json_data["Items"]:
                info = item["Item"]
                rakutenItem = RakutenItem(itemName=info["itemName"], itemPrice=info["itemPrice"],
                                          itemCaption=info["itemCaption"], affiliateUrl=info["affiliateUrl"],
                                          itemCode=info["itemCode"],
                                          imageUrlRow=json.dumps(info["mediumImageUrls"], ensure_ascii=False),
                                          seller="rakuten", rank=rank)
                if rakutenItem.capacity is None:
                    # 容量を取得できない場合は、データベースへ登録しない
                    continue

                image_request = requests.get(rakutenItem.imageUrl)
                if image_request.status_code != 200:
                    logger.error(f"{rakutenItem.imageUrl}から画像のダウンロードに失敗しました。")
                    continue
                image = ContentFile(image_request.content)

                model_item, created = Item.objects.update_or_create(item_code=rakutenItem.itemCode,
                                                                    defaults=rakutenItem.dictInfo)
                if not created:
                    # 既に作成済みであれば既存の画像を削除する
                    model_item.image.delete()
                model_item.image.save(f'{rakutenItem.itemPrice}.jpg', image, save=True)
                # 順位を + 1
                rank += 1


class Command(BaseCommand):
    def handle(self, *args, **options):
        fetchRakutenData(SEARCH_WORDS, SEARCH_PAGES)
