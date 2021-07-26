from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path('', views.index),

    path('user/', views.user),  # Para debug
    path('api/section/<int:id>', views.section),

    path('user/login/', views.user_login),
    path('user/logout/', views.user_logout),
    path('user/register/', views.user_register),

    path('quiz/play/', views.quiz_play),
    path('quiz/result/<int:question_answered_pk>', views.quiz_result),
]
