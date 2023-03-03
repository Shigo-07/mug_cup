from django.core.management.base import BaseCommand

from main.models import Item
from config.local_settings import RAKUTEN_ID
# from main.models import Item
from django.core.files.images import ImageFile
from django.core.files.base import ContentFile

import requests
import json
import os

REQ_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
param = {"format": "json", "keyword": "マグカップ", "applicationId": RAKUTEN_ID}


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("===============start get rakuten ichiba===============")
        request = requests.get(REQ_URL, param)
        if request.status_code != 200:
            print("error:APIから結果を得ることができませんでした。")
            exit()
        json_result = request.json()
        for item in json_result["Items"]:
            data = {}
            info = item["Item"]
            data["name"] = info["itemName"]
            data["price"] = info["itemPrice"]
            data["caption"] = info["itemCaption"]
            data["item_url"] = info["itemUrl"]
            data["item_code"] = info["itemCode"]
            data["image_url"] = json.dumps(info["mediumImageUrls"], ensure_ascii=False)

            image_request = requests.get(info["mediumImageUrls"][0]["imageUrl"])
            if image_request.status_code != 200:
                continue
            image = ContentFile(image_request.content)
            # model_item = Item(**data)
            model_item, created = Item.objects.update_or_create(item_code=data["item_code"], defaults=data)
            model_item.image.save(f'{data["price"]}.jpg', image, save=False)

        print("===============end get rakuten ichiba===============")
