from django.contrib import admin
from django.urls import path
from Inicio import views

urlpatterns = [
    path('',views.loginTemplate,name="Login")
]