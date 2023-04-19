from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Category

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def index(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'shop/index.html', context)

def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category)
    context = {'category': category, 'products': products}
    return render(request, 'shop/category.html', context)

def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'shop/product.html', context)