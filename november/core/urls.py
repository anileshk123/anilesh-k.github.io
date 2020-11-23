from django.urls import path        
from . import views


app_name = "core"
urlpatterns = [
    
    path('', views.index , name= 'index'),
    path('qrcode/add', views.addQrcode , name= 'addQrcode'),
    path('qrcode/', views.listQrcode , name= 'listQrcode'),
    
]