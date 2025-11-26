from django.urls import path
from .views import iniciar_simulado, corrigir_simulado, historico
from . import views

app_name = 'questoes'

urlpatterns = [
    path('simulado/', iniciar_simulado, name='simulado'),
    path("correcao/<int:tentativa_id>/", views.correcao, name="correcao"),
    path("corrigir/", views.corrigir_simulado, name="corrigir"),
    path('hsitorico/', historico, name='historico'),
]    
