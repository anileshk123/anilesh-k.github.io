from rest_framework import serializers
from core.models import *
class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'quantity']