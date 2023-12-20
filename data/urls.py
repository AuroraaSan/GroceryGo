"""data URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from .views import home
from . import views
from django.urls import path, include, re_path



urlpatterns = [
    path('', RedirectView.as_view(url='http://127.0.0.1:8000/shop/', permanent=False)),
    #path('account/', views.account_details, name='account_details'),
    path('home/', home, name='home'),
    path("admin/", admin.site.urls),
    path('account/', include('account.urls')),
    re_path(r'^account/account/$', RedirectView.as_view(url='/account/', permanent=True)),
    path('orders/', include('orders.urls', namespace='orders')),
    path("shop/", include("shop.urls", namespace='shop')),
    path("cart/", include("cart.urls", namespace="cart")),
]
