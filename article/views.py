from django.shortcuts import render
from django.views.generic import DetailView
from article.models import Article


# Create your views here.
class ArticleDetail(DetailView):
    model = Article
    context_object_name = "article"
    template_name = "article/article.html"

