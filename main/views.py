from django.shortcuts import render
from django.views.generic import ListView, FormView
from .models import Item
from django.http import Http404
from .forms import TopForm
from django.urls import reverse
from urllib.parse import urlencode
from django.db.models import Q


# Create your views here.

class TopView(FormView):
    template_name = "main/top.html"
    form_class = TopForm

    def get_success_url(self):
        """
        入力：postメソッドのパラメータを受け取る
        出力：/list/?min=**&max=**
        """
        min = self.request.POST.get("min")
        max = self.request.POST.get("max")
        search_word = self.request.POST.get("search_word")
        query_dict = {
            "min": min,
            "max": max,
            "search_word": search_word,
        }
        query_dict = {key: value for key, value in query_dict.items() if value}
        return_url = "".join([reverse("cup:list"), "?", urlencode(query_dict)])
        return return_url


class CupListView(ListView):
    template_name = "main/list.html"
    model = Item
    context_object_name = "items"
    paginate_by = 10

    def get_queryset(self):
        """
        入力：GETのmin,max,search_wordを受け取る
        出力：
        
            min → min以上のItem一覧
            max → max以下のItem一覧
            search_word → search_wordが含まれるItem一覧
        """
        min = self.request.GET.get('min')
        max = self.request.GET.get("max")
        search_word = self.request.GET.get("search_word")

        # min = min if not min else None if isinstance(min, int) else int(min)
        min = None if not min else int(min)
        # max = max if not max else None if isinstance(max, int) else int(max)
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
