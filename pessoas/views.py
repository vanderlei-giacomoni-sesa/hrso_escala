from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, F
from django.http import JsonResponse
from django.shortcuts import resolve_url

from django.db.models.functions import Coalesce
from django.db.models.expressions import Value

from localflavor.br.br_states import STATE_CHOICES

from escala_geral.models import DadosConselhoProfissional, RegimeEscala, Escala

from pessoas.ferramentas.organizacao import listar_setores_unidade, buscar_pessoas_fisicas_com_vinculo_unidade, \
    buscar_pessoas_fisicas_com_vinculo_setor, nomear_vinculo_funcional
from pessoas.ferramentas.pessoas import (
    buscar_vinculos_colaborador, busca_web_pessoa_fisica, acrescentar_vinculos_profissional)
from pessoas.forms import FormularioUnidade, FormularioNovoSetorUnidade, FormularioSetorUnidade
import json

from pessoas.models import PessoaFisica, Unidade, PessoaFisicaUsuario, VinculoPessoaFisicaSetor, Setor, \
    VinculoFuncional, Profissional, VinculoColaboradorUnidade
from comuns.models import Funcao, ConselhoProfissional, Ocupacao, Fornecedor
from comuns.ferramentas.gerais import retornar_valor_nao_nulo

# Create your views here.

@login_required
def inicio(request):
    return redirect("Pessoas:organizacao")


@login_required
def colaboradores(request):
    cpf_usuario = PessoaFisicaUsuario.objects.get(usuario=request.user)
    unidade_usuario = Unidade.objects.filter(
        vinculocolaboradorunidade__vinculo_funcional__profissional__pessoa_fisica=cpf_usuario.pessoa_fisica).first()

    print(unidade_usuario)

    return redirect("Pessoas:Colaboradores Unidade", slug_unidade=unidade_usuario.slug)


