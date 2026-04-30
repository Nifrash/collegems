from django.urls import path
from . import views

urlpatterns = [
    path('redirect/', views.dashboard_redirect, name='dashboard_redirect'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('staffs/', views.student_dashboard, name='staff_dashboard'),
    path('lecturer/', views.lecturer_dashboard, name='lecturer_dashboard'),
    path('students/', views.student_dashboard, name='student_dashboard'),

]