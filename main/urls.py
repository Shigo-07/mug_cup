from django.contrib import admin
from django.urls import path
from .views import CupListView, TopView

app_name = "cup"
urlpatterns = [
    path("list/", CupListView.as_view(), name="list"),
    path("", TopView.as_view(), name="top"),
]
