from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shopping_cart = models.ForeignKey('Order', on_delete=models.CASCADE, null=True, blank=True, related_name='+')

    def en_shopping_cart(self):
        if not self.shopping_cart:
            self.shopping_cart = Order.objects.create(profile=self)
            self.save()
        return self.shopping_cart

class OrderStatus(models.TextChoices):
    INITIAL = 'INITIAL',
    COMPLETED = 'COMPLETED',
    DELIVERED = 'DELIVERED',

class OrderEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='+')
    count = models.IntegerField(default=0)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_entries')

    @property
    def total_price(self):
        return self.product.price * self.count


class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.INITIAL)

    def add_product(self, product: Product):
        order_entry = self.order_entries.filter(product=product).first()
        if not order_entry:
            order_entry = OrderEntry(product=product, count=0, order=self)
        order_entry.count += 1
        order_entry.save()

