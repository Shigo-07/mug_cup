from django.core.management.base import BaseCommand
from main.models import Item

def RemoveNotExistItem(model):
    pass


class Commanc(BaseCommand):

    def handle(self, *args, **options):
        print("===============start check rakuten item===============")

        print("===============end check rakuten item===============")