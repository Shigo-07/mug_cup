from django.contrib import admin
from django.urls import path
from .views import CupListView

urlpatterns = [
    path("", CupListView.as_view(), name="list"),
]
