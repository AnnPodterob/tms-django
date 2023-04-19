from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    # price = models.DecimalField(max_digit=8, decimal_places=2)

    def __str__(self):
        return self.name