from django.contrib import admin
from django.urls import path
from AppUM import views

urlpatterns = [
     path('login', views.vista_login,name="Login"),
     path('login_validacion', views.validacion_login,name="LoginValidacion"),
]