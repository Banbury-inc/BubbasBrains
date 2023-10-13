from rest_framework import generics
from .models import Item
from .serializers import ItemSerializer
from django.http import JsonResponse
import sys
from django.shortcuts import render
sys.path.append('/home/mmills/Documents/Repositories/BubbasBrains/Scripts')
import Scripts.get_system_info
sys.path.append('/home/mmills/Documents/Repositories/BubbasBrains/Motor_Control/Arm')
import armControl

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
def system_info(request):
    response = get_system_info.SystemInfo.get_device_name() 
    return JsonResponse({'result' : response})
def initialize(request):
    response = armControl.initialize() 
    return JsonResponse({'result' : response})
