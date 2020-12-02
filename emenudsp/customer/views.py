from django.shortcuts import render
from .models import menu
from core.models import *
from django.http import JsonResponse
# Create your views here.

def Index(request): 
    emenu = MenuItem.objects.filter(is_active = True).order_by('-id')[:10]
    category = Category.objects.all()
    return render(request, 'index.html', { 'emenu' : emenu , 'category' : category})

def Cart(request): 
    cart = Cart.objects.all()
    emenu = MenuItem.objects.filter(is_active = True).order_by('-id')[:10]
    category = Category.objects.all()
    return render(request, 'cart.html', { 'emenu' : emenu , 'category' : category})

def addToCart(request):
    
    cart = Cart()
    print('hiiiiiiiiiiiiiiiiii')
    cart.qr_code = QRCode.objects.get(qr_code_id="hjws5tbp")
    cart.menu_item = MenuItem.objects.get(id=request.GET.get('menuitem', None))
    cart.save()
    data = {
    'data': "success"# User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)