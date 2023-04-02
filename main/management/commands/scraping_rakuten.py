from django.core.management.base import BaseCommand
from urllib.parse import urlparse
from main.models import Item
from django.conf import settings
# from main.models import Item
from django.core.files.images import ImageFile
from django.core.files.base import ContentFile
import unicodedata
import re
import requests
import json
import time
from dataclasses import dataclass

REQ_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
PATTERN = "[0-9]+\.?[0-9]*ml|[0-9]+\.?[0-9]*cc|[0-9]+\.?[0-9]*l"
SEARCH_WORDS = ["マグカップ", "グラス", "コップ"]
SEARCH_PAGES = 1
IMAGE_RESIZE = "_ex=400x400"
RAKUTEN_ID = settings.RAKUTEN_ID
AFFILIATE_ID = settings.AFFILIATE_ID


@dataclass
class RakutenItem:
    itemName: str
    itemPrice: int
    itemCaption: str
    affiliateUrl: str
    itemCode: str
    imageUrlRow: str

    @property
    def capacity(self):
        '''nameもしくはcaptionから容量を算出する'''
        # 半角かつ小文字へ変換する
        words = unicodedata.normalize('NFKC', self.itemName).lower()
        # タイトルから容量を取得する
        capacity = self._wordsToCapacity(words)

        if not capacity:  # タイトルで取得できない場合は説明欄から取得
            words = unicodedata.normalize('NFKC', self.itemCaption).lower()
            capacity = self._wordsToCapacity(words)
            if not capacity:  # 容量情報がない場合はモデルへ登録できないため、登録できないデータとしてNoneを返す
                return None

        return capacity

    @property
    def imageUrl(self):
        imageUrls = json.loads(self.imageUrlRow)
        return urlparse(imageUrls[0]["imageUrl"])._replace(query=IMAGE_RESIZE).geturl()

    @property
    def dictInfo(self):
        return {
            "name": self.itemName,
            "price": self.itemPrice,
            "caption": self.itemCaption,
            "item_url": self.affiliateUrl,
            "item_code": self.itemCode,
            "image_url": self.imageUrlRow,
            "capacity": self.capacity,
        }

    def _wordsToCapacity(self, words: str):
        # 半角かつ小文字へ変換
        words = unicodedata.normalize('NFKC', words).lower()
        list_capacity = re.findall(PATTERN, words)
        list_number = []
        for capacity in list_capacity:
            if "ml" in capacity or "cc" in capacity:
                number = float(re.search("[0-9]+\.?[0-9]*", capacity).group(0))
                list_number.append(int(number))
            elif "l" in capacity:
                number = float(re.search("[0-9]+\.?[0-9]*", capacity).group(0)) * 1000

                list_number.append(int(number))
        if len(set(list_number)) == 1:
            return list_number[0]
        else:
            return None


def fetchRakutenData(keywords: list, pages: int):
    for keyword in keywords:
        for i in range(pages):
            # API制限にかからないよう1眇以上リクエストを待つ
            time.sleep(1.5)

            parameter = {"format": "json", "keyword": keyword, "applicationId": RAKUTEN_ID, "page": str(i + 1),
                         "affiliateId": AFFILIATE_ID}
            request = requests.get(REQ_URL, parameter)

            if request.status_code != 200:
                print(f"page:{parameter['page']}　の取得に失敗しました。")
                print(f"errorの内容：{request.content}")
                continue

            json_data = request.json()
            for item in json_data["Items"]:
                info = item["Item"]
                rakutenItem = RakutenItem(itemName=info["itemName"], itemPrice=info["itemPrice"],
                                          itemCaption=info["itemCaption"], affiliateUrl=info["affiliateUrl"],
                                          itemCode=info["itemCode"],
                                          imageUrlRow=json.dumps(info["mediumImageUrls"], ensure_ascii=False))
                if rakutenItem.capacity is None:
                    # 容量を取得できない場合は、データベースへ登録しない
                    continue

                image_request = requests.get(rakutenItem.imageUrl)
                if image_request.status_code != 200:
                    print(f"error:{rakutenItem.itemCode}")
                    continue
                image = ContentFile(image_request.content)

                model_item, created = Item.objects.update_or_create(item_code=rakutenItem.itemCode,
                                                                    defaults=rakutenItem.dictInfo)
                if not created:
                    # 既に作成済みであれば既存の画像を削除する
                    model_item.image.delete()
                model_item.image.save(f'{rakutenItem.itemPrice}.jpg', image, save=True)

class Command(BaseCommand):
    def handle(self, *args, **options):
        fetchRakutenData(SEARCH_WORDS, SEARCH_PAGES)
