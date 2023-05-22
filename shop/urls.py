
from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>', views.product_detail, name='product_detail'),
    path('products/', views.product_list, name='products'),
    path('categories/', views.category_list, name='categories'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('place_order', views.place_order, name='place_order'),
]