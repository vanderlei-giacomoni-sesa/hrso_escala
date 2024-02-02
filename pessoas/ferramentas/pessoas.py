from pessoas.ferramentas.organizacao import nomear_vinculo_funcional
from pessoas.models import VinculoFuncional


def buscar_vinculos_colaborador(colaborador):
    vinculos_colaborador = VinculoFuncional.objects.filter(profissional__pessoa_fisica=colaborador,
                                                                vinculo_ativo=True)
    return [{'tipo_vinculo': nomear_vinculo_funcional(v),
             'funcao': v.profissional.funcao.nome,

             } for v in vinculos_colaborador
            ]