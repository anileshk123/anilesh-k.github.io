from django.shortcuts import render
from .models import menu
# Create your views here.

def index(request): 

    emenu = menu.objects.all()

    return render(request, 'index.html', { 'emenu' : emenu})