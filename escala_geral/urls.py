from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'Escala'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('configuracoes/', views.Configuracoes.as_view(),name="Configurações"),
    path('configuracoes/horarios/', views.ConfigurarHorarios.as_view(),name="Configurar Horários"),

]

