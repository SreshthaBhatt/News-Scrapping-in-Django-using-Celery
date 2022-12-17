from django.db import models

# Create your models here.
class News(models.Model):
    title=models.CharField(max_length=250)
    link=models.CharField(max_length=2100,default="",unique=True)
    published=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    source = models.CharField(max_length=30, default="", blank=True, null=True)

