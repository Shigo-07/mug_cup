from django.contrib import admin
from django.urls import path
from .views import CupListView, TopView, AboutView, OwnerView, PrivacyView

app_name = "cup"
urlpatterns = [
    path("list/", CupListView.as_view(), name="list"),
    path("about/", AboutView.as_view(), name="about"),
    path("owner/", OwnerView.as_view(), name="owner"),
    path("privacy/", PrivacyView.as_view(),name="privacy"),
    path("", TopView.as_view(), name="top"),
    # path("error/",ErrorView.as_view()),
]
