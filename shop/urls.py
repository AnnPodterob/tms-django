
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
    path('submit_order/', views.submit_order, name='submit_order'),
    path('delete_order_entries/', views.delete_order_entries, name='delete_order_entries'),
    path('delete_order_entry/', views.delete_order_entry, name='delete_order_entry'),
    path('edit_count_order_entry/', views.edit_count_order_entry, name="edit_count_order_entry"),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('user_profile/update_profile/', views.update_profile, name='update_profile'),
    path('history/', views.order_history, name='order_history'),
    path('repeat/<int:order_id>/', views.repeat_order, name='repeat_order'),
    path("register/", views.register_request, name="register"),
    path('search/',views.search_products, name='search_products'),
]