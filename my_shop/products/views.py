from django.shortcuts import render
from products.models import Product, Category
from card.cart import HybridCart

def product_list(request):
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    
    products = Product.objects.filter(
        available=True
    ).select_related(
        'category'
    ).prefetch_related('poductimage_set')
        
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    if search_query:
        products = products.filter(name__icontains=search_query)
        
    categories = Category.objects.all()
    cart = HybridCart(request)
    
    return render(request, 'stors/prodli.html', {
        'products': products,
        'categories': categories,
        'cart': cart
    })