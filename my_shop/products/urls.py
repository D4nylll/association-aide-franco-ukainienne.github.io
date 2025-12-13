
from django.urls import path
from django.contrib.auth import views as auth_views
from products import views


urlpatterns = [
    path('products/', views.product_list, name='product_list'),
] 

