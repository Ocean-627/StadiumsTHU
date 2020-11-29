"""
In this file we implement API for managers
"""
from django.urls import path
from app.manager import views

urlpatterns = [
    # API for manager
    path('logon/', views.LogonView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('stadium/', views.StadiumView.as_view()),
    path('court/', views.CourtView.as_view()),
    path('reserveevent/', views.ReserveEventView.as_view()),
    path('changeduration/', views.ChangeDurationView.as_view()),
    path('addevent/', views.AddEventView.as_view()),
    path('user/', views.UserView.as_view()),
    path('history/', views.HistoryView.as_view()),
    # path('revoke/', views.revoke)
]

