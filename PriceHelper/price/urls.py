"""PriceHelper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from price.views import table, other_tables, profile, delete_user_product, delete_user_shop, update_price

app_name = 'price'

urlpatterns = [
    path('table/', table, name='table'),
    path('other_tables/', other_tables, name='other_tables'),
    path('profile/', profile, name='profile'),
    path('delete_user_product/', delete_user_product, name='delete_user_product'),
    path('delete_user_shop/', delete_user_shop, name='delete_user_shop'),
    path('update_price/', update_price, name='update_price')
]