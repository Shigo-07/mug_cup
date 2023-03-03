from django.core.management.base import BaseCommand

class Commanc(BaseCommand):

    def handle(self, *args, **options):
        print("===============start check capacity===============")

        print("===============end check capacity===============")