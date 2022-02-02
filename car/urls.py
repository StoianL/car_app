from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_car/', views.add_car, name='add_car'),
    path('list_car/', views.list_car, name='list_car'),
    path('list_repair/', views.list_repair, name='list_repair'),
    path('add_brand/', views.add_brand, name='add_brand'),
    path('<int:pk>/', views.detail_car, name='detail_car'),
    path('edit_repair/<int:pk>/', views.edit_repair, name='edit_repair'),
]
