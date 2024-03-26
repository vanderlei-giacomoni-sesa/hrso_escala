from contratos.models import Fornecedor, Licitacao
from django.forms import ModelForm


class FornecedorForm(ModelForm):
    titulo = 'Fornecedor'

    class Meta:
        model = Fornecedor
        fields = ['cnpj_fornecedor', 'nome_fantasia', 'razao_social_fornecedor', 'nome_banco', 'codigo_banco',
                  'agencia_banco', 'conta_fornecedor', 'estado_fornecedor', 'cidade_fornecedor',
                  'bairro_fornecedor', 'cep_fornecedor', 'endereco_fornecedor', 'telefone_fornecedor',
                  'contato_fornecedor', 'email_fornecedor']


class FornecedorAtualizar(ModelForm):
    titulo = 'Fornecedor'

    class Meta:
        model = Fornecedor
        fields = ['nome_fantasia', 'razao_social_fornecedor', 'nome_banco', 'codigo_banco',
                  'agencia_banco', 'conta_fornecedor', 'estado_fornecedor', 'cidade_fornecedor',
                  'bairro_fornecedor', 'cep_fornecedor', 'endereco_fornecedor', 'telefone_fornecedor',
                  'contato_fornecedor', 'email_fornecedor']


class NovaLicitacao(ModelForm):
    titulo = 'Nova Licitação'

    class Meta:
        model = Licitacao
        fields = ['modalidade_licitacao', 'numero_licitacao', 'objeto', 'unidades']




