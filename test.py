import json
import requests
import re
import pprint
from config.local_settings import RAKUTEN_ID
# from main.models import Item
from pathlib import Path

REQ_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
param = {"format": "json", "keyword": "マグカップ", "applicationId": RAKUTEN_ID}

result = requests.get(REQ_URL, param)
if result.status_code != 200:
    exit()
    # ロギング用の処理を行う

json_result = result.json()
for item in json_result["Items"]:
    data = {}
    info = item["Item"]
    data["name"] = info["itemName"]
    data["price"] = info["itemPrice"]
    data["caption"] = info["itemCaption"]
    data["item_url"] = info["itemUrl"]
    data["item_code"] = info["itemCode"]
    data["image_url"] = json.dumps(info["mediumImageUrls"], ensure_ascii=False)
    pprint.pprint(data)
    image = requests.get(info["mediumImageUrls"][0]["imageUrl"]).content
    path_image = Path.joinpath(Path(__file__).parent, "test", f"{data['price']}.jpg")
    with open(path_image,"wb") as f:
        f.write(image)