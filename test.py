from config.local_settings import RAKUTEN_ID
import re
import requests

REQ_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
param = {"format": "json", "keyword": "マグカップ", "applicationId": RAKUTEN_ID}

request = requests.get(REQ_URL, param)
if request.status_code != 200:
    print("error:APIから結果を得ることができませんでした。")
    exit()
json_result = request.json()
for item in json_result["Items"]:
    res = re.findall("[0-9]*ml", item["Item"]["itemName"])
    if res:
        print(f"name:{res}")
        print(f"url:{item['Item']['itemUrl']}")
        continue
    res = re.findall("[0-9]*ml", item["Item"]["itemCaption"])
    if res:
        print(f"caption:{res}")
        print(f"url:{item['Item']['itemUrl']}")
        continue
    res = re.findall("[0-9]*cc", item["Item"]["itemCaption"])
    if res:
        print(f"caption:{res}")
        print(f"url:{item['Item']['itemUrl']}")
        continue