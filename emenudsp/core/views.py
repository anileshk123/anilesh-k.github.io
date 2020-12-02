from django.shortcuts import render,redirect,reverse
from .models import *
import random, string
from django.contrib import messages
 
# Create your views here.

def index(request): 

    return render(request, 'core/dashboard.html')

def addQrcode(request):
    if request.method == 'POST': 
        qr_code = QRCode()
        qr_code.name = request.POST['name']
        qr_code.description = request.POST['description']
        qr_code.qr_code_id = ''.join(random.choice(string.ascii_lowercase + string.digits) for each in range(8))
        qr_code.save()
        qr_code.generate_qrcode()
        messages.success(request, 'Table successfully Created')
        return redirect(reverse('core:listQrcode'))
    
    return render(request, 'core/addQrcode.html')

def listQrcode(request):
    qrcode = QRCode.objects.all()
    context = {
        'data' : qrcode
    }
    return render(request, 'core/listQrcode.html', context)

def addCategory(request):
    if request.method == 'POST':
        category = Category()
        category.name = request.POST['name']
        category.description = request.POST['description']
        category.save()
        messages.success(request, 'Category successfully Created')
        return redirect(reverse('core:listCategory'))
    
    return render(request, 'core/addCategory.html')

def listCategory(request):
    category = Category.objects.all()
    context = {
        'data' : category
    }
    return render(request, 'core/listCategory.html', context)

def addMenuItem(request):
    if request.method == 'POST':
        item = MenuItem()
        item.name = request.POST['name']
        item.price = request.POST['price']
        item.category = Category.objects.get(id=request.POST['category'])   
        item.description = request.POST['description']
        item.save()
        if request.FILES.getlist('media'):
            for media in request.FILES.getlist('media'):
                media_object = Media()
                media_object.type = 'Image'
                media_object.file = media
                media_object.save()
                item.media.add(media_object)
                item.save()
        messages.success(request, 'Item successfully Created')
        return redirect(reverse('core:listMenuItem'))
    category = Category.objects.all()
    context = {
        'data' : category
    }
    return render(request, 'core/addMenuItem.html', context)


def listMenuItem(request):
    item = MenuItem.objects.all()
    context = {
        'data' : item
    }
    return render(request, 'core/listMenuItem.html', context)