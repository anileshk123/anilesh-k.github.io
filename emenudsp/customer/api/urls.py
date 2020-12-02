from django.urls import path        
from . import views


urlpatterns = [
    path('cart/', views.myCart.as_view(), name="myCart"),    
]