from rest_framework import generics
from .models import Item
from .serializers import ItemSerializer
from django.http import JsonResponse
import sys
import os
from django.shortcuts import render
import get_system_info
from adafruit_servokit import ServoKit
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
def getSystemInfo(request):
    response = get_system_info.get_device_name()
    return JsonResponse({'result' : response})
def initialize(request):
    print("Initializing Arm")
    kit = ServoKit(channels=16)
    elbowangle = 90
    wristangle = 90
    shoulderangle = 90
    kit.servo[4].angle = shoulderangle
    kit.servo[2].angle = elbowangle
    kit.servo[3].angle = wristangle
def moveShoulderUp(request):
    print("Initializing Arm")
    kit = ServoKit(channels=16)
    elbowangle = 30
    wristangle = 30
    shoulderangle = 30
    kit.servo[4].angle = shoulderangle
    kit.servo[2].angle = elbowangle
    kit.servo[3].angle = wristangle
 
