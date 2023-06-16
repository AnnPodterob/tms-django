from django.shortcuts import get_object_or_404
from .models import Category, Product
from .models import Order, OrderEntry, OrderStatus
from .models import Profile
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import UserForm, NewUserForm
from django.contrib.auth import login


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
    pagin = Paginator(products, 5)

    page = request.GET.get('page')
    obj = pagin.get_page(page)
    return render(request, 'shop/product.html', {'products': products, 'page': obj,})


def add_to_cart(request):
    assert request.method == 'POST'
    product_id = request.POST['product_id']
    product = get_object_or_404(Product, id=product_id)
    request.user.profile.en_shopping_cart().add_product(product)
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
def submit_order(request):
    profile = request.user.profile
    order = profile.shopping_cart
    order.status = OrderStatus.COMPLETED
    order.save()
    profile.shopping_cart = Order.objects.create(profile=profile)
    profile.save()
    messages.success(request, "Order completed successfully")
    return render(request, 'shop/order_s_s.html', {'order': order})

def delete_order_entries(request):
    assert request.method == "POST"
    order = request.user.profile.shopping_cart
    order.order_entries.all().delete()
    order.save()
    return redirect('shop:cart')

@login_required()
def delete_order_entry(request):
    shopping_cart = request.user.profile.shopping_cart
    shopping_cart.order_entries.filter(id=request.POST['order_id']).delete()
    shopping_cart.save()
    messages.success(request, "Product delete")
    return redirect('shop:cart')

@login_required
def user_profile(request):
    user = request.user
    orders = request.user.profile.orders.all().order_by('id').reverse()[:5]
    context = {'user': user, 'orders': orders}
    return render(request, 'shop/user_profile.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = request.user
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            messages.success(request, "You are change information ;)")
            return redirect('shop:update_profile')
    else:
        form = UserForm(instance=request.user)
    return render(request, 'shop/update_profile.html', {'form': form})
    # if request.method == 'POST':
    #     user = request.user
    #     user.first_name = request.POST['first_name']
    #     user.last_name = request.POST['last_name']
    #     user.email = request.POST['email']
    #     user.save()
    #     return redirect('user_profile')
    # else:
    #     user = request.user
    #     context = {'user': user}
    #     return render(request, 'update_profile.html', context)



@login_required()
def edit_count_order_entry(request):
    shopping_cart = request.user.profile.shopping_cart.order_entries.get(id=request.POST['entry_id'])
    shopping_cart.count = request.POST['entry_count']
    shopping_cart.save()
    return redirect('shop:cart')

@login_required
def order_history(request):
    orders = request.user.profile.orders.all().order_by('id').reverse()[:5]
    # orders = Order.objects.filter(user=request.user).order_by('-id')[:5]
    pagin = Paginator(orders, 5)

    page = request.GET.get('page')
    obj = pagin.get_page(page)
    return render(request, 'shop/order_history.html', {'orders': orders, 'page':obj,})


@login_required()
def repeat_order(request):
    profile = request.user.profile
    shopping_cart = profile.shopping_cart
    shopping_cart.order_entries.all().delete()
    profile.shopping_cart.save()
    orders = request.user.profile.orders.get(id=request.POST['order_id'])
    for order in orders.order_entries.all():
        profile.shopping_cart.order_entries.create(product=order.product, count=order.count)
        profile.shopping_cart.save()
    profile.save()
    return redirect('shop:cart')


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('shop:index')
        messages.error(request, "Invalid information.")
    form = NewUserForm()
    return render(request, "registration/register.html", context={"form": form})


def search_products(request):
    products = Product.objects.filter(name__icontains=request.POST['search'])
    pagin = Paginator(products, 5)

    page = request.GET.get('page')
    obj = pagin.get_page(page)
    return render(request, 'shop/search.html', {
        'products': products, 'page': obj,
    })