"""
In this file we implement API for users
"""
from django.urls import path
from app.user import views

urlpatterns = [
    # API for user
    path('login/', views.LoginView.as_view()),
    path('user/', views.UserView.as_view()),
    path('stadium/', views.StadiumView.as_view()),
    path('court/', views.CourtView.as_view()),
    path('duration/', views.DurationView.as_view()),
    path('reserve/', views.ReserveView.as_view()),
    path('comment/', views.CommentView.as_view()),
    path('commentimage/', views.CommentImageView.as_view()),
]
