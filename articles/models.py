from django.db import models

# Create your models here.

class Articles(models.Model):

    title = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    like_count = models.IntegerField(default=0)

