from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from users.models import User, City, User_Product, User_Shop
from price.models import Price

# Create your views here.

from users.forms import UserProfileForm
from price.forms import AddProductToUserForm, AddShopToUserForm, AddProductForm, AddShopForm, PriceForm

def table(request):
    user = request.user
    if request.method == 'POST':
        if 'add_product_to_user' in request.POST:
            product_user_form = AddProductToUserForm(user, request.POST)
            if product_user_form.is_valid():
                product_user_form.save()
                return HttpResponseRedirect(reverse('price:table'))
        elif 'add_shop_to_user' in request.POST:
            shop_user_form = AddShopToUserForm(user, request.POST)
            if shop_user_form.is_valid():
                shop_user_form.save()
                return HttpResponseRedirect(reverse('price:table'))
        elif 'add_product' in request.POST:
            product_form = AddProductForm(user, request.POST, request.FILES)
            if product_form.is_valid():
                product_form.save()
                return HttpResponseRedirect(reverse('price:table'))
        elif 'add_shop' in request.POST:
            shop_form = AddShopForm(user, request.POST, request.FILES)
            if shop_form.is_valid():
                shop_form.save()
                return HttpResponseRedirect(reverse('price:table'))
        else:
            product_user_form = AddProductToUserForm(user)
            shop_user_form = AddShopToUserForm(user)
            product_form = AddProductForm(user)
            shop_form = AddShopForm(user)
    else:
        product_user_form = AddProductToUserForm(user)
        shop_user_form = AddShopToUserForm(user)
        product_form = AddProductForm(user)
        shop_form = AddShopForm(user)
    user_shops = user.shops.all().order_by('name')
    count_of_shops = len(user_shops)
    user_products = user.products.all().order_by('name')
    prices = Price.objects.filter(product__user=user)
    context = {
        'title': 'Таблица цен',
        'user_shops': user_shops,
        'len': count_of_shops,
        'user_products': user_products,
        'product_user_form': product_user_form,
        'shop_user_form': shop_user_form,
        'product_form': product_form,
        'shop_form': shop_form,
        'prices': prices
    }
    return render(request, 'price/table.html', context)

def user_table(request, username):
    user = User.objects.get(username=username)
    user_shops = user.shops.all().order_by('name')
    count_of_shops = len(user_shops)
    user_products = user.products.all().order_by('name')
    prices = Price.objects.filter(product__user=user)

    context = {
        'title': 'Таблица цен',
        'username': username,
        'user_shops': user_shops,
        'len': count_of_shops,
        'user_products': user_products,
        'prices': prices
    }
    return render(request, 'price/user_table.html', context)

def delete_user_product(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        product_id = request.POST.get('product_id')
        User_Product.objects.get(user_id = user_id, product_id = product_id).delete()
    return HttpResponseRedirect(reverse('price:table'))

def delete_user_shop(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        shop_id = request.POST.get('shop_id')
        User_Shop.objects.get(user_id = user_id, shop_id = shop_id).delete()
    return HttpResponseRedirect(reverse('price:table'))

def update_price(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        product_id = request.POST.get('product_id')
        shop_id = request.POST.get('shop_id')
        price_value = request.POST.get('price')
        user_product = User_Product.objects.get(user_id=user_id, product_id=product_id)
        user_shop = User_Shop.objects.get(user_id=user_id, shop_id=shop_id)
        price, created = Price.objects.get_or_create(product = user_product, shop = user_shop)
        if price_value:
            price.price = price_value
            price.save()
        else:
            Price.objects.get(product=user_product, shop=user_shop).delete()
    return HttpResponseRedirect(reverse('price:table'))

def other_tables(request):
    current_user = request.user
    user_list = User.objects.filter(private=False).order_by('first_name', 'last_name')
        # .exclude(id=current_user.id)
    context = {'title': 'Другие пользователи', 'user_list': user_list}
    return render(request, 'price/other_tables.html', context)

def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('price:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {'title': 'Личный кабинет', 'form': form, 'cities': City.objects.all()}
    return render(request, 'price/profile.html', context)