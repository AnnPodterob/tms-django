from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Product
from .models import Order, OrderEntry, OrderStatus
from .models import Profile
from django.contrib import messages



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

@login_required
def cart(request):
    # order = Order.objects.get_or_create(user=request.user)[0]
    order_entries = OrderEntry.objects.all()
    total_price = sum(entry.total_price for entry in order_entries)
    context = {
        'order_entries': order_entries,
        'total_price': total_price,
    }
    request.user.profile.en_shopping_cart()
    return render(request, 'shop/cart.html', context)

@login_required
def clear_cart(request):
    profile = request.user.profile
    order = profile.shopping_cart
    OrderEntry.objects.filter(order=order).delete()
    return redirect('shop:cart')

@login_required
def place_order(request):
    profile = request.user.profile
    order = profile.shopping_cart
    order.status = OrderStatus.COMPLETED
    order.save()
    profile.shopping_cart = Order.objects.create(profile=profile)
    profile.save()
    return render(request, 'shop/cart.html', {'order': order})
    # profile = request.user.profile
    # order = profile.shopping_cart
    # order.status = OrderStatus.COMPLETED
    # order.save()
    # profile.shopping_cart = Order.objects.create(profile=profile)
    # profile.save()
    # Order.objects.create(profile=profile)
    # messages.success(request, 'Заказ успешно оформлен')
    # return redirect('shop:cart')