"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from shop import views
app_name='shop'

urlpatterns = [
    path('',views.allcategories,name='categories'),
    path('product/<int:p>',views.allproducts,name='product'),
    path('details/<int:p>',views.details,name='details'),
    path('register/', views.register, name="register"),
    path('login', views.user_login, name="login"),
    path('logout', views.user_logout,name="logout"),
    path('add_categories', views.add_categories,name="add_categories"),
    path('add_product', views.add_product,name="add_product"),
    path('add_stock/<int:p>', views.add_stock, name="add_stock"),

]
