from django import forms

from pessoas.models import Unidade, Setor


class FormularioUnidade(forms.ModelForm):
    titulo = "Informações da Unidade:"

    class Meta:

        model = Unidade
        fields = ['nome_unidade',
                  'sigla_unidade',
                  'diretor_unidade',
                  'nome_cargo_diretor',
                  ]


class FormularioSetorUnidade(forms.ModelForm):
    titulo = "Informações do Setor:"

    class Meta:

        model = Setor
        fields = ['nome_setor',
                  'sigla_setor',
                  'responsavel_setor',
                  'cargo_responsavel_setor',
                  'setor_ativo',
                  'setor_pai',
                  ]


class FormularioNovoSetorUnidade(forms.ModelForm):
    titulo = "Informações do Setor:"

    class Meta:

        model = Setor
        fields = ['nome_setor',
                  'unidade_referencia',
                  'sigla_setor',
                  'responsavel_setor',
                  'cargo_responsavel_setor',
                  'setor_pai',
                  ]

        widgets = {
            'unidade_referencia': forms.HiddenInput(),
            'setor_pai': forms.HiddenInput(),
        }
