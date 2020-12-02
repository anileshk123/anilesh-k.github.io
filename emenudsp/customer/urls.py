from django.urls import path        
from . import views

app_name = "customer"

urlpatterns = [
    path('', views.Index , name= 'index'),
    path('cart/', views.Cart , name= 'cart'),
    path('addtocart', views.addToCart , name= 'addToCart'),
    
]