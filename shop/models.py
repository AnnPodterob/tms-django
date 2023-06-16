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
    price = models.FloatField(default=0.0)
    description = models.TextField()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shopping_cart = models.ForeignKey('Order', on_delete=models.CASCADE, null=True, blank=True, related_name='+')

    def __str__(self):
        return str(self.user)

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
    status = models.CharField(max_length=23, choices=OrderStatus.choices, default=OrderStatus.INITIAL)

    def __str__(self):
        return f'id:{self.id} - {self.profile} - {self.status}'

    def add_product(self, product: Product):
        order_entry = self.order_entries.filter(product=product).first()
        if not order_entry:
            order_entry = OrderEntry(product=product, count=0, order=self)
        order_entry.count += 1
        order_entry.save()
        self.save()

    @property
    def price(self):
        return sum(order_entry.total_price for order_entry in self.order_entries.all())

    @property
    def product_count(self):
        return sum(order_entry.count for order_entry in self.order_entries.all())

    # def is_empty(self):
    #     return not self.order_entries.exists()