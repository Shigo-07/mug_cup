from django.shortcuts import render
from django.views.generic import ListView
from .models import Item
# Create your views here.

class CupListView(ListView):
    template_name = "main/list.html"
    model = Item
    context_object_name = "items"

    def get_queryset(self):
        capacity = self.request.GET.get('capacity')
        if capacity:
            return Item.objects.filter(capacity__gte=capacity)
        else:
            return Item.objects.all()
