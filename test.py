from urllib.parse import urlparse
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

query = "マグカップ"
url = "https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch"

url_code = "https://shopping.yahooapis.jp/ShoppingWebService/V1/json/itemLookup"


@dataclass
class RakutenItem:
    itemName: str
    itemPrice: int
    itemCaption: str
    affiliateUrl: str
    itemCode: str
    imageUrlRow: str
    seller: str

    @property
    def capacity(self):
        '''nameもしくはcaptionから容量を算出する'''
        # 正規表現で検査できるよう、半角かつ小文字へ変換
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
        ''' 取得する画像がデフォルトだと小さいため、URLのサイズクエリを書き換えする'''
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
            "seller": self.seller,
        }

    def _wordsToCapacity(self, words: str):
        '''
        目的：正規表現を使って、下記の処理を行う
        ・文字列からml、l、ccの単位が付いている数値を取り出す
        ・int型のml単位の値を返す
        入力：words -> str
        出力：list_number[0] -> int or None
        '''
        # 正規表現で検査できるよう、半角かつ小文字へ変換
        # words = unicodedata.normalize('NFKC', words).lower()
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


params = {
    "appid": app_id,
    "query": query,
    "image_size": 600,
    "affiliate_id": AFFILIATE_ID,
    "affiliate_type": "vc",
}

response = requests.get(url, params=params)
data = response.json()
json_data = response.json()
for item in json_data["hits"]:
    print("=====================================================")
    print(item["name"])
    print(item["description"])
    print(item["url"])
    print(item["price"])
    print(item["code"])
    params_code = {"appid": app_id, "itemcode": item["code"]}
    res = requests.get(url_code, params=params_code)
    data_code = res.json()
    print(data_code)
    print("=====================================================")
