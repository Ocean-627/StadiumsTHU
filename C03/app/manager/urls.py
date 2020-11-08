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
    path('court/', views.get_court),
    path('court/reserve/', views.get_court_reserve),
    path('change/', views.change_duration),
    path('event/', views.add_event),
    path('users/', views.get_users),
    path('history/', views.get_history),
    path('get/change/', views.get_detail_change),
    path('get/event/', views.get_detail_event),
    # path('revoke/', views.revoke)
]
