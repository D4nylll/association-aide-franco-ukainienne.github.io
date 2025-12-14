from django.shortcuts import render, redirect
from card.models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from card.cart import HybridCart

@login_required
def checkout(request):
    cart = HybridCart(request)
    if len(cart) == 0:
        return redirect('product_list')

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email')
        )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
        cart.clear() 
        return redirect('payment', order_id=order.id)
        
    return render(request, 'stors/checkout.html', {'cart': cart})