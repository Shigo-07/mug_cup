from django.core.management.base import BaseCommand
from main.models import Item
import time
from config.local_settings import RAKUTEN_ID
import requests

REQ_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"


def RemoveNotExistItem(model):
    items = model.objects.all()
    delete_counts = 0
    delete_items = []
    for item in items:
        time.sleep(1.5)
        parameter = {"format": "json", "applicationId": RAKUTEN_ID, "itemCode": item.item_code}

        request = requests.get(REQ_URL, parameter)
        if request.status_code != 200:
            print(f"errorの内容：{request.content}")
            continue

        json_data = request.json()
        # アイテムが存在しない場合は画像とデータを削除する
        if len(json_data["Items"]) == 0:
            delete_items.append(parameter["itemCode"])
            item.image.delete()
            item.delete()
            delete_counts += 1

    return delete_counts, delete_items


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("===============start check rakuten item===============")
        delete_counts, delete_items = RemoveNotExistItem(Item)
        print(f"削除したデータ数：{delete_counts},itemCode:{'-'.join(delete_items)}")
        print("===============end check rakuten item===============")
