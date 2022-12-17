from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display=['id','title','link','published','created_at','updated_at','source']
    ordering=['-updated_at']