from django.core.management.base import BaseCommand
from main.models import Item

# コップ以外の商品を削除するためのキーワードを入力する
REMOVE_WORD_LIST = [
    "エプソン",
    "カートリッジ",
    "ふるさと納税",
]

def remove_item_match_word():
    '''
    REMOVE_WORD_LISTに一致するワードが含まれる場合は、そのデータを削除する
    '''
    for remove_word in REMOVE_WORD_LIST:
        remove_items = Item.objects.filter(name__icontains=remove_word)
        for remove_item in remove_items:
            remove_item.image.delete()
            remove_item.delete()

def remove_item_over_1l():
    '''
    1L以上のアイテムは削除する
    '''
    remove_items = Item.objects.filter(capacity__gt=1000)
    for remove_item in remove_items:
        remove_item.image.delete()
        remove_item.delete()
class Command(BaseCommand):

    def handle(self, *args, **options):
        remove_item_match_word()
        remove_item_over_1l()