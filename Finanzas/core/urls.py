from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('dahsboard/', Dashboard , name="dash"),
    path('registro/', registro , name="Save"),
    
]
