from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from card.cart import HybridCart

@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs):
    cart = HybridCart(request)
    cart.merge_session_cart_to_db(user)