from django.test import TestCase
from main.models import Item
from django.core.management import call_command
from unittest.mock import patch, MagicMock

class TestScrapingRakuten(TestCase):
    '''
    楽天のスクレイピングコマンドのテストを実施
    '''

    def test_rakuten_item(self):
        from main.management.commands.scraping_rakuten import fetchRakutenData, RakutenItem

        json_data = {"Items": [
            {"Item": {"itemName": "マグカップ 100ml", "itemPrice": 1000, "itemCaption": "容量300ml",
                      "affiliateUrl": "https://rakuten.co.jp/item1", "itemCode": "item1",
                      "mediumImageUrls": [{
                                              "imageUrl": "https://thumbnail.image.rakuten.co.jp/@0_mall/moccasin/cabinet/main04/b69.jpg?_ex=128x128"}, ],
                      "shopName": "shop1"}},
            {"Item": {"itemName": "グラス  100ml", "itemPrice": 500, "itemCaption": "容量250ml",
                      "affiliateUrl": "https://rakuten.co.jp/item2", "itemCode": "item2",
                      "mediumImageUrls": [{
                                              "imageUrl": "https://thumbnail.image.rakuten.co.jp/@0_mall/moccasin/cabinet/main04/b69.jpg?_ex=128x128"}, ],
                      "shopName": "shop1"}},
            {"Item": {"itemName": "コップ  100ml", "itemPrice": 800, "itemCaption": "容量500ml",
                      "affiliateUrl": "https://rakuten.co.jp/item3", "itemCode": "item3",
                      "mediumImageUrls": [{
                                              "imageUrl": "https://thumbnail.image.rakuten.co.jp/@0_mall/moccasin/cabinet/main04/b69.jpg?_ex=128x128"}, ],
                      "shopName": "shop1"}},
        ]}

        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_res.json.return_value = json_data

        with patch('main.management.commands.scraping_rakuten',return_value=mock_res):
            fetchRakutenData(["マグカップ"],1)

        print(Item.objects.all())
        print(len(Item.objects.all()))