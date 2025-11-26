from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('principal/', views.principal_view, name='principal'),
    path('notas/', views.notas_view, name='notas'),
    path('conteudos/', views.conteudos_view, name='conteudos'),
    path('exercicios/', views.exercicios_view, name='exercicios'),
]
