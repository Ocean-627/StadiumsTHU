"""
In this file we implement API for users
"""
from django.urls import path
from app.user import views

urlpatterns = [
    # API for user
    path('logon/', views.logon),
    path('login/', views.login),
    path('logout/', views.logout),
    path('stadium/', views.get_stadiums),
    path('court/', views.get_courts),
    path('court/reserve/', views.get_durations),
    path('reserve/', views.reserve),
]