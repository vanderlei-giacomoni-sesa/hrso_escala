from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import resolve_url

from pessoas.ferramentas.organizacao import listar_setores_unidade, buscar_pessoas_fisicas_com_vinculo_unidade, \
    buscar_pessoas_fisicas_com_vinculo_setor
from pessoas.ferramentas.pessoas import buscar_vinculos_colaborador
from pessoas.forms import FormularioUnidade, FormularioNovoSetorUnidade, FormularioSetorUnidade
import json

from pessoas.models import PessoaFisica, Unidade, PessoaFisicaUsuario, VinculoPessoaFisicaSetor, Setor, \
    VinculoFuncional, Profissional, VinculoColaboradorUnidade
from comuns.models import Funcao
from comuns.ferramentas.gerais import retornar_valor_nao_nulo

# Create your views here.

@login_required
def inicio(request):
    return redirect("Pessoas:colaboradores")


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
        ).values('id', 'nome_unidade', 'sigla_unidade', 'slug')

        print(unidades)

        self.unidades = [self.dados_unidade(u) for u in unidades]

        self.context = {'unidade': self.unidade, 'unidades': self.unidades,
                        'setor': self.setor, 'nav_path': self.nav_path}

        return super().dispatch(request, *args, **kwargs)


class CoalboradoresInicio(BaseViewOrganizacao):

    def get(self, request, *args, **kwargs):

        self.nav_path = [{"nome": "Colaboradores",
                          'href:': "#",
                          'ativo': True, 'options': None},
                         ]
        self.context['nav_path'] = self.nav_path

        return render(request, 'pessoas/colaboradores_inicio.html', self.context)


class Colaborador(BaseViewOrganizacao):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.colaborador = None

    def get(self, request, *args, **kwargs):
        print(kwargs['slug_colaborador'])
        self.colaborador = PessoaFisica.objects.get(slug=kwargs['slug_colaborador'])
        self.nav_path = [{"nome": "Colaboradores",
                          'href:': resolve_url("Pessoas:colaboradores"),
                          'ativo': False, 'options': None},
                         {"nome": self.colaborador.nome, 'href': "#", 'ativo': True, 'options': None}]
        self.context['nav_path'] = self.nav_path
        self.context['colaborador'] = self.colaborador
        self.context['vinculos_colaborador'] = buscar_vinculos_colaborador(self.colaborador)
        return render(request, 'pessoas/colaborador.html', self.context)


class Organizacao(BaseViewOrganizacao):
    def get(self, request):
        self.nav_path = [{"nome": "Organização", 'href:': "#", 'ativo': True, 'options': None}]
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
        self.nav_path = [{"nome": "Organização", 'href:': "#", 'ativo': False, 'options': None},
                         {"nome": self.unidade.nome_unidade, 'href': resolve_url('Pessoas:Gerenciar Unidade', slug_unidade=self.unidade.slug), 'ativo': True, 'options': None}]
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
        self.nav_path = [{"nome": "Organização", 'href:': "#", 'ativo': False, 'options': None},
                         {"nome": self.unidade.nome_unidade,
                          'href': resolve_url('Pessoas:Gerenciar Unidade', slug_unidade=self.unidade.slug),
                          'ativo': False, 'options': None},
                         {"nome": self.setor.nome_setor, 'href:': "#", 'ativo': True, 'options': None}]
        self.context['nav_path'] = self.nav_path
        form = FormularioSetorUnidade(instance=self.setor)
        self.context['form'] = form
        return render(request, 'pessoas/unidade.html', self.context)


class ViewColaboradoresUnidade(BaseViewOrganizacao):
    def get(self, request, *args, **kwargs):
        self.nav_path = [{"nome": "Organização", 'href:': "#", 'ativo': False, 'options': None},
                         {"nome": self.unidade.nome_unidade,
                          'href': resolve_url('Pessoas:Colaboradores Unidade', slug_unidade=self.unidade.slug),
                          'ativo': True, 'options': None},
                         ]
        self.context['nav_path'] = self.nav_path

        self.context['colaboradores'] = list(buscar_pessoas_fisicas_com_vinculo_unidade(self.unidade.id))

        return render(request, 'pessoas/colaboradores_unidade.html', self.context)


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
        self.nav_path = [{"nome": "Organização", 'href:': "#", 'ativo': False, 'options': None},
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
        filtro_nome = Q(
            pessoa_fisica__nome__icontains=post['informacoes-buscar'],
            vinculofuncional__vinculocolaboradorunidade__unidade=self.unidade
        )

        filtro_funcao = Q(funcao=post['informacoes-buscar'],
                          vinculofuncional__vinculocolaboradorunidade__unidade=self.unidade)

        filtros = {'nome': filtro_nome,
                   'funcao': filtro_funcao,
                   }

        colaboradores = Profissional.objects.filter(filtros[post['tipo-busca']]).values(
            'pessoa_fisica__nome', 'id', 'funcao__nome', 'vinculofuncional__id', 'vinculofuncional__vinculocolaboradorunidade__id'
            )

        #colaboradores = VinculoColaboradorUnidade.objects.filter(filtro_vinculos)
        return JsonResponse({'status': 'ok',
                             'colaboradores': [{'nome': c['pessoa_fisica__nome'],
                                                'id': c['id'],
                                                'funcao': c['funcao__nome'],
                                                'id_vinculo_colaborador_unidade': c['vinculofuncional__vinculocolaboradorunidade__id']
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
        self.nav_path = [{"nome": "Organização", 'href:': "#", 'ativo': False, 'options': None},
                         {"nome": self.unidade.nome_unidade,
                          'href': resolve_url('Pessoas:Colaboradores Unidade', slug_unidade=self.unidade.slug),
                          'ativo': False, 'options': None},
                         {"nome": self.setor.nome_setor,
                          'href': resolve_url('Pessoas:Colaboradores Setor', slug_unidade=self.unidade.slug,
                                              slug_setor=self.setor.slug), 'ativo': False, 'options': None},
                         {"nome": "Vincular Colaboradores", 'href:': "#", 'ativo': True, 'options': None}

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
        print('processar_post', post)
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

