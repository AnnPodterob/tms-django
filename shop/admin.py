from django.contrib import admin
from .models import Category, Product
from .models import Profile, Order, OrderEntry
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# admin.site.register(Profile)

# admin.site.register(OrderEntry)
# admin.site.register(Product)
#


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInline]


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [OrderInline]


@admin.register(OrderEntry)
class OrderEntryAdmin(admin.ModelAdmin):
    pass


class OrderEntryInline(admin.TabularInline):
    model = OrderEntry
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderEntryInline]


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]


# class ProductInline(admin.StackedInline):
#     model = Product
#     extra = 0
#
# class ProductAdmin(admin.ModelAdmin):
#      list_display = ['name']
#
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     inlines = [ProductInline]
#
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     search_fields = ['profile']
#     list_display = ['profile']
#
# @admin.register(OrderEntry)
# class OrderEntryAdmin(admin.ModelAdmin):
#     search_fields = ['product', 'order']
#     list_display = ['product', 'order']
#
# class OrderInline(admin.TabularInline):
#     model = Order
#     extra = 0
#
# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     search_fields = ['user', 'shopping_cart']
#     list_display = ['user', 'shopping_cart']
#     inlines = [OrderInline]
#
# @admin.register(OrderEntry)
# class OrderEntryAdmin(admin.ModelAdmin):
#     pass
#
# class OrderEntryInline(admin.TabularInline):
#     model = OrderEntry
#     extra = 0
#
# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#
#
# admin.site.unregister(User)
#
# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     inlines = [ProfileInline]