import base64
import hashlib
import json
from django.conf import settings

def get_liqpay_context(order):
    public_key = settings.LIQPAY_PUBLIC_KEY
    private_key = settings.LIQPAY_PRIVATE_KEY
    
    params = {
        'action': 'pay',
        'amount': str(order.get_total_cost),
        'currency': 'UAH',
        'description': f'Оплата заказа №{order.id}',
        'order_id': str(order.id),
        'version': '3',
        'public_key': public_key,
        'result_url': 'http://127.0.0.1:8000/payment/success/', 
        'server_url': 'http://127.0.0.1:8000/payment/callback/', 
    }
    
    json_data = json.dumps(params)
    data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
    
    sign_str = private_key + data + private_key
    signature = base64.b64encode(hashlib.sha1(sign_str.encode('utf-8')).digest()).decode('utf-8')
    
    return {'data': data, 'signature': signature}