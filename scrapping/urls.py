from django.urls import path
from .views import *

urlpatterns = [
    path('', NewsScrapeView.as_view(),name='home'),
]