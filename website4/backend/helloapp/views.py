from django.shortcuts import render, redirect
from django.views import generic
import os
import pymongo
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from .forms import UserForm
import bcrypt
from .forms import LoginForm
from .forms import UserProfileForm
from django.http import HttpResponse



def homepage(request):
    print("Hello world") 
    return HttpResponse()


