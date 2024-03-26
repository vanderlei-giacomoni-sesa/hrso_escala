from pessoas.models import Setor, PessoaFisica, VinculoFuncional, VinculoPessoaFisicaSetor, Profissional, \
    VinculoColaboradorUnidade
from django.db.models import Q, F
from comuns.ferramentas.gerais import retornar_valor_nao_nulo

def listar_setores_setor(setor, setor_url):
    setor_pai_ativo = False
    if Setor.objects.filter(setor_pai=setor).exists():
        setores = []
        for setor in Setor.objects.filter(setor_pai=setor):

            setor_adicionar = {'nome_setor': setor.nome_setor, "sigla_setor": setor.sigla_setor,
                               'slug': setor.slug, 'setor_ativo': False}

            if setor == setor_url:
                setor_adicionar['setor_ativo'] = True
                setor_pai_ativo = True

            setores_setor = listar_setores_setor(setor, setor_url)
            if setores_setor:
                setor_adicionar['setores_setor'] = setores_setor[0]
                if setores_setor[1]:
                    setor_adicionar['setor_ativo'] = True
            else:
                setor_adicionar['setores_setor'] = None
            setores.append(setor_adicionar)

        return setores, setor_pai_ativo
    else:
        return None


def listar_setores_unidade(unidade, setor_url):
    lista_setores_unidade = []
    if Setor.objects.filter(unidade_referencia__id=unidade['id'], setor_pai__isnull=True).exists():
        setores_unidade = Setor.objects.filter(unidade_referencia__id=unidade['id'], setor_pai__isnull=True)
        print(setores_unidade)
        for setor in setores_unidade:
            setor_adicionar = {'nome_setor': setor.nome_setor, "sigla_setor": setor.sigla_setor, 'slug': setor.slug,
                               'setor_ativo': False}
            if setor == setor_url:
                setor_adicionar['setor_ativo'] = True

            setores_setor = listar_setores_setor(setor, setor_url)
            if setores_setor:
                setor_adicionar['setores_setor'] = setores_setor[0]
                if setores_setor[1]:
                    setor_adicionar['setor_ativo'] = True
            else:
                setor_adicionar['setores_setor'] = None
            lista_setores_unidade.append(setor_adicionar)

    return lista_setores_unidade


def buscar_pessoas_fisicas_com_vinculo_unidade(id_unidade):
    vinculos_unidade = VinculoColaboradorUnidade.objects.filter(unidade=id_unidade)#.values('id').annotate(
    return [{'nome': v.vinculo_funcional.profissional.pessoa_fisica.nome,
             'cpf': v.vinculo_funcional.profissional.pessoa_fisica.cpf,
             'slug': v.vinculo_funcional.profissional.pessoa_fisica.slug,
             'tipo_vinculo': nomear_vinculo_funcional(v.vinculo_funcional), 'id_vinculo_unidade': v.id
             } for v in vinculos_unidade]


def buscar_pessoas_fisicas_com_vinculo_setor(id_setor):
    vinculos_setor = VinculoPessoaFisicaSetor.objects.filter(setor__id=id_setor, ativo=True)

    return [{'nome': v.vinculo_unidade.vinculo_funcional.profissional.pessoa_fisica.nome,
             'cpf': v.vinculo_unidade.vinculo_funcional.profissional.pessoa_fisica.cpf,
             'slug': v.vinculo_unidade.vinculo_funcional.profissional.pessoa_fisica.slug,
             'tipo_vinculo': nomear_vinculo_funcional(v.vinculo_unidade.vinculo_funcional), 'id_vinculo_setor': v.id
             } for v in vinculos_setor]


def nomear_vinculo_funcional(vinculo_funcional):
    if isinstance(vinculo_funcional, VinculoFuncional):
        return {1: "SESA", 2:"FUNEAS",
            3: vinculo_funcional.cnpj_vinculo.razao_social_fornecedor,
            4: vinculo_funcional.cnpj_vinculo.razao_social_fornecedor}[vinculo_funcional.tipo_vinculo]
    else:
        v = VinculoFuncional.objects.get(id=vinculo_funcional)
        return {1: "SESA", 2: "FUNEAS",
                3: v.cnpj_vinculo.razao_social_fornecedor,
                4: v.cnpj_vinculo.razao_social_fornecedor}[v.tipo_vinculo]





