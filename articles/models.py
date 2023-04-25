from django.db import models
from django.contrib import admin

# Create your models here.

class Articles(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.CharField(max_length=200)
    like_count = models.IntegerField(default=0)

    @admin.display(
        boolean=True,
        description="Is popular?",
        ordering='like_count'
    )

    def __str__(self):
        return self.title

    def is_popular(self):
        return self.like_count > 100