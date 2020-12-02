from django.urls import path        
from . import views


app_name = "core"
urlpatterns = [
    
    path('', views.index , name= 'index'),
    path('qrcode/add', views.addQrcode , name= 'addQrcode'),
    path('qrcode/', views.listQrcode , name= 'listQrcode'),
    path('category/add', views.addCategory , name= 'addCategory'),
    path('category/', views.listCategory , name= 'listCategory'),
    path('menuitem/add', views.addMenuItem , name= 'addMenuItem'),
    path('menuitem/', views.listMenuItem , name= 'listMenuItem'),
    
]