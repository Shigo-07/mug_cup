from django.test import TestCase
from main.models import Item
from django.urls import reverse
from urllib.parse import urlencode


class TestItemSetup(TestCase):
    '''
    fixturesの内容をテストする
    主に、素材、容量、値段が意図した個数か確認
    '''
    fixtures = ['test_item.json']

    def test_item_quantity(self):
        '''
        fixturesのデータの個数が、素材ごとに辞書の数分、作成されていること
        '''
        items = Item.objects.all()
        material_dict = {"マグカップ": 12, "グラス": 1, "ステンレス": 1}
        self.assertEqual(len(items), 14)
        for key, value in material_dict.items():
            item = Item.objects.filter(name__icontains=key)
            self.assertEqual(len(item), value)

    def test_capacity_quantity(self):
        '''
        fixturesのデータの個数が、容量ごとに辞書の数分、作成されていること
        '''
        capacity_dict = {"200": 6, "300": 4, "500": 4}
        for key, value in capacity_dict.items():
            item = Item.objects.filter(capacity=int(key))
            self.assertEqual(len(item), value)

    def test_price_quantity(self):
        '''
        fixturesのデータの個数が、値段ごとに辞書の数分、作成されていること
        '''
        price_dict = {"500": 5, "2000": 3, "7500": 2, "20000": 2, "31000": 2}
        for key, value in price_dict.items():
            item = Item.objects.filter(price=int(key))
            self.assertEqual(len(item), value)



class TestUrlQuery(TestCase):
    '''
    CupListViewに対して以下の観点のテストケースを作成する
    ・不正なクエリに対して意図したレスポンスになっているか
    '''
    fixtures = ['test_item.json']

    def setUp(self) -> None:
        self.list_url = reverse("cup:list")

    def test_404_for_negative_integer(self):
        '''int型のqueryに対して負の整数は404エラー'''
        query_dict = {"min_price": -1, "max_price": -1, "min_capacity": -1, "max_capacity": -1}
        for key, value in query_dict.items():
            request_url = "".join([self.list_url, "?", urlencode({key: value})])
            response = self.client.get(request_url)
            self.assertEqual(response.status_code, 404)

    def test_404_for_except_int(self):
        '''int型のqueryに対してint以外はは404エラー'''
        query_list = ["min_price", "max_price", "min_capacity", "max_capacity"]
        value_list = ["string", 10.0, -10.0]
        for query in query_list:
            for value in value_list:
                request_url = "".join([self.list_url, "?", urlencode({query: value})])
                response = self.client.get(request_url)
                self.assertEqual(response.status_code, 404)

    def test_404_for_prohibit_sort(self):
        '''sort=禁止文字は404エラー'''
        request_url = "".join([self.list_url, "?", urlencode({"sort": "prohibit"})])
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 404)

    def test_404_for_samenumber(self):
        '''minとmaxが同じ場合は404エラーを返す'''
        price_dict = {"min_price": 1000, "max_price": 1000}
        capacity_dict = {"min_capacity": 200, "max_capacity": 200}
        list_dict= [price_dict,capacity_dict]
        for dict in list_dict:
            request_url = "".join([self.list_url, "?", urlencode(dict)])
            response = self.client.get(request_url)
            self.assertEqual(response.status_code, 404)

    def test_404_for_large_number(self):
        '''minとmaxが10,000,000以上であれば404エラーを返す'''
        query_dict = {"min_price": 10000000, "max_price": 10000000, "min_capacity": 10000000, "max_capacity": 10000000}
        for key, value in query_dict.items():
            request_url = "".join([self.list_url, "?", urlencode({key: value})])
            response = self.client.get(request_url)
            self.assertEqual(response.status_code, 404)

        query_dict = {"min_price": 9999999, "max_price": 9999999, "min_capacity": 9999999, "max_capacity": 9999999}
        for key, value in query_dict.items():
            request_url = "".join([self.list_url, "?", urlencode({key: value})])
            response = self.client.get(request_url)
            self.assertEqual(response.status_code, 200)

    def test_404_for_large_search_material(self):
        '''search_materialが240文字を超えたとき404エラーをかえす'''
        query_dict = {"search_material":f"{'a' * 240}"}
        request_url = "".join([self.list_url, "?", urlencode(query_dict)])
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 404)

        query_dict = {"search_material":f"{'a' * 239}"}
        request_url = "".join([self.list_url, "?", urlencode(query_dict)])
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)

