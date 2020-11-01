"""
In this file we implement API for managers
"""
from django.urls import path
from app.manager import views

urlpatterns = [
    # API for manager
    path('logon/', views.logon),
    path('login/', views.login),
    path('logout/', views.logout),
]
