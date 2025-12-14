from django.shortcuts import render, get_object_or_404
from payment.utils import get_liqpay_context
from card.models import Order


def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    liqpay_context = get_liqpay_context(order) 
    
    return render(request, 'stors/payment.html', {
        'order': order,
        'liqpay_data': liqpay_context['data'],
        'liqpay_signature': liqpay_context['signature']
    })
