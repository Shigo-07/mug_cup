from django.contrib import admin
from django.urls import path
from .views import ArticleDetail

app_name = "article"
urlpatterns = [
    path("<int:pk>/", ArticleDetail.as_view(), name="article"),
]