class BaseViewOrganizacao(LoginRequiredMixin, View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.unidade = None
        self.unidades = None
        self.context = None
        self.setor = None
        self.nav_path = None

    def dados_unidade(self, u):
        u['setores_unidade'] = listar_setores_unidade(u, self.setor)
        u['ativa'] = False if not self.unidade else (True if u['id'] == self.unidade.id else False)
        return u

    def dispatch(self, request, *args, **kwargs):
        if 'slug_unidade' in kwargs:
            self.unidade = Unidade.objects.get(slug=kwargs['slug_unidade'])
        if 'slug_setor' in kwargs:
            self.setor = Setor.objects.get(slug=kwargs['slug_setor'])

        print(request.user)

        cpf_usuario = PessoaFisicaUsuario.objects.get(usuario=request.user)

        unidades = Unidade.objects.filter(
            vinculocolaboradorunidade__vinculo_funcional__profissional__pessoa_fisica=cpf_usuario.pessoa_fisica
        ).values('id', 'nome_unidade', 'sigla_unidade', 'slug').distinct()

        print(unidades)

        self.unidades = [self.dados_unidade(u) for u in unidades]

        self.context = {'unidade': self.unidade, 'unidades': self.unidades,
                        'setor': self.setor, 'nav_path': self.nav_path}

        return super().dispatch(request, *args, **kwargs)


class CoalboradoresInicio(BaseViewOrganizacao):

    def processar_post(self, request, post):
        tipos_acao = {"buscar-pessoas": busca_web_pessoa_fisica}
        return tipos_acao[post['tipo-acao']](request, post)


    def get(self, request, *args, **kwargs):

        self.nav_path = [{"nome": "Colaboradores",
                          'href': "#",
                          'ativo': True, 'options': None},
                         ]
        self.context['nav_path'] = self.nav_path

        return render(request, 'pessoas/colaboradores_inicio.html', self.context)

    def post(self, request, *args, **kwargs):
        post = request.POST.copy().dict()
        return self.processar_post(request, post)


class Colaborador(BaseViewOrganizacao):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.colaborador = None

    def criar_vinculo_funcional(self, request, post):
        print('Criar Vinculo Funcional')
        print(post)
        vinculos_processaveis = {
            VinculoFuncional.Vinculo.FUNEAS.label: self.criar_vinculo_funeas,
            VinculoFuncional.Vinculo.CONTRATO.label: self.criar_vinculo_contrato,
            VinculoFuncional.Vinculo.ACADEMICO.label: self.criar_vinculo_academico,
        }
        return vinculos_processaveis[post['tipoVinculo']](request, post)

    def criar_vinculo_funeas(self, request, post):
        print(request, post)
        funeas = Fornecedor.objects.get(cnpj_fornecedor="24039073000155")
        unidade = Unidade.objects.get(id=int(post['idUnidade']))
        profissional = Profissional.objects.get(id=post['idProfissional'])
        print(funeas)
        vinculo, criado = VinculoFuncional.objects.update_or_create(
            profissional=profissional, cnpj_vinculo=funeas, tipo_vinculo=VinculoFuncional.Vinculo.FUNEAS,
            defaults={'vinculo_ativo': True}
        )
        vinculo_unidade, vuc = VinculoColaboradorUnidade.objects.update_or_create(
            unidade=unidade, vinculo_funcional=vinculo, defaults={'ativo': True, 'fim_vinculo': None})

        return redirect('Pessoas:Colaborador', slug_colaborador=self.colaborador.slug)

    def criar_vinculo_contrato(self, request, post):
        print('Criar Vinculo Contrato')
        print(post)
        fornecedor = Fornecedor.objects.get(id=int(post['idFornecedor']))
        profissional = Profissional.objects.get(id=post['idProfissional'])

        unidade = Unidade.objects.get(id=int(post['idUnidade']))

        print(profissional)
        print(fornecedor)

        vinculo, criado = VinculoFuncional.objects.update_or_create(
            profissional=profissional, cnpj_vinculo=fornecedor, tipo_vinculo=VinculoFuncional.Vinculo.CONTRATO,
            defaults={'vinculo_ativo': True}
        )

        vinculo_unidade, vuc = VinculoColaboradorUnidade.objects.update_or_create(
            unidade=unidade, vinculo_funcional=vinculo, defaults={'ativo': True, 'fim_vinculo': None})

        return redirect('Pessoas:Colaborador', slug_colaborador=self.colaborador.slug)

    def criar_vinculo_academico(self, request, post):
        print('Criar Vinculo Contrato')
        print(post)

        unidade = Unidade.objects.get(id=int(post['idUnidade']))

        fornecedor = Fornecedor.objects.get(id=int(post['idFornecedor']))
        profissional = Profissional.objects.get(id=post['idProfissional'])

        vinculo, criado = VinculoFuncional.objects.update_or_create(
            profissional=profissional, cnpj_vinculo=fornecedor, tipo_vinculo=VinculoFuncional.Vinculo.ACADEMICO,
            defaults={'vinculo_ativo': True})

        vinculo_unidade, vuc = VinculoColaboradorUnidade.objects.update_or_create(
            unidade=unidade, vinculo_funcional=vinculo, defaults={'ativo': True, 'fim_vinculo': None})

        return redirect('Pessoas:Colaborador', slug_colaborador=self.colaborador.slug)

    def vincular_funcao_colaborador(self, request, post):
        funcao_vincular = Funcao.objects.get(id=int(post['funcaoSelecionada']))

        conselho = ConselhoProfissional.objects.get(
            id=int(post['conselhoSelecionado'])) if "conselhoSelecionado" in post else None

        numero_conselho = post['numeroConselho'] if "numeroConselho" in post else None

        estado_conselho = post['EstadoConselho'] if "EstadoConselho" in post else None

        ocupacao = Ocupacao.objects.get(id=int(post['ocupacaoSelecionada']))

        print("Dados Vinculo", funcao_vincular, conselho, estado_conselho, numero_conselho)

        p, c = Profissional.objects.update_or_create(
            funcao=funcao_vincular, pessoa_fisica=self.colaborador, cbo=ocupacao,
            defaults={'ativo': True})

        if conselho and estado_conselho and numero_conselho:
            dc, dcc = DadosConselhoProfissional.objects.get_or_create(
                profissional=p, conselho=conselho, estado_conselho=estado_conselho, numero=numero_conselho)

        return redirect('Pessoas:Colaborador', slug_colaborador=self.colaborador.slug)

    def inativar_vinculo_funcional(self, request, post):
        vinculo = VinculoFuncional.objects.get(id=post['idVinculoFuncional'])
        vinculo.vinculo_ativo = False
        vinculo.save()

        return JsonResponse({'status': 'ok', 'idVinculoFuncional': post['idVinculoFuncional']}, safe=False)

    def buscar_fornecedor_contratado_vincular(self, request, post):
        print(request, post)
        razao_social = post['razaoSocial']
        cnpj_buscar = post['cnpj']

        filters = {}

        from validate_docbr import CNPJ

        if CNPJ().validate(cnpj_buscar) is True:
            filters['cnpj_fornecedor'] = cnpj_buscar
        elif len(razao_social) >= 3:
            filters['razao_social_fornecedor__icontains'] = razao_social
        else:
            return JsonResponse({'status': 'informações-invalidas', 'idProfissional': post['idProfissional']}, safe=False)
        fornecedores = Fornecedor.objects.filter(**filters).values('razao_social_fornecedor', 'id')

        return JsonResponse({'status': 'ok',
                             'idProfissional': post['idProfissional'],
                             'fornecedores': list(fornecedores),
                             }, safe=False)

    def processar_post(self, request, post):
        tipos_acao = {"vincularFuncaoColaborador": self.vincular_funcao_colaborador,
                      'criarVinculoFuncional': self.criar_vinculo_funcional,
                      'inativarVinculoFuncional': self.inativar_vinculo_funcional,
                      'buscarFornecedorContratadoVincular': self.buscar_fornecedor_contratado_vincular}
        return tipos_acao[post['tipo-acao']](request, post)

    def post(self, request, *args, **kwargs):
        self.colaborador = PessoaFisica.objects.get(slug=kwargs['slug_colaborador'])
        post = request.POST.copy().dict()
        return self.processar_post(request, post)

    def get(self, request, *args, **kwargs):
        self.colaborador = PessoaFisica.objects.get(slug=kwargs['slug_colaborador'])
        self.nav_path = [{"nome": "Colaboradores",
                          'href': resolve_url("Pessoas:colaboradores"),
                          'ativo': False, 'options': None},
                         {"nome": self.colaborador.nome, 'href': "#", 'ativo': True, 'options': None}]
        self.context['nav_path'] = self.nav_path
        print(self.context['nav_path'])
        self.context['colaborador'] = self.colaborador

        self.context['profissoes_colaborador'] = [acrescentar_vinculos_profissional(p) for p in Profissional.objects.filter(
            pessoa_fisica=self.colaborador, funcao__ativa=True).values('id').annotate(
            funcao=F('funcao__nome'), nome_conselho=F('dadosconselhoprofissional__conselho__sigla'),
            estado_conselho=F('dadosconselhoprofissional__estado_conselho'),
            numero_conselho=F('dadosconselhoprofissional__numero'))]

        #self.context['vinculos_colaborador'] = buscar_vinculos_colaborador(self.colaborador)

        self.context['funcoes'] = list(
            Funcao.objects.filter(ativa=True).values('nome', 'id').annotate(
                ocupacoes=ArrayAgg('ocupacoes_permitidas__id', distinct=True),
                conselhos=ArrayAgg('conselhos_permitidos__id', distinct=True)
            ))
        self.context['ocupacoes'] = list(Ocupacao.objects.filter().values('codigo_cbo', 'id', 'titulo'))
        self.context['conselhos'] = list(ConselhoProfissional.objects.filter().values('id', 'sigla', 'nome'))
        self.context['estados'] = [e[0] for e in STATE_CHOICES]

        return render(request, 'pessoas/colaborador.html', self.context)


class Organizacao(BaseViewOrganizacao):
    def get(self, request):
        self.nav_path = [{"nome": "Organização", 'href': resolve_url("Pessoas:organizacao"), 'ativo': True, 'options': None}]
        self.context['nav_path'] = self.nav_path
        return render(request, 'pessoas/organizacao.html', self.context)


class ViewUnidade(BaseViewOrganizacao):
    def post(self, request, *args, **kwargs):
        form = FormularioUnidade(request.POST, instance=self.unidade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Unidade atualizada com sucesso!')
        else:
            messages.error(request, 'Erro ao atualizar unidade!')
        return redirect('Pessoas:Gerenciar Unidade', slug_unidade=self.unidade.slug)

    def get(self, request, *args, **kwargs):
        self.nav_path = [{"nome": "Organização", 'href': resolve_url('Pessoas:organizacao'), 'ativo': False, 'options': None},

                         {"nome": self.unidade.nome_unidade, 'href': "#", 'ativo': True, 'options': None}]
        self.context['nav_path'] = self.nav_path
        form = FormularioUnidade(instance=self.unidade)
        self.context['form'] = form

        return render(request, 'pessoas/unidade.html', self.context)


class ViewSetor(BaseViewOrganizacao):
    def post(self, request, *args, **kwargs):
        form = FormularioSetorUnidade(request.POST, instance=self.setor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Setor atualizado com sucesso!')
        else:
            messages.error(request, 'Erro ao atualizar o Setor!')
        return redirect('Pessoas:Gerenciar Setor', slug_unidade=kwargs['slug_unidade'], slug_setor=kwargs['slug_setor'])

    def get(self, request, *args, **kwargs):
        self.nav_path = [{"nome": "Organização", 'href': resolve_url("Pessoas:organizacao"), 'ativo': False, 'options': None},
                         {"nome": self.unidade.nome_unidade,
                          'href': resolve_url('Pessoas:Gerenciar Unidade', slug_unidade=self.unidade.slug),
                          'ativo': False, 'options': None},
                         {"nome": self.setor.nome_setor, 'href': "#", 'ativo': True, 'options': None}]
        self.context['nav_path'] = self.nav_path
        form = FormularioSetorUnidade(instance=self.setor)
        self.context['form'] = form
        return render(request, 'pessoas/unidade.html', self.context)


class ViewEscalaSetor(BaseViewOrganizacao):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

    def processar_post(self, request, post):
        print(post)
        tipos_acao = {"AdicionarEscala": self.adicionar_escala}

        return tipos_acao[post['tipo-acao']](request, post)
    def post(self, request, *args, **kwargs):
        post = request.POST.copy().dict()
        return self.processar_post(request, post)

    def adicionar_escala(self, request, post):

        if (regime_escala := post['regimeEscala']) in RegimeEscala.values and self.setor.id == int(post['id_setor']):
            nome_escala = post['nomeEscala']
            escala, created = Escala.objects.update_or_create(nome_escala=nome_escala,
                                                              regime_escala=regime_escala,
                                                              setor=self.setor, defaults={"escala_ativa":True}
                                                              )
            print(escala)
        else:
            messages.error(request, 'Erro ao adicionar escala, informações incorretas')

        return redirect("Pessoas:Gerenciar Escalas Setor",
                        slug_setor=self.setor.slug, slug_unidade=self.unidade.slug)

    def get(self, request, *args, **kwargs):
        self.context['escalas'] = list(Escala.objects.filter(setor=self.setor).values(
            'id', 'nome_escala', 'escala_ativa', 'regime_escala', 'slug'))

        self.context['regimes_escala'] = [{'value': opcao.value, "label": opcao.label} for opcao in RegimeEscala]

        print(self.unidade, self.setor)
        self.nav_path = [{"nome": "Organização", 'href': resolve_url("Pessoas:organizacao"), 'ativo': False, 'options': None},
                         {"nome": self.unidade.nome_unidade,
                          'href': resolve_url('Pessoas:Gerenciar Unidade', slug_unidade=self.unidade.slug),
                          'ativo': False, 'options': None},
                         {"nome": self.setor.nome_setor,
                          'href': resolve_url('Pessoas:Gerenciar Setor', slug_unidade=self.unidade.slug,
                                              slug_setor=self.setor.slug),
                          'ativo': False, 'options': None},
                         {"nome": "Escalas", 'href': "#", 'ativo': False, 'options': None}
                         ]
        self.context['nav_path'] = self.nav_path

        return render(request, 'pessoas/organizacao/escalas_setor.html', self.context)



class ViewColaboradoresUnidade(BaseViewOrganizacao):
    def get(self, request, *args, **kwargs):
        self.nav_path = [{"nome": "Colaboradores", 'href': resolve_url("Pessoas:colaboradores"), 'ativo': False, 'options': None},
                         {"nome": self.unidade.nome_unidade,
                          'href': resolve_url('Pessoas:Colaboradores Unidade', slug_unidade=self.unidade.slug),
                          'ativo': True, 'options': None},
                         ]
        self.context['nav_path'] = self.nav_path

        self.context['colaboradores'] = None # list(buscar_pessoas_fisicas_com_vinculo_unidade(self.unidade.id))
        self.context['unidade'] = self.unidade

        return render(request, 'pessoas/colaboradores_unidade.html', self.context)

    def processar_post(self, request, post):
        tipos_acao = {"buscar-pessoas": busca_web_pessoa_fisica}
        return tipos_acao[post['tipo-acao']](request, post)

    def post(self, request, *args, **kwargs):
        post = request.POST.copy().dict()
        return self.processar_post(request, post)


class ViewColaboradoresSetor(BaseViewOrganizacao):

    def processar_post(self, request, post):
        print(post)

        tipos_acao = {
                      "inativarVinculoColaboradorSetor": self.inativar_vinculo_colaborador_setor}

        return tipos_acao[post['tipo-acao']](request, post)

    def inativar_vinculo_colaborador_setor(self, request, post):
        vinculo_inativar = VinculoPessoaFisicaSetor.objects.get(id=post['idVinculoColaboradorSetor'])
        vinculo_inativar.ativo = False
        vinculo_inativar.save()

        return JsonResponse({'status': 'ok', 'idVinculoColaboradorSetor': post['idVinculoColaboradorSetor']}, safe=False)

    def get(self, request, *args, **kwargs):
        self.nav_path = [{"nome": "Colaboradores", 'href': resolve_url("Pessoas:colaboradores"), 'ativo': False, 'options': None},
                         {"nome": self.unidade.nome_unidade,
                          'href': resolve_url('Pessoas:Colaboradores Unidade', slug_unidade=self.unidade.slug),
                          'ativo': False, 'options': None},
                         {"nome": self.setor.nome_setor,
                          'href': resolve_url('Pessoas:Colaboradores Setor', slug_unidade=self.unidade.slug,
                                              slug_setor=self.setor.slug), 'ativo': True, 'options': None}


                         ]
        self.context['nav_path'] = self.nav_path
        colaboradores = list(buscar_pessoas_fisicas_com_vinculo_setor(self.setor.id))
        self.context['colaboradores'] = colaboradores

        return render(request, 'pessoas/colaboradores_setor.html', self.context)

    def post(self, request, *args, **kwargs):
        post = request.POST.copy().dict()
        return self.processar_post(request, post)


class ViewColaboradoresSetorVincular(BaseViewOrganizacao):

    def buscar_colaborador(self, request, post):
        filtro_nome = Q(pessoa_fisica__nome__icontains=post['informacoes-buscar'],
                        vinculofuncional__vinculocolaboradorunidade__unidade=self.unidade)

        filtro_funcao = Q(funcao=post['informacoes-buscar'],
                          vinculofuncional__vinculocolaboradorunidade__unidade=self.unidade)

        filtros = {'nome': filtro_nome,
                   'funcao': filtro_funcao,
                   }

        colaboradores = Profissional.objects.filter(filtros[post['tipo-busca']]).values(
            'pessoa_fisica__nome', 'id', 'funcao__nome', 'vinculofuncional__id',
            'vinculofuncional__vinculocolaboradorunidade__id').distinct()

        return JsonResponse(
            {'status': 'ok',
             'colaboradores': [
                 {'nome': c['pessoa_fisica__nome'],
                  'id': c['id'],
                  'funcao': c['funcao__nome'],
                  'id_vinculo_colaborador_unidade': c['vinculofuncional__vinculocolaboradorunidade__id'],
                  'vinculo': nomear_vinculo_funcional(c['vinculofuncional__id'])
                  } for c in colaboradores]
             }, safe=False)

    def vincular_colaboradores_setor(self, request, post):
        post_processar = request.POST.copy()

        profissionais_vincular = request.POST.getlist("profissionalVincular")

        for id_profissional in profissionais_vincular:
            vu = VinculoColaboradorUnidade.objects.get(id=int(id_profissional))
            # Rever questoes de vinculo ativo e fim de vinculo - criar novos vinculos se inativo?
            vcs, created = VinculoPessoaFisicaSetor.objects.update_or_create(
                setor=self.setor, vinculo_unidade=vu, defaults={'ativo': True, 'fim_vinculo': None})

        return redirect('Pessoas:Colaboradores Setor',
                        slug_unidade=self.unidade.slug, slug_setor=self.setor.slug)

    def processar_post(self, request, post):
        print(post)

        tipos_acao = {"buscar-colaborador": self.buscar_colaborador,
                      "vincularColaboradoresSetor": self.vincular_colaboradores_setor}

        return tipos_acao[post['tipo-acao']](request, post)

    def get(self, request, *args, **kwargs):
        print("get", request)
        self.nav_path = [{"nome": "Colaboradores", 'href': resolve_url("Pessoas:colaboradores"), 'ativo': False, 'options': None},
                         {"nome": self.unidade.nome_unidade,
                          'href': resolve_url('Pessoas:Colaboradores Unidade', slug_unidade=self.unidade.slug),
                          'ativo': False, 'options': None},
                         {"nome": self.setor.nome_setor,
                          'href': resolve_url('Pessoas:Colaboradores Setor', slug_unidade=self.unidade.slug,
                                              slug_setor=self.setor.slug), 'ativo': False, 'options': None},
                         {"nome": "Vincular Colaboradores", 'href': "#", 'ativo': True, 'options': None}

                         ]
        self.context['nav_path'] = self.nav_path
        colaboradores = list(buscar_pessoas_fisicas_com_vinculo_setor(self.setor.id))
        self.context['colaboradores'] = colaboradores
        self.context['funcoes'] = list(Funcao.objects.filter(ativa=True).values('nome', 'id'))

        return render(request, 'pessoas/colaboradores_setor_vincular.html', self.context)

    def post(self, request, *args, **kwargs):
        post = request.POST.copy().dict()
        return self.processar_post(request, post)


class CadastrarSetor(LoginRequiredMixin, View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.unidade = None
        self.setor = None

    def dispatch(self, request, *args, **kwargs):
        self.unidade = Unidade.objects.get(slug=kwargs['slug_unidade'])

        return super().dispatch(request, *args, **kwargs)

    def processar_post(self, request, post):

        acoes = {'novo-setor-setor': self.novo_setor_setor,
                 'novo-setor-unidade': self.novo_setor_unidade,
                 'salvar-novo-setor': self.salvar_novo_setor,
                 }

        return acoes[post['tipo-acao']](request, post)

    def novo_setor_setor(self, *args, **kwargs):
        print('novo_setor_setor', args)
        self.setor = Setor.objects.get(id=int(args[1]['id']))
        form = FormularioNovoSetorUnidade(initial={'unidade_referencia': self.unidade, 'setor_pai': self.setor})
        return render(args[0], 'pessoas/cadastrar_setor.html', {'unidade': self.unidade,
                                                                'setor': self.setor,
                                                                'form': form
                                                                })

    def novo_setor_unidade(self, *args, **kwargs):
        print('novo_setor_unidade')
        form = FormularioNovoSetorUnidade(initial={'unidade_referencia': self.unidade, 'setor_pai': None})
        return render(args[0], 'pessoas/cadastrar_setor.html', {'unidade': self.unidade,
                                                                'setor': self.setor,
                                                                'form': form})

    def salvar_novo_setor(self, *args, **kwargs):
        print('salvar_novo_setor')
        form = FormularioNovoSetorUnidade(args[0].POST)
        print(form)
        if form.is_valid():
            novo_setor = form.save()
            return redirect('Pessoas:Gerenciar Setor',
                            slug_unidade=self.unidade.slug,
                            slug_setor=novo_setor.slug)
        print("O formulario nao e valido")

        form = FormularioNovoSetorUnidade(initial={'unidade_referencia': self.unidade, 'setor_pai': self.setor})
        return render(args[0], 'pessoas/cadastrar_setor.html', {'unidade': self.unidade,
                                                                'setor': self.setor,
                                                                'form': form})


    def post(self, request, *args, **kwargs):
        post = request.POST.copy().dict()
        return self.processar_post(request, post)

    def get(self, request, *args, **kwargs):
        return redirect('Pessoas:organizacao')


class BaseViewFuncao(LoginRequiredMixin, View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.funcao = None
        self.funcoes = None
        self.context = None
    def dispatch(self, request, *args, **kwargs):
        if 'slug_funcao' in kwargs:
            self.funcao = Funcao.objects.get(slug=kwargs['slug_funcao'])
        self.funcoes = Funcao.objects.all().values('id', 'nome', 'slug', 'ativa')

        self.context = {'funcao': self.funcao, 'funcoes': self.funcoes}

        return super().dispatch(request, *args, **kwargs)


class FuncoesProfissionais(BaseViewFuncao):
    def get(self, request, *args, **kwargs):
        self.nav_path = [
            {"nome": "Funções", 'href': '#', 'ativo': True, 'options': None}]
        self.context['nav_path'] = self.nav_path

        return render(request, 'pessoas/funcao/funcoes.html', context=self.context)


class FuncaoProfissional(BaseViewFuncao):

    def vincular_cbo(self, request, post):
        ocupacao = Ocupacao.objects.get(id=post['idCbo'])
        self.funcao.ocupacoes_permitidas.add(ocupacao)
        return JsonResponse({'status': 'ok'}, safe=False)

    def vincular_conselho(self, request, post):
        conselho = ConselhoProfissional.objects.get(id=post['idConselhoClasse'])
        self.funcao.conselhos_permitidos.add(conselho)
        return JsonResponse({'status': 'ok'}, safe=False)

    def desvincular_cbo(self, request, post):
        ocupacao = Ocupacao.objects.get(id=post['idCbo'])
        self.funcao.ocupacoes_permitidas.remove(ocupacao)
        return JsonResponse({'status': 'ok'}, safe=False)

    def desvincular_conselho(self, request, post):
        conselho = ConselhoProfissional.objects.get(id=post['idConselhoClasse'])
        print(conselho)
        self.funcao.conselhos_permitidos.remove(conselho)
        return JsonResponse({'status': 'ok'}, safe=False)

    def processar_post(self, request, post):
        acoes = {'vincularCbo': self.vincular_cbo,
                 'vincularConselhoClasse': self.vincular_conselho,
                 'desvincularCbo': self.desvincular_cbo,
                 'desvincularConselhoClasse': self.desvincular_conselho,
                 }
        return acoes[post['tipo-acao']](request, post)


    def get(self, request, *args, **kwargs):
        self.nav_path = [
            {"nome": "Funções", 'href': '#', 'ativo': None, 'options': None},
        {"nome": f"{self.funcao.nome}", 'href': '#', 'ativo': True, 'options': None}]

        self.context['nav_path'] = self.nav_path

        self.context['ocupacoes_funcao'] = list(
            Ocupacao.objects.filter(funcao=self.funcao).values('id', 'codigo_cbo', 'titulo'))

        self.context['ocupacoes'] = list(Ocupacao.objects.filter().exclude(
            id__in=[o['id'] for o in self.context['ocupacoes_funcao']]
        ).values('id', 'codigo_cbo', 'titulo'))

        self.context['conselhos_funcao'] = list(
            ConselhoProfissional.objects.filter(funcao=self.funcao).values('id', 'sigla', 'nome'))
        self.context['conselhos_profissionais'] = list(
            ConselhoProfissional.objects.filter().exclude(
                id__in=[c['id'] for c in self.context['conselhos_funcao']]
            ).values('id', 'sigla', 'nome'))

        print(self.context['conselhos_profissionais'])

        return render(request, 'pessoas/funcao/funcao.html', context=self.context)

    def post(self, request, *args, **kwargs):
        post = request.POST.copy().dict()
        print(post)
        return self.processar_post(request, post)