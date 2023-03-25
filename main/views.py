from django.shortcuts import render
from django.views.generic import ListView, FormView, TemplateView
from .models import Item
from django.http import Http404
from .forms import TopForm
from django.urls import reverse
import urllib.parse
from django.db.models import Q


def createUrlPagination(request):
    '''
    目的：検索クエリを残しながら、ページネーションのpageだけ抜いたURLを返す
    入力：request => djangoのrequestオブジェクト
    出力：urlForPagination => string
    '''
    url = request.build_absolute_uri()
    pr = urllib.parse.urlparse(url)
    d = urllib.parse.parse_qs(pr.query)
    d.pop("page", None)
    return urllib.parse.urlunparse(pr._replace(query=urllib.parse.urlencode(d, doseq=True)))


def conditionFromRange(min: int, max: int, field: str):
    if min and max:
        if min < max:
            dict_q = {f"{field}__range": (min, max)}
            condition = Q(**dict_q)
        else:
            raise Http404("サイズの指定方法に誤りがあります")
    elif min:
        dict_q = {f"{field}__gte": min}
        condition = Q(**dict_q)
    elif max:
        dict_q = {f"{field}__lte": max}
        condition = Q(**dict_q)
    else:
        condition = None

    return condition


def conditionFromRequet(request):
    """
    目的：requestのクエリからItemオブジェクトをソート・検索する
    入力：request => djangoのrequestオブジェクト
    出力：condition => djangoのQオブジェクト
    """
    dict_int_query = {
        "min_capacity": 0,
        "max_capacity": 0,
        "min_price": 0,
        "max_price": 0,
    }
    for key in dict_int_query.keys():
        dict_int_query[key] = request.GET.get(key)
        dict_int_query[key] = None if not dict_int_query[key] else int(dict_int_query[key])

    search_material = request.GET.get("search_material")
    search_material = None if not search_material else str(search_material)

    # サイズの検索
    condition_size = conditionFromRange(
        min=dict_int_query["min_capacity"],
        max=dict_int_query["max_capacity"],
        field="capacity"
    )
    # 価格の検索
    condition_price = conditionFromRange(
        min=dict_int_query["min_price"],
        max=dict_int_query["max_price"],
        field="price"
    )
    # 単語検索
    if search_material:
        condition_material = Q(name__icontains=search_material)
    else:
        condition_material = None

    # 結合用に空のQオブジェクトを作成
    conditions = Q()
    condition_all = [condition_size, condition_price, condition_material]
    for condition in condition_all:
        if condition != None:
            conditions &= condition

    return conditions


class TopView(TemplateView):
    template_name = "main/top.html"


class CupListView(ListView):
    template_name = "main/list.html"
    model = Item
    context_object_name = "items"
    paginate_by = 12

    def get_queryset(self):
        # URLのクエリパラメータからQオブジェクトを取得
        Q_conditions = conditionFromRequet(self.request)
        query = Item.objects.filter(Q_conditions)
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


class TestView(TemplateView):
    template_name = "404.html"