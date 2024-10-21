from django.contrib import admin
from django.urls import path
from AppUM import views

urlpatterns = [
     path('', views.login,name="Inicio"),
]