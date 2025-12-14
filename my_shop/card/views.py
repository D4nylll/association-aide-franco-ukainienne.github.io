from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from products.models import Product, Category, PoductImage
from card.models import Order, OrderItem
from card.cart import HybridCart
from django.db.models import Q
from payment.utils import get_liqpay_context
from users.forms import UserRegistrationForm


@require_POST
def cart_add(request, product_id):
    cart = HybridCart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    messages.success(request, "Товар добавлен в корзину!")
    return redirect('product_list')


def cart_remove(request, product_id):
    cart = HybridCart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = HybridCart(request)
    
    cart_product_ids = [item['product'].id for item in cart]
    cart_categories = Product.objects.filter(id__in=cart_product_ids).values_list('category', flat=True)
    
    
    recommendations = Product.objects.filter(
        category__in=cart_categories,
        available=True
    ).exclude(id__in=cart_product_ids).order_by('?')[:4]
    
    return render(request, 'stors/cart_d.html', {
        'cart': cart,
        'recommendations': recommendations
    })



def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    liqpay_context = get_liqpay_context(order) 
    
    return render(request, 'stors/payment.html', {
        'order': order,
        'liqpay_data': liqpay_context['data'],
        'liqpay_signature': liqpay_context['signature']
    })