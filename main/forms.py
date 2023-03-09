from django.forms import (
    forms,
    CharField,
    IntegerField
)


class TopForm(forms.Form):
    """ トップページ用のフォーム　"""
    min = IntegerField(label="最低容量", min_value=50, max_value=900, required=False)
    max = IntegerField(label="最低容量", min_value=100, max_value=1000, required=False)
    search_word = CharField(label="検索単語", max_length=20, required=False)
