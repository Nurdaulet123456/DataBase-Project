from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('products/', views.search, name='products'),
    path('delete/<str:name>/', views.change_consultant, name='delete'),
    path('editDisc/', views.edit_discounts, name='edit_discounts'),
]