from django.urls import path
from .views import iniciar_simulado, corrigir_simulado, historico
from . import views


app_name = 'questoes'

urlpatterns = [
    path('menu/', views.menu_simulado, name='menu_simulado'),
    path('iniciar/', views.iniciar_simulado, name='iniciar_simulado'),
    path('corrigir/<int:prova_id>/', views.corrigir_simulado, name='corrigir_simulado'),
    path("correcao/<int:tentativa_id>/", views.correcao, name="correcao"),
    path('historico/', historico, name='historico'),
]
