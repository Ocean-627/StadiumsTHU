"""
In this file we implement API for users
"""
from django.urls import path
from app.user import views

urlpatterns = [
    # API for user
    path('logon/', views.LogonView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('stadium/', views.StadiumView.as_view()),
    path('court/', views.CourtView.as_view()),
    path('duration/', views.DurationView.as_view()),
    path('reserve/', views.ReserveView.as_view()),
]
