from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from users.models import User, City, User_Product, User_Shop
from price.models import Price, Basket, Product, Shop

# Create your views here.

from users.forms import UserProfileForm
from price.forms import AddProductToUserForm, AddShopToUserForm, AddProductForm, AddShopForm, PriceForm, AddUserProductToBasket

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
    count_of_products = len(user_products)
    prices = Price.objects.filter(product__user=user)
    if count_of_shops == 0 and count_of_products == 0:
        is_empty = True
    else:
        is_empty = False

    context = {
        'title': 'Таблица цен',
        'username': username,
        'user_shops': user_shops,
        'len': count_of_shops,
        'user_products': user_products,
        'prices': prices,
        'is_empty': is_empty
    }
    return render(request, 'price/user_table.html', context)

def import_table(request, username):
    imp_user = User.objects.get(username=username)
    curr_user = request.user

    User_Product.objects.filter(user=curr_user).delete()
    User_Shop.objects.filter(user=curr_user).delete()
    imp_products = User_Product.objects.filter(user=imp_user)
    imp_shops = User_Shop.objects.filter(user=imp_user)
    imp_prices = Price.objects.filter(product__user=imp_user)

    for product in imp_products:
        if product.product.author:
            Product.objects.create(name=product.product.name, icon=product.product.icon, category=product.product.category, author=curr_user)
        User_Product.objects.create(user=curr_user, product=product.product)

    for shop in imp_shops:
        if shop.shop.author:
            Shop.objects.create(name=shop.shop.name, icon=shop.shop.icon, adress=shop.shop.adress, author=curr_user)
        User_Shop.objects.create(user=curr_user, shop=shop.shop, difficulty=shop.difficulty)

    for price in imp_prices:
        print(price.product.product)
        print(price.shop.shop)
        new_user_product = User_Product.objects.get(user=curr_user, product=price.product.product)
        new_user_shop = User_Shop.objects.get(user=curr_user, shop=price.shop.shop)
        Price.objects.create(product=new_user_product, shop=new_user_shop, price=price.price)

    return HttpResponseRedirect(reverse('price:table'))

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

class ShopChoice:
    def __init__(self, product, shop, price):
        self.product = product
        self.shop = shop
        self.price = price

    def __str__(self):
        return str(self.product) + ' ' + self.shop + ' ' + str(self.price)

def basket(request):
    user = request.user
    user_products = User_Product.objects.filter(user=user)
    added_products = Basket.objects.filter(user_product__in = user_products)
    best_prices = []
    result = None
    if request.method == 'POST':
        if 'add_product_to_user' in request.POST:
            basket_form = AddUserProductToBasket(user, request.POST)
            if basket_form.is_valid():
                basket_form.save()
                return HttpResponseRedirect(reverse('price:basket'))
        elif 'best_prices' in request.POST:
            difficulty = request.POST.get('difficulty')

            for product in added_products:
                best_prices.append(ShopChoice(str(product), 'Пятерочка', 100))

            for i in range(len(best_prices)):
                print(best_prices[i])

            result = difficulty

    basket_form = AddUserProductToBasket(user)
    context = {
        'user': user,
        'basket_form': basket_form,
        'added_products': added_products,
        'best_prices': best_prices,
        'result': result
    }
    return render(request, 'price/basket.html', context)

# def best_prices(request):
#     return HttpResponseRedirect(reverse('price:basket'))

def delete_product_basket(request):
    if request.method == 'POST':
        added_product_id = request.POST.get('added_product_id')
        Basket.objects.get(id=added_product_id).delete()
    return HttpResponseRedirect(reverse('price:basket'))
