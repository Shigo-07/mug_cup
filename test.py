import requests
from dataclasses import dataclass
import unicodedata
import re

REQ_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
PATTERN = "[0-9]+\.?[0-9]*ml|[0-9]+\.?[0-9]*cc|[0-9]+\.?[0-9]*l"
SEARCH_WORDS = ["マグカップ", "グラス", "コップ"]

app_id = "dj00aiZpPU1vQ0xCT1llUnlobyZzPWNvbnN1bWVyc2VjcmV0Jng9MWE-"
query = "マグカップ"
url = "https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch"


@dataclass
class YahooProduct:
    itemName: str
    itemPrice: int
    itemCaption: str
    affiliateUrl: str
    itemCode: str
    imageUrl: str

    @property
    def capacity(self):
        '''nameもしくはcaptionから容量を算出する'''
        # 正規表現で検査できるよう、半角かつ小文字へ変換
        words = unicodedata.normalize('NFKC', self.itemName).lower()
        # タイトルから容量を取得する
        capacity = self._extractCapacity(words)

        if not capacity:  # タイトルで取得できない場合は説明欄から取得
            words = unicodedata.normalize('NFKC', self.itemCaption).lower()
            capacity = self._extractCapacity(words)
            if not capacity:  # 容量情報がない場合はモデルへ登録できないため、登録できないデータとしてNoneを返す
                return None

        return capacity

    def _extract_capacity(self, words: str):
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

}

response = requests.get(url, params=params)
data = response.json()

for item in data["hits"]:
    print("商品名:", item["name"])
    print("価格:", item["price"])
    print("URL:", item["url"])
    print("画像URL", item["exImage"]["url"])
    print("===================")

# if __name__ == "__main__":
#     pass
