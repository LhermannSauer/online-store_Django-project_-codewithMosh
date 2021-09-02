from django.shortcuts import render
from .models import Product
from rest_framework import viewsets, permissions
from .serializers import ProductSerializer
# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows users to be viewed or edited'''
    queryset = Product.objects.all().order_by('title')
    serializer_class = ProductSerializer
