from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'Contratos'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('contratos-unidade/unidade/<slug:slug_unidade>/', views.ContratosUnidade.as_view(),
         name='Contratos Unidade'),
    path('contrato/<slug:slug_contrato>/', views.DetalhesContrato.as_view(), name='Contrato'),
    path('licitacoes/unidade/<slug:slug_unidade>/', views.LicitacoesUnidade.as_view(),
         name='Licitacoes Unidade'),
    path('licitacoes/unidade/<slug:slug_unidade>/licitacao/<slug:slug_licitacao>/', views.LicitacaoUnidade.as_view(),
         name='Licitacao Unidade'),
    path('licitacoes/unidade/<slug:slug_unidade>/licitacao/<slug:slug_licitacao>/novo-contrato/',
         views.NovoContrato.as_view(), name='Novo Contrato Licitacao'),

    path('fornecedores/', views.Fornecedores.as_view(),
         name='Fornecedores'),
    path('fornecedores/novo-fornecedor', views.NovoFornecedor.as_view(),
         name='Novo Fornecedor'),

    path('fornecedores/fornecedor/<slug:slug_fornecedor>/', views.ViewFornecedor.as_view(),
         name='Fornecedor'),
    path('fornecedores/fornecedor/<slug:slug_fornecedor>/novo-contrato/', views.NovoContrato.as_view(),
         name='Novo Contrato Fornecedor'),
]

