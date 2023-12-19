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
    user_shops = User_Shop.objects.filter(user=user)
    # user_shops = user.shops.all().order_by('name')
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
        comment = request.POST.get('comment')
        user_product = User_Product.objects.get(user_id=user_id, product_id=product_id)
        user_shop = User_Shop.objects.get(user_id=user_id, shop_id=shop_id)
        price, created = Price.objects.get_or_create(product = user_product, shop = user_shop)
        if price_value:
            price.price = float(price_value.replace(",", "."))
            price.comment = comment
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
        return str(self.product) + ' ' + str(self.shop) + ' ' + str(self.price)

    def diff(self):
        if self.shop == 'Нет магазина':
            return 0
        return self.shop.difficulty

class ShopsChoice:
    def __init__(self):
        self.data = []

    def append(self, shop_choice):
        return self.data.append(shop_choice)

    def total_difficulty(self):
        sum = 0
        added_shops = []
        for el in self.data:
            if el.shop in added_shops:
                continue
            else:
                sum += el.diff()
                added_shops.append(el.shop)
        return sum

    def count_of_shops(self):
        count = 0
        added_shops = []
        for el in self.data:
            if el.shop in added_shops:
                continue
            else:
                count += 1
                added_shops.append(el.shop)
        return count

    def total_price(self):
        sum = 0
        for el in self.data:
            sum += el.price
        return sum

    def have(self, shop):
        for el in self.data:
            if el.shop == shop:
                return True
        return False

    def is_not_full(self):
        for el in self.data:
            if el.shop == 'Нет магазина':
                return True
        return False

    def len(self):
        return len(self.data)

def get_best_choice(added_products, user_shops):
    best_prices = ShopsChoice()
    full_prices = True

    for product in added_products:
        prod_to_add = product
        price_to_add = -1
        for shop in user_shops:
            curr_price = Price.objects.filter(shop=shop, product=product.user_product)
            if curr_price.exists():
                if price_to_add < 0:
                    shop_to_add = shop
                    price_to_add = curr_price.first().price
                else:
                    if curr_price.first().price < price_to_add:
                        shop_to_add = shop
                        price_to_add = curr_price.first().price
                    elif curr_price.first().price == price_to_add:
                        if best_prices.have(shop):
                            shop_to_add = shop
                            price_to_add = curr_price.first().price
        if price_to_add < 0:
            full_prices = False
            best_prices.append(ShopChoice(prod_to_add, 'Нет магазина', 0))
        else:
            best_prices.append(ShopChoice(prod_to_add, shop_to_add, price_to_add * product.count))

    return best_prices, full_prices

def basket(request):
    user = request.user
    user_products = User_Product.objects.filter(user=user)
    added_products = Basket.objects.filter(user_product__in = user_products)
    best_prices = ShopsChoice()
    total_diff = 0
    total_sum = 0
    is_result = False
    is_shops = True
    exist_full_prices = False

    if request.method == 'POST':
        if 'add_product_to_user' in request.POST:
            basket_form = AddUserProductToBasket(user, request.POST)
            if basket_form.is_valid():
                basket_form.save()
                return HttpResponseRedirect(reverse('price:basket'))
        elif 'best_prices' in request.POST:
            difficulty = request.POST.get('difficulty')
            user_shops = User_Shop.objects.filter(user=user)

            if difficulty:
                from itertools import combinations
                result = []
                for r in range(1, len(user_shops) + 1):
                    for combo in combinations(user_shops, r):
                        if sum(shop.difficulty for shop in combo) <= int(difficulty):
                            result.append(list(combo))

                min_price = -1
                for shops in result:
                    temp, full_prices = get_best_choice(added_products, shops)
                    if not full_prices:
                        if exist_full_prices:
                            continue
                    else:
                        exist_full_prices = True
                    temp_price = temp.total_price()
                    if min_price < 0 or (best_prices.is_not_full()):
                        if min_price < 0:
                            best_prices = temp
                            min_price = temp_price
                        if temp.is_not_full():
                            if temp.total_price() < best_prices.total_price():
                                best_prices = temp
                                min_price = temp_price
                            elif temp.total_price() == best_prices.total_price():
                                if temp.total_difficulty() < best_prices.total_difficulty():
                                    best_prices = temp
                                    min_price = temp_price
                        else:
                            best_prices = temp
                            min_price = temp_price
                    else:
                        if temp_price < min_price:
                            best_prices = temp
                            min_price = temp_price
                        elif temp_price == min_price:
                            if best_prices.total_difficulty() < temp.total_difficulty():
                                continue
                            elif best_prices.total_difficulty() == temp.total_difficulty():
                                if temp.count_of_shops() < best_prices.count_of_shops():
                                    best_prices = temp
                                    min_price = temp_price
                            else:
                                best_prices = temp
                                min_price = temp_price
            else:
                best_prices, full_prices = get_best_choice(added_products, user_shops)

            if best_prices.count_of_shops() == 0:
                is_shops = False

            total_diff = best_prices.total_difficulty()
            total_sum = best_prices.total_price()
            is_result = True

    basket_form = AddUserProductToBasket(user)
    context = {
        'title': 'Корзина',
        'user': user,
        'basket_form': basket_form,
        'added_products': added_products,
        'best_prices': best_prices,
        'total_diff': total_diff,
        'total_sum': total_sum,
        'is_result': is_result,
        'is_shops': is_shops
    }
    return render(request, 'price/basket.html', context)

def delete_product_basket(request):
    if request.method == 'POST':
        added_product_id = request.POST.get('added_product_id')
        Basket.objects.get(id=added_product_id).delete()
    return HttpResponseRedirect(reverse('price:basket'))
