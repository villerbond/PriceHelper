from django import forms
from .models import Product, Shop, Category, Price, Basket
from users.models import User_Product, User_Shop
from django.db.models import Q

class AddProductToUserForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(AddProductToUserForm, self).__init__(*args, **kwargs)
        self.user = user
        available_products = Product.objects.filter(Q(author__isnull=True) | Q(author=self.user)).exclude(user_product__user=user)
        self.fields['product'] = forms.ModelChoiceField(queryset=available_products.order_by('name'))

    def save(self):
        User_Product.objects.create(user = self.user, product = self.cleaned_data['product'])

class AddShopToUserForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(AddShopToUserForm, self).__init__(*args, **kwargs)
        self.user = user
        available_shops = Shop.objects.filter(Q(author__isnull=True) | Q(author=self.user)).exclude(user_shop__user=user)
        self.fields['shop'] = forms.ModelChoiceField(queryset=available_shops.order_by('name'))

    def save(self):
        User_Shop.objects.create(user = self.user, shop = self.cleaned_data['shop'])

class AddProductForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Введите название продукта'
        }))
        self.fields['icon'] = forms.ImageField()
        self.fields['category'] = forms.ModelChoiceField(queryset=Category.objects.all())

    def save(self):
        if self.user.is_superuser:
            Product.objects.create(name = self.data['name'], icon = self.cleaned_data['icon'], category = self.cleaned_data['category'])
        else:
            Product.objects.create(name = self.data['name'], icon = self.cleaned_data['icon'], category = self.cleaned_data['category'], author = self.user)

class AddShopForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(AddShopForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Введите название магазина'
        }))
        self.fields['icon'] = forms.ImageField(widget=forms.FileInput(), required=False)
        self.fields['adress'] = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Введите адрес магазина'
        }), required=False)

    def save(self):
        Shop.objects.create(name = self.data['name'], icon = self.cleaned_data['icon'], adress = self.data['adress'], author = self.user)

class UserProductChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.product.name

class AddUserProductToBasket(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(AddUserProductToBasket, self).__init__(*args, **kwargs)
        existing_products = Basket.objects.filter(user_product__user = user).values_list('user_product__product_id', flat=True)
        user_products = User_Product.objects.filter(user = user).exclude(product_id__in=existing_products)
        self.fields['user_product'] = UserProductChoiceField(queryset=user_products.order_by('product__name'))
        self.fields['count'] = forms.IntegerField(min_value=1)
        # self.fields['count'] = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)])

    def save(self):
        Basket.objects.create(user_product = self.cleaned_data['user_product'], count = self.data['count'])

class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = ['price']