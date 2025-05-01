
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index ,name ='index'),  # Root path
    path('dashboard/', views.student_dashboard, name='student_dashboard'),

    ]
