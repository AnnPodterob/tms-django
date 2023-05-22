from django.contrib import admin
from .models import Category, Product
from .models import Profile, Order, OrderEntry

# admin.site.register(Profile)

# admin.site.register(OrderEntry)
admin.site.register(Product)

class ProductInline(admin.StackedInline):
    model = Product
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ['profile']
    list_display = ['profile']

@admin.register(OrderEntry)
class OrderEntryAdmin(admin.ModelAdmin):
    search_fields = ['product', 'order']
    list_display = ['product', 'order']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user', 'shopping_cart']
    list_display = ['user', 'shopping_cart']
    # inlines = [OrderInline]