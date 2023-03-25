from django.core.management.base import BaseCommand
from main.models import Item

# コップ以外の商品を削除するためのキーワードを入力する
REMOVE_WORD_LIST = [
    "エプソン",
    "カートリッジ",
]

class Command(BaseCommand):

    def handle(self, *args, **options):
        for remove_word in REMOVE_WORD_LIST:
            remove_items = Item.objects.filter(name__icontains=remove_word)
            for remove_item in remove_items:
                remove_item.image.delete()
                remove_item.delete()
