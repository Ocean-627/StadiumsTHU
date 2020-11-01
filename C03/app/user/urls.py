from django.urls import path
from app.user import views

urlpatterns = [
    # API for user
    path('logon/', views.logon),
    path('login/', views.login),
    path('logout/', views.logout),
]