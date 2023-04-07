from django.test import TestCase
from main.models import Item
from django.urls import reverse
from urllib.parse import urlencode


class TestAnyView(TestCase):
    '''
    list view以外の表示に関するテストケースを記述
    '''

    def test_redirect_root(self):
        '''/へアクセスしたときに/cup/へリダイレクトするか'''
        response = self.client.get("/")
        self.assertRedirects(response, "/cup/")

    def test_response_about(self):
        '''/about/へアクセスしたときに200でレスポンスがあるか'''
        response = self.client.get("/cup/about/")
        self.assertEqual(response.status_code, 200)

    def test_response_owner(self):
        '''/owner/へアクセスしたときに200でレスポンスがあるか'''
        response = self.client.get("/cup/owner/")
        self.assertEqual(response.status_code, 200)

    def test_response_privacy(self):
        '''/privacy/へアクセスしたときに200でレスポンスがあるか'''
        response = self.client.get("/cup/privacy/")
        self.assertEqual(response.status_code, 200)
