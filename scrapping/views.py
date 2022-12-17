from django.shortcuts import render
from django.views import generic
from .models import News

# Create your views here.
class NewsScrapeView(generic.ListView):
    template_name='home.html'
    context_object_name='article'

    def get_queryset(self):
        return News.objects.all()
    