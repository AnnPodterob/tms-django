from django.db import models
from django.contrib import admin

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()

class Articles(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    like_count = models.IntegerField(default=0)
    authors = models.ManyToManyField(Author)

    @admin.display(
        boolean=True,
        description="Is popular?",
        ordering='like_count'
    )

    def __str__(self):
        return self.title

    def is_popular(self):
        return self.like_count > 100

