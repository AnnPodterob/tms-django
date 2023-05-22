from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Product
from .models import Order, OrderEntry
from .models import Profile


def index(request):
    return render(request, 'shop/index.html', {
        'categories': Category.objects.all(),
    })


def category_detail(request, category_id: int):
    return render(request, 'shop/category_detail.html', {
        'category': get_object_or_404(Category, id=category_id),
    })


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'shop/index.html', {'categories': categories})


def product_detail(request, product_id: int):
    return render(request, 'shop/product_detail.html', {
        'product': get_object_or_404(Product, id=product_id),
    })


def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product.html', {'products': products})


@login_required
def add_to_cart(request):
    assert request.method == 'POST'
    product_id = request.POST['product_id']
    product = get_object_or_404(Product, id=product_id)
    request.user.profile.en_shopping_cart().add_product(product)
    # profile = Profile.objects.all()
    # if not profile.shopping_cart:
    #     profile.shopping_cart = Order.objects.create(profile=self)
    #     profile.save()
    # pr = profile.shopping_cart
    # order = Order.objects.all()
    # order_entry = order.order_entries.filter(product=product).first()
    # if not order_entry:
    #     order_entry = OrderEntry(product=product, count=0, order=self)
    # order_entry.count += 1
    # order_entry.save()
    # order = get_object_or_404(OrderEntry, id=product_id)
    # order.count += 1
    # order.save()
    return redirect('shop:product_detail', product_id)

