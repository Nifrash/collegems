from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.student_create, name='student_create'),
    path('profile/', views.student_detail, name='student_detail'),
    path('update/', views.student_update, name='student_update'),
    path('delete/', views.student_delete, name='student_delete'),
]