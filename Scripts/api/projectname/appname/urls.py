from django.urls import path
from .views import ItemListCreateView, ItemDetailView
from . import views

urlpatterns = [
    path('items/', ItemListCreateView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('', views.index, name='index'),
]
