from config.local_settings import RAKUTEN_ID
import urllib
import re
import requests
import unicodedata
import json
from django.core.files.base import ContentFile

REQ_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
param = {"format": "json", "keyword": "マグカップ", "applicationId": RAKUTEN_ID}
PATTERN = "[0-9]+\.?[0-9]*ml|[0-9]+\.?[0-9]*cc|[0-9]+\.?[0-9]*l"

# request = requests.get(REQ_URL, param)
# if request.status_code != 200:
#     print("error:APIから結果を得ることができませんでした。")
#     exit()
# json_result = request.json()
# for item in json_result["Items"]:
#     res = re.findall("[0-9]*ml", item["Item"]["itemName"])
#     if res:
#         print(f"name:{res}")
#         print(f"url:{item['Item']['itemUrl']}")
#         continue
#     res = re.findall("[0-9]*ml", item["Item"]["itemCaption"])
#     if res:
#         print(f"caption:{res}")
#         print(f"url:{item['Item']['itemUrl']}")
#         continue
#     res = re.findall("[0-9]*cc", item["Item"]["itemCaption"])
#     if res:
#         print(f"caption:{res}")
#         print(f"url:{item['Item']['itemUrl']}")
#         continue

SEARCH_WORDS = ["マグカップ"]
SEARCH_PAGES = 50


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

                image_request = requests.get(info["mediumImageUrls"][0]["imageUrl"])
                if image_request.status_code != 200:
                    continue
                image = ContentFile(image_request.content)
                # model_item = Item(**data)
                model_item, created = Item.objects.update_or_create(item_code=data["item_code"], defaults=data)
                model_item.image.save(f'{data["price"]}.jpg', image, save=False)


def ResizeImageUrl(url):
    return urllib.parse.urlparse(url)._replace(query="_ex=400x400").geturl()


if __name__ == "__main__":
    # fetchRakutenData(SERARCH_WORDS, SEARCH_PAGES)
    url = "https://thumbnail.image.rakuten.co.jp/@0_mall/scamposaka/cabinet/2023ss/veitecoeur/fc-037-0-0211.jpg?_ex=128x128"
    print(ResizeImageUrl(url))
