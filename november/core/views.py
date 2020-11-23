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
