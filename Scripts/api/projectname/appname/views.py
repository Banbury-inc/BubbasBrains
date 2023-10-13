from rest_framework import generics
from .models import Item
from .serializers import ItemSerializer
from django.http import JsonResponse
import sys
import os
from django.shortcuts import render
sys.path.append('/home/mmills/Documents/Repositories/BubbasBrains/Scripts')
import get_system_info

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

    # Get the directory where my_module.py is located
    module_dir = os.path.dirname(os.path.abspath('/home/mmills/Documents/Repositories/BubbasBrains/Scripts'))

    # Add the directory to sys.path
    sys.path.append(module_dir)

    # Now, you can import and use the function from my_module
    response = get_system_info.get_device_name()

    return JsonResponse({'result' : response})
