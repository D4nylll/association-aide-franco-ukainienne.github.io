from django.conf import settings
from .models import Product, CartItem

class HybridCart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        self.user = request.user
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        
        if self.user.is_authenticated:
            item, created = CartItem.objects.get_or_create(user=self.user, product=product)
            if update_quantity:
                item.quantity = quantity
            else:
                item.quantity += quantity
            item.save()
        else:
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
            
            if update_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
            self.save_session()

    def save_session(self):
        self.session.modified = True

    def remove(self, product):
        if self.user.is_authenticated:
            CartItem.objects.filter(user=self.user, product=product).delete()
        else:
            product_id = str(product.id)
            if product_id in self.cart:
                del self.cart[product_id]
                self.save_session()

    def __iter__(self):
        if self.user.is_authenticated:
            items = CartItem.objects.filter(user=self.user)
            for item in items:
                yield {
                    'product': item.product,
                    'price': item.product.price,
                    'quantity': item.quantity,
                    'total_price': item.get_cost()
                }
        else:
            product_ids = self.cart.keys()
            products = Product.objects.filter(id__in=product_ids)
            cart_copy = self.cart.copy()
            for product in products:
                cart_copy[str(product.id)]['product'] = product
            
            for item in cart_copy.values():
                item['price'] = float(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

    def __len__(self):
        if self.user.is_authenticated:
            return sum(item.quantity for item in CartItem.objects.filter(user=self.user))
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        if self.user.is_authenticated:
            return sum(item.get_cost() for item in CartItem.objects.filter(user=self.user))
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        if self.user.is_authenticated:
            CartItem.objects.filter(user=self.user).delete()
        else:
            del self.session[settings.CART_SESSION_ID]
            self.save_session()

    def merge_session_cart_to_db(self, user):
        if not self.cart:
            return
            
        for product_id, item_data in self.cart.items():
            try:
                product = Product.objects.get(id=product_id)
                db_item, created = CartItem.objects.get_or_create(
                    user=user, product=product,
                    defaults={'quantity': 0}
                )
                db_item.quantity += item_data['quantity']
                db_item.save()
            except Product.DoesNotExist:
                continue
        
        self.cart = {}
        del self.session[settings.CART_SESSION_ID]
        self.save_session()