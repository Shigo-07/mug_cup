from django.core.management.base import BaseCommand
from urllib.parse import urlparse
from main.models import Item
from config.local_settings import RAKUTEN_ID
# from main.models import Item
from django.core.files.images import ImageFile
from django.core.files.base import ContentFile
import unicodedata
import re
import requests
import json
import time

REQ_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
PATTERN = "[0-9]+\.?[0-9]*ml|[0-9]+\.?[0-9]*cc|[0-9]+\.?[0-9]*l"
SEARCH_WORDS = ["マグカップ", "グラス", "コップ"]
SEARCH_PAGES = 50
IMAGE_RESIZE = "_ex=400x400"


def wordsToCapacity(words: str):
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

            parameter = {"format": "json", "keyword": keyword, "applicationId": RAKUTEN_ID, "page": str(i + 1)}
            request = requests.get(REQ_URL, parameter)

            if request.status_code != 200:
                print(f"page:{parameter['page']}　の取得に失敗しました。")
                print(f"errorの内容：{request.content}")
                continue

            json_data = request.json()
            for item in json_data["Items"]:
                info = item["Item"]
                # 半角かつ小文字へ変換する
                words = unicodedata.normalize('NFKC', info["itemName"]).lower()
                # タイトルから容量を取得する
                capacity = wordsToCapacity(words)
                if not capacity:  # タイトルで取得できない場合は説明欄から取得
                    words = unicodedata.normalize('NFKC', info["itemCaption"]).lower()
                    capacity = wordsToCapacity(words)
                    if not capacity:  # 容量情報がない場合、登録しない
                        continue

                data = {}

                data["name"] = info["itemName"]
                data["price"] = info["itemPrice"]
                data["caption"] = info["itemCaption"]
                data["item_url"] = info["itemUrl"]
                data["item_code"] = info["itemCode"]
                data["image_url"] = json.dumps(info["mediumImageUrls"], ensure_ascii=False)
                data["capacity"] = capacity

                # 取得する画像サイズのクエリを変更する
                image_url = urlparse(info["mediumImageUrls"][0]["imageUrl"])._replace(query=IMAGE_RESIZE).geturl()
                image_request = requests.get(image_url)
                if image_request.status_code != 200:
                    print(f"error:{data['item_code']}")
                    continue
                image = ContentFile(image_request.content)

                model_item, created = Item.objects.update_or_create(item_code=data["item_code"], defaults=data)
                if not created:
                    model_item.image.delete()
                model_item.image.save(f'{data["price"]}.jpg', image, save=True)


class Command(BaseCommand):
    def handle(self, *args, **options):
        fetchRakutenData(SEARCH_WORDS, SEARCH_PAGES)
