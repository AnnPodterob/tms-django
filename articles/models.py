from django.db import models

# Create your models here.

class Articles(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.CharField(max_length=200)
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title