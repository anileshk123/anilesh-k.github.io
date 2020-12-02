from django.shortcuts import render, redirect, reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_401_UNAUTHORIZED,
    HTTP_201_CREATED
)
from rest_framework import generics
from core.models import *
from customer.api.serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
# Create your views here.

today = datetime.date.today()

@api_view(["POST"])
def addToCart(request):
    return Response({"response": "Rating successfully"}, status=200)
    #if request.method == 'POST':
        # cart = Cart()
        # print('hiiiiiiiiiiiiiiiiii')
        # cart.qr_code = QRCode.objects.get(qr_code_id="hjws5tbp")
        # cart.menu_item = MenuItem.objects.get(id=request.POST['menu'])
        # cart.save()
        # return redirect(reverse('customer:index'))
    
class myCart(APIView):
    def post(self, request):
        if request.data:
            serializer = AddToCartSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            try:
                qr_code = QRCode.objects.get(qr_code_id=request.data['qr_code'])
                menuitem = MenuItem.objects.get(id=request.data['menuitem'])
                if Cart.objects.filter(qr_code = qr_code, menu_item = menuitem, is_active=True).exists():
                    cart = Cart.objects.get(qr_code=qr_code, menu_item = menuitem, is_active=True)
                    qty = cart.quantity
                    cart.quantity = qty + int(request.data['quantity'])
                    cart.date_updated = today
                    cart.save()
                    
                else:
                    serializer.save(qr_code=qr_code, menu_item=menuitem)
                    
                return Response({'status':HTTP_201_CREATED,"data":[],'message':'Added to bag'})
            except:
                return Response({'status':HTTP_400_BAD_REQUEST,'data':[],"message":"Incorrect QR Code or Menu"})
        else:
            return Response({'status':HTTP_500_INTERNAL_SERVER_ERROR,'data':[],"message":"Something went wrong. Please try again later"})

    def get(self, request, qrcode_id=None):
        if qrcode_id == None:
            return Response({'status':HTTP_403_FORBIDDEN,'data':[],"message": "QR Code id not present"})

        elif len(qrcode_id) <= 0:
            return Response({'status':HTTP_401_UNAUTHORIZED,'data':[],"message": "Invalid QR Code"})

        elif len(qrcode_id) >= 0:
            try:
                qr_object = QRCode.objects.get(qr_code_id=qrcode_id)
                cart = Cart.objects.filter(is_active=True,qr_code=qr_object).order_by('id')
                if cart.exists():
                    serializer = ListCartSerializer(cart, many=True, context={"request": request})
                    return Response({'status':HTTP_200_OK,"data": serializer.data,'message':'OK'})
                else:
                    return Response({'status':HTTP_404_NOT_FOUND,'data':[],"message": "No data"}, )
            except:
                return Response({'status':HTTP_400_BAD_REQUEST,'data':[],"message":"Incorrect QR Code "})

        else:
            return Response({'status':HTTP_500_INTERNAL_SERVER_ERROR,'data':[],"message":"Something went wrong. Please try again later"})