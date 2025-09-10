from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('apply/', views.apply, name='apply'),
    path(
        'submit_application/',
        views.submit_application,
        name='submit_application'
    ),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path(
        'export_applicants/',
        views.export_applicants,
        name='export_applicants'
    ),
]
