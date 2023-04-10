from django.core.management.base import BaseCommand
from main.models import Item
import time
import requests
from django.conf import settings

REQ_URL = "https://shopping.yahooapis.jp/ShoppingWebService/V1/json/itemLookup"
YAHOO_ID = settings.YAHOO_ID


def RemoveNotExistItem(model):
    items = model.objects.filter(seller="yahoo")
    delete_counts = 0
    delete_items = []
    for item in items:
        time.sleep(1.5)
        parameter = {"appid": YAHOO_ID, "itemcode": item.item_code}

        request = requests.get(REQ_URL, parameter)
        if request.status_code != 200:
            print(f"errorの内容：{request.content}")
            continue

        json_data = request.json()
        # アイテムが存在しない場合は画像とデータを削除する
        if int(json_data["ResultSet"]["totalResultsReturned"]) == 0:
            delete_items.append(parameter["itemcode"])
            item.image.delete()
            item.delete()
            delete_counts += 1

    return delete_counts, delete_items


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("===============start check yahoo item===============")
        delete_counts, delete_items = RemoveNotExistItem(Item)
        print(f"削除したデータ数：{delete_counts},itemCode:{'-'.join(delete_items)}")
        print("===============end check yahoo item===============")
