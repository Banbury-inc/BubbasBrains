from rest_framework import generics
from .models import Item
from .serializers import ItemSerializer
from django.http import JsonResponse
import sys
import os
from django.shortcuts import render

class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
def index(request):
    return render(request, 'Manual_Control_dev.html')
def test(request):
    response = "Hello World"
    return JsonResponse({'result' : response})
