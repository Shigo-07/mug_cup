import json
import requests
import re
import pprint

REQ_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
param = {"format": "json", "keyword": "マグカップ", "applicationId": "1041635425516382228"}

result = requests.get(REQ_URL, param)
json_result = result.json()
for item in json_result["Items"]:
    # print(re.findall("[0-9]*ml", item["Item"]["itemName"]))
    info = item["Item"]
    image_url = info["mediumImageUrls"]
    itemCaption = info["itemCaption"]
    itemUrl = info["itemUrl"]
    itemPrice = info["itemPrice"]
    itemName = info["itemName"]
    print(itemName, image_url, itemCaption, itemUrl, itemPrice)
