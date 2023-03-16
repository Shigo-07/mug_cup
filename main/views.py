from django.shortcuts import render
from django.views.generic import ListView, FormView, TemplateView
from .models import Item
from django.http import Http404
from .forms import TopForm
from django.urls import reverse
from urllib.parse import urlencode
from django.db.models import Q


def createUrlPagination(request):
    '''
    目的：ページネーション用にページ数だけ削除したURLを返す
    入力：requestオブジェクト
    戻り値：min、max、search_wordのパラメータを記載したurl　-> str
    '''
    min = request.GET.get("min")
    max = request.GET.get("max")
    search_word = request.GET.get("search_word")
    sort = request.GET.get("sort")
    query_dict = {
        "min": min,
        "max": max,
        "search_word": search_word,
        "sort": sort
    }
    query_dict = {key: value for key, value in query_dict.items() if value}
    urlForPagination = "".join([reverse("cup:list"), "?", urlencode(query_dict)])
    return urlForPagination


def queryFilterSearch(request):
    """
    目的：min,max,search_wordを受け取り、目的のモデルをfilterする
    入力：GETのmin,max,search_wordを受け取る
    戻り値：検索結果を反映したqueryオブジェクト
    補足：
        min → min以上のItem一覧
        max → max以下のItem一覧
        search_word → search_wordが含まれるItem一覧
    """
    min = request.GET.get('min')
    max = request.GET.get("max")
    search_word = request.GET.get("search_word")

    min = None if not min else int(min)
    max = None if not max else int(max)
    search_word = None if not search_word else str(search_word)
    # サイズの検索
    if min and max:
        if min < max:
            query = Item.objects.filter(capacity__range=(min, max))
        else:
            raise Http404("サイズの指定方法に誤りがあります")
    elif min:
        query = Item.objects.filter(capacity__gte=min)
    elif max:
        query = Item.objects.filter(capacity__lte=max)
    else:
        query = Item.objects.all()

    # 単語検索
    if search_word:
        query = query.filter(name__icontains=search_word)

    return query


class TopView(TemplateView):
    template_name = "main/top.html"


class CupListView(ListView):
    template_name = "main/list.html"
    model = Item
    context_object_name = "items"
    paginate_by = 12

    def get_queryset(self):
        query = queryFilterSearch(self.request)
        # ソート条件で並び替え
        if self.request.GET.get("sort"):
            sort_key = self.request.GET.get("sort")
            query = query.order_by(sort_key)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        urlForPagination = createUrlPagination(self.request)
        extra = {"urlForPagination": urlForPagination}
        context.update(extra)
        return context
