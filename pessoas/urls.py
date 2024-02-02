from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'Pessoas'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('colaboradores/', views.CoalboradoresInicio.as_view(), name='colaboradores'),
    path('organizacao/', views.Organizacao.as_view(), name='organizacao'),
    path('organizacao/<slug:slug_unidade>/', views.ViewUnidade.as_view(), name='Gerenciar Unidade'),
    path('organizacao/<slug:slug_unidade>/<slug:slug_setor>/', views.ViewSetor.as_view(), name='Gerenciar Setor'),
    path('colaboradores/unidade/<slug:slug_unidade>/', views.ViewColaboradoresUnidade.as_view(),
         name='Colaboradores Unidade'),
    path('colaboradores/unidade/<slug:slug_unidade>/<slug:slug_setor>/', views.ViewColaboradoresSetor.as_view(),
         name='Colaboradores Setor'),
    path('colaboradores/unidade/<slug:slug_unidade>/<slug:slug_setor>/vincular', views.ViewColaboradoresSetorVincular.as_view(),
         name='Vincular Colaboradores Setor'),
    path('colaboradores/colaborador/<slug:slug_colaborador>/', views.Colaborador.as_view(), name='Colaborador'),
    path('organizacao-adicionar-setor/<slug:slug_unidade>/', views.CadastrarSetor.as_view(), name='Cadastrar Setor'),
]