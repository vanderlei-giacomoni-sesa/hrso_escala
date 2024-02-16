from pessoas.ferramentas.organizacao import nomear_vinculo_funcional
from pessoas.models import VinculoFuncional, PessoaFisica
from comuns.models import PeriodoReferencia
from django.http import JsonResponse
from validate_docbr import CPF

def buscar_vinculos_colaborador(colaborador):
    vinculos_colaborador = VinculoFuncional.objects.filter(profissional__pessoa_fisica=colaborador, vinculo_ativo=True)
    return [{'tipo_vinculo': nomear_vinculo_funcional(v),
             'funcao': v.profissional.funcao.nome,

             } for v in vinculos_colaborador]


def acrescentar_vinculos_profissional(profissional):
    vinculos_colaborador = VinculoFuncional.objects.filter(profissional__id=profissional['id'], vinculo_ativo=True)
    profissional['vinculos_colaborador'] = [{'vinculo': nomear_vinculo_funcional(v)} for v in vinculos_colaborador]
    return profissional


def busca_web_pessoa_fisica(request, post):
    filters = {}
    unidade = post['unidade'] if post['unidade'] and post['unidade'] != "undefined" else None
    setor = post['setor'] if post['setor'] and post['setor'] != "undefined" else None

    if setor:
        filters['profissional__vinculofuncional__vinculocolaboradorunidade__vinculopessoafisicasetor__setor__id'] = setor
    if unidade:
        filters['profissional__vinculofuncional__vinculocolaboradorunidade__unidade__id'] = unidade

    cpf = post['cpf']
    print(cpf)
    nome = post['nome']
    print(unidade, setor, nome, cpf)
    print(type(unidade), type(setor), type(nome), type(cpf))
    if CPF().validate(cpf) is True:
        filters['cpf'] = cpf
    else:
        filters['nome__icontains'] = nome

    funcionarios = PessoaFisica.objects.filter(**filters).order_by('nome') #.values('nome', 'cpf', 'slug', 'profissional__vinculofuncional__tipo_vinculo')

    funcionarios = [{'nome': f.nome,
                     'cpf': f.cpf,
                     'slug': f.slug,
                     'vinculos_funcionario': buscar_vinculos_colaborador(f)
                     } for f in funcionarios]

    return JsonResponse({'status': 'ok', 'funcionarios': funcionarios}, safe=False)
