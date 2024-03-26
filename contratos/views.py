from datetime import date

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, redirect, resolve_url
from django.views import View
from validate_docbr import CNPJ

from comuns.models import Fornecedor
from contratos.ferramentas.aditivos import DadosAditivoContrato
from contratos.ferramentas.contratos import dados_contratos, buscar_lotes_contrato, buscar_ultimo_aditivo_contrato, \
    dados_item_contrato
from contratos.ferramentas.licitacao import DadosLoteLicitacao, DadosItemLicitacao
from contratos.forms import FornecedorForm, FornecedorAtualizar, NovaLicitacao
from contratos.models import (Licitacao, LoteLicitacao, LoteContrato, ItemLoteContrato, ItemLoteLicitacao,
                              UnidadesMedida, Contrato, AditivoContrato, LoteAditivoContrato, AditivoQuantidade,
                              ItemLoteAditivo, QuantidadeAditivada)
from pessoas.models import Unidade, PessoaFisicaUsuario


# Create your views here.

def inicio(request):
    cpf_usuario = PessoaFisicaUsuario.objects.get(usuario=request.user)
    unidade_usuario = Unidade.objects.filter(
        vinculocolaboradorunidade__vinculo_funcional__profissional__pessoa_fisica=cpf_usuario.pessoa_fisica).first()
    return redirect("Contratos:Contratos Unidade", slug_unidade=unidade_usuario.slug)


class BaseViewContrato(LoginRequiredMixin, View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.unidade = None
        self.unidades = None
        self.context = None
        self.nav_path = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        cpf_usuario = PessoaFisicaUsuario.objects.get(usuario=request.user)

        if 'slug_unidade' in kwargs:
            self.unidade = Unidade.objects.get(slug=kwargs['slug_unidade'])
        else:
            self.unidade = Unidade.objects.filter(
                vinculocolaboradorunidade__vinculo_funcional__profissional__pessoa_fisica=cpf_usuario.pessoa_fisica
            ).first()

        unidades = Unidade.objects.filter(
            vinculocolaboradorunidade__vinculo_funcional__profissional__pessoa_fisica=cpf_usuario.pessoa_fisica
        ).values('id', 'nome_unidade', 'sigla_unidade', 'slug').distinct()

        self.unidades = [self.dados_unidade(u) for u in unidades]
        self.context = {'unidade': self.unidade, 'unidades': self.unidades, 'nav_path': self.nav_path}

    def dados_unidade(self, u):
        u['ativa'] = False if not self.unidade else (True if u['id'] == self.unidade.id else False)
        return u


class Fornecedores(BaseViewContrato):
    def get(self, request, *args, **kwargs):
        fornecedores = Fornecedor.objects.filter().values(
            'id', 'razao_social_fornecedor', 'cnpj_fornecedor', 'slug').order_by('razao_social_fornecedor')

        self.context['fornecedores'] = fornecedores

        return render(request, 'contratos/fornecedores/fornecedores.html', self.context)


class NovoFornecedor(BaseViewContrato):
    def get(self, request, *args, **kwargs):
        self.context['form'] = FornecedorForm()
        return render(request, 'contratos/fornecedores/novo_fornecedor.html', self.context)

    def post(self, request, *args, **kwargs):
        form = FornecedorForm(request.POST)
        print(form)
        print(form.data)
        cnpj_cadastrado = form.data['cnpj_fornecedor']
        print(cnpj_cadastrado, type(cnpj_cadastrado))

        if form.is_valid():
            validar_cpf = CNPJ().validate(cnpj_cadastrado)
            print("validar_cpf", validar_cpf)
            if CNPJ().validate(doc=cnpj_cadastrado) is True:
                if Fornecedor.objects.filter(cnpj_fornecedor=cnpj_cadastrado).exists():
                    fc = Fornecedor.objects.get(cnpj_fornecedor=cnpj_cadastrado)
                    messages.error(request, f"O fornecedor {fc} ja esta cadastrado com esse CNPJ")
                else:
                    form.save(commit=True)
                    messages.success(
                        request, f"Fornecedor {form.data['razao_social_fornecedor']} Cadastrado com sucesso")
            else:
                messages.error(request, "CNPJ Inválido")
                self.context['form'] = form
                return render(request, 'contratos/fornecedores/novo_fornecedor.html', self.context)

        else:
            self.context['form'] = form
            return render(request, 'contratos/fornecedores/novo_fornecedor.html', self.context)

        return redirect('Contratos:Fornecedores')


class NovoContrato(BaseViewContrato):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.licitacao = None
        self.fornecedor = None
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        if "slug_fornecedor" in kwargs.keys():
            self.fornecedor = Fornecedor.objects.get(slug=kwargs['slug_fornecedor'])
            self.context['fornecedor'] = self.fornecedor
        if 'slug_licitacao' in kwargs.keys():
            self.licitacao = Licitacao.objects.get(slug=kwargs['slug_licitacao'])
            self.context['licitacao'] = self.licitacao

        self.context['options_licitacao'] = [] if self.licitacao else Licitacao.objects.filter(
            cadastro_finalizado=True).values('numero_licitacao', 'modalidade_licitacao__nome_modalidade', 'id')
        self.context['options_fornecedores'] = [] if self.fornecedor else Fornecedor.objects.filter(
        ).values('razao_social_fornecedor', 'cnpj_fornecedor', 'id')

    def get(self, request, *args, **kwargs):

        return render(request, 'contratos/contratos/novo_contrato.html', self.context)

    def validar_dados_contrato_salvar(self, request, post):
        errors = []

        # Valida se fornecedor_contratado é um número inteiro
        fornecedor_id = post.get('fornecedor_contratado')
        if not fornecedor_id.isdigit():
            errors.append('Informe um fornecedor para salvar o contrato')

        # Valida se licitacao_referencia é um número inteiro
        licitacao_id = post.get('licitacao_referencia')
        if not licitacao_id.isdigit():
            errors.append('Informe uma licitacao para salvar o contrato')

        # Valida se numero_contrato é fornecido
        if not post.get('numero_contrato'):
            errors.append('Informe o numero do contrato')

        # Valida se inicio_vigencia e fim_vigencia são datas válidas
        try:
            inicio_vigencia = date.fromisoformat(post.get('inicio_vigencia'))
            fim_vigencia = date.fromisoformat(post.get('fim_vigencia'))
            if fim_vigencia <= inicio_vigencia:
                errors.append('A data de fim de vigência deve ser maior que a data de início.')
        except ValueError:
            errors.append('As datas de início e fim de vigência são inválidas.')
        for error in errors:
            messages.error(request, error)

        # Retorna True se não houver erros, False caso contrário
        return not errors

    def post(self, request, *args, **kwargs):
        post = request.POST

        if self.validar_dados_contrato_salvar(request, post):
            fornecedor_contratado = Fornecedor.objects.get(id=int(post.get('fornecedor_contratado')))
            licitacao_referencia = Licitacao.objects.get(id=int(post.get('licitacao_referencia')))
            numero_contrato = post.get('numero_contrato')
            inicio_vigencia = date.fromisoformat(post.get('inicio_vigencia'))
            fim_vigencia = date.fromisoformat(post.get('fim_vigencia'))

            contrato_salvar = Contrato(unidade_contrato=self.unidade,
                                       numero_contrato=numero_contrato,
                                       licitacao_referencia=licitacao_referencia,
                                       fornecedor_contratado=fornecedor_contratado,
                                       inicio_vigencia=inicio_vigencia,
                                       fim_vigencia=fim_vigencia,
                                       )
            contrato_salvar.save()
            return redirect('Contratos:Contrato', slug_contrato=contrato_salvar.slug)
        else:
            return render(request, 'contratos/contratos/novo_contrato.html', self.context)


class ViewFornecedor(BaseViewContrato):
    def get(self, request, *args, **kwargs):
        fornecedor = Fornecedor.objects.get(slug=kwargs['slug_fornecedor'])
        self.context['fornecedor'] = fornecedor
        self.context['contratos'] = dados_contratos(Contrato.objects.filter(fornecedor_contratado=fornecedor))

        ################# NAVPATH #########################
        self.nav_path = [{"nome": "Fornecedores",
                          'href': resolve_url("Contratos:Fornecedores"),
                          'ativo': False, 'options': None},
                         {"nome": fornecedor.razao_social_fornecedor, 'href': "#", 'ativo': True, 'options': None}]
        self.context['nav_path'] = self.nav_path

        self.context['form'] = FornecedorAtualizar(instance=fornecedor)
        return render(request, 'contratos/fornecedores/fornecedor.html', self.context)

    def post(self, request, *args, **kwargs):

        fornecedor = Fornecedor.objects.get(slug=kwargs['slug_fornecedor'])
        form = FornecedorAtualizar(request.POST, instance=fornecedor)

        if form.is_valid():
            form.save()
            messages.success(request, 'Informações Atualizadas com sucesso')
        else:
            messages.error(request, "Informações inválidas")

        return redirect('Contratos:Fornecedor', slug_fornecedor=kwargs['slug_fornecedor'])


class LicitacoesUnidade(BaseViewContrato):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.context['licitacoes'] = Licitacao.objects.filter(unidades=self.unidade)

    def get(self, request, *args, **kwargs):
        ################# NAVPATH #########################
        self.nav_path = [{"nome": "Licitações",
                          'href': resolve_url("Contratos:Licitacoes Unidade", slug_unidade=kwargs['slug_unidade']),
                          'ativo': False, 'options': None},
                         {"nome": self.unidade.sigla_unidade,
                          'href': resolve_url("Contratos:Licitacoes Unidade", slug_unidade=kwargs['slug_unidade']),
                          'ativo': True, 'options': None}
                         ]
        self.context['nav_path'] = self.nav_path
        self.context['form'] = NovaLicitacao()

        return render(request, 'contratos/licitacoes/licitacoes_unidade.html', self.context)

    def post(self, request, *args, **kwargs):

        form = NovaLicitacao(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Licitação cadastrada com sucesso')
            return redirect('Contratos:Licitacoes Unidade', slug_unidade=kwargs['slug_unidade'])
        else:
            messages.error(request, "Informações inválidas")
            return redirect('Contratos:Licitacoes Unidade', slug_unidade=kwargs['slug_unidade'])


class LicitacaoUnidade(BaseViewContrato):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lotes_licitacao = None

    def adicionar_item_lote_licitacao(self, request, post):
        print(post)
        lote_licitacao = LoteLicitacao.objects.get(
            id=int(post['id_lote_licitacao_alterar']), licitacao_referencia=self.context['licitacao'])
        numero_item = int(post['numero_item'])
        unidade_medida = post['unidadeMedida']
        descricao = post['descricao_item_salvar']
        quantidade = float(post['quantidade_licitada_salvar'])
        valor = float(post['valor_licitado_salvar'])

        dados_setornar = {'numero_lote': lote_licitacao.numero_lote,
                          'idLote': lote_licitacao.id, 'numeroItemLote': numero_item,
                          'numeroItemLoteLinha': post['numeroItemLote']}

        print(unidade_medida)

        var_num_item = ItemLoteLicitacao.objects.filter(lote_licitacao_refecencia=lote_licitacao,
                                                numero_item=int(post['numero_item'])).count()

        item_licitacao = ItemLoteLicitacao(
            numero_item=numero_item, descricao_item=descricao, unidade=self.unidade, var_num_item=var_num_item,
            lote_licitacao_refecencia=lote_licitacao, quantidade_licitada=quantidade, valor_licitado=valor,
            unidade_medida=unidade_medida)
        item_licitacao.save()

        dados_setornar['status'] = 'success'


        max_var_i = ItemLoteLicitacao.objects.filter(
            numero_item=numero_item, lote_licitacao_refecencia=lote_licitacao).aggregate(max=Max('var_num_item'))['max']

        dados_setornar['item_salvo'] = DadosItemLicitacao(item_licitacao).dados_item_licitacao(max_var_i)

        return JsonResponse(dados_setornar,
                            safe=False)
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.context['licitacoes'] = Licitacao.objects.filter(unidades=self.unidade)
        self.context['licitacao'] = Licitacao.objects.get(slug=kwargs['slug_licitacao'])
        self.context['unidadesMedida'] = [list(z) for z in zip(UnidadesMedida.values, UnidadesMedida.labels)]
        print(self.context['unidadesMedida'])

        self.lotes_licitacao = LoteLicitacao.objects.filter(
            licitacao_referencia=self.context['licitacao']
        ).values('id', 'numero_lote', 'descricao_lote')
        self.context['lotes_licitacao'] = [DadosLoteLicitacao(lote_licitacao=l).dados_lote_licitacao() for l in self.lotes_licitacao]

        print(self.context['lotes_licitacao'])

    def get(self, request, *args, **kwargs):
        self.nav_path = [{"nome": "Licitações",
                          'href': resolve_url("Contratos:Licitacoes Unidade", slug_unidade=kwargs['slug_unidade']),
                          'ativo': False, 'options': None},
                         {"nome": self.unidade.sigla_unidade,
                          'href': resolve_url("Contratos:Licitacoes Unidade", slug_unidade=kwargs['slug_unidade']),
                          'ativo': False, 'options': None},
                         {"nome": f'{self.context['licitacao'].modalidade_licitacao} {self.context['licitacao'].numero_licitacao}',
                          'href': resolve_url("Contratos:Licitacoes Unidade", slug_unidade=kwargs['slug_unidade']),
                          'ativo': True, 'options': None}
                         ]
        self.context['nav_path'] = self.nav_path

        return render(request, 'contratos/licitacoes/licitacao_unidade.html', self.context)

    def processar_post(self, request, *args, **kwargs):
        post = request.POST.copy().dict()
        tipos_acao = {"cadastrarNovoLote": self.cadastrar_novo_lote,
                      'adicionarItemLoteLicitacao': self.adicionar_item_lote_licitacao,
                      'excluirItemLoteLicitacao': self.excluir_item_lote_licitacao,
                      'excluirLoteLicitacao': self.excluir_lote_licitacao,
                      'finalizarEdicaoLicitacao': self.finalizar_edicao_licitacao,
                      }
        return tipos_acao[post['tipo-acao']](request, post)

    def excluir_item_lote_licitacao(self, request, post):
        item_licitacao = ItemLoteLicitacao.objects.get(id=post['idItemLoteExcluir'])
        id_lote = item_licitacao.lote_licitacao_refecencia.id
        try:
            item_licitacao.delete()
            return JsonResponse({'status': 'success',
                                 'idItemLoteExcluir': post['idItemLoteExcluir'],
                                 'idLoteExcluido': id_lote})
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)}, safe=False)

    def finalizar_edicao_licitacao(self, request, post):
        self.context['licitacao'].cadastro_finalizado = True
        self.context['licitacao'].save()
        return redirect("Contratos:Licitacao Unidade", slug_unidade=self.unidade.slug,
                        slug_licitacao=self.context['licitacao'].slug)


    def excluir_lote_licitacao(self, request, post):
        loteLicitacao = LoteLicitacao.objects.get(id=post['id_lote_licitacao_excluir'])

        try:
            loteLicitacao.delete()
            return JsonResponse({'status': 'success',
                                 'id_lote_licitacao_excluir': post['id_lote_licitacao_excluir']})
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)}, safe=False)


    def cadastrar_novo_lote(self, request, post):
        lista_lotes = zip(request.POST.getlist('numeroLote'), request.POST.getlist('descricaoLote'))

        for l in lista_lotes:
            if not LoteLicitacao.objects.filter(numero_lote=int(l[0]),
                                              licitacao_referencia=self.context['licitacao']).exists():
                ls = LoteLicitacao.objects.create(numero_lote=int(l[0]),
                                                  descricao_lote=l[1],
                                                  licitacao_referencia=self.context['licitacao'])
            else:
                messages.error(request, f"Ja existe um lote com o numero {l[0]} para esta licitação.")



        return redirect("Contratos:Licitacao Unidade", slug_unidade=self.unidade.slug,
                        slug_licitacao=self.context['licitacao'].slug)

    def post(self, request, *args, **kwargs):

        return self.processar_post(request, *args, **kwargs)


class ContratosUnidade(BaseViewContrato):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.context['contratos'] = dados_contratos(Contrato.objects.filter(unidade_contrato=self.unidade))

        self.nav_path = [{"nome": "Contratos",
                          'href': resolve_url("Contratos:Contratos Unidade", slug_unidade=self.unidade.slug),
                          'ativo': True, 'options': None},
                         ]
        self.context['nav_path'] = self.nav_path

        print(self.context['contratos'])

    def get(self, request, *args, **kwargs):
        return render(request, 'contratos/contratos_unidade.html', self.context)


class DetalhesContrato(BaseViewContrato):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.contrato = None
        self.licitacao = None
        self.uac = None

        self.visualizacoes = None

        self.acoes_contrato = None

        self.itens_cadastrar = None
        self.itens_cadastrados = None
        self.lotes_contratados = None

        self.possui_itens_cadastrar = False

        self.ultimo_aditivo_contrato = None
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.contrato = Contrato.objects.get(slug=kwargs['slug_contrato'])
        self.uac = buscar_ultimo_aditivo_contrato(self.contrato)
        self.licitacao = self.contrato.licitacao_referencia
        self.context['contrato'] = self.contrato
        self.context['tipos_aditivo'] = AditivoContrato.TIPO_ADITIVO_CHOICES
        self.lotes_contratados = buscar_lotes_contratados(self.contrato)
        self.lotes_contrataveis = buscar_lotes_contrataveis(self.contrato, self.lotes_contratados)
        self.definir_acoes_contrato()

        self.nav_path = [{"nome": "Contratos",
                          'href': resolve_url("Contratos:Contratos Unidade", slug_unidade=self.unidade.slug),
                          'ativo': False, 'options': None},
                         {"nome": f"{self.licitacao.modalidade_licitacao} - {self.licitacao.numero_licitacao}",
                          'href': resolve_url("Contratos:Licitacao Unidade", slug_unidade=self.unidade.slug,
                                              slug_licitacao=self.licitacao.slug),
                          'ativo': False, 'options': None},
                         {"nome": f"{self.contrato.numero_contrato} - {self.contrato.fornecedor_contratado.razao_social_fornecedor}",
                          'href': resolve_url("Contratos:Fornecedor",
                                              slug_fornecedor=self.contrato.fornecedor_contratado.slug)
                             , 'ativo': False, 'options': None}]
        self.context['nav_path'] = self.nav_path

        self.context['lotes_contratados'] = []
        self.context['acoes_contrato'] = self.acoes_contrato

        self.context['lotes_contratados'], self.context['lotes_contrataveis'] = buscar_lotes_contrato(self.contrato)

    class Acoes:
        desvincular_profissional = {"value": "desvincular_profissional",
                                    "label": "Desvincular Profissional",
                                    "js_function": "desvinculaProfissional()",
                                    }
        finalizar_cadastro_contrato = {"value": "finalizar_cadastro_contrato",
                                       "label": "Finalizar Cadastro",
                                       "js_function": "finalizarCadastroContrato()"}
        rescindir_contrato = {"value": "rescindir_contrato",
                              "label": "Rescindir Contrato",
                              "js_function": "rescindirContrato()"}
        apagar_contrato = {"value": "apagar_contrato",
                           "label": "Apagar Contrato",
                           "js_function": "apagarContrato()"}
        adicionar_lote = {"value": "adicionar_lote",
                          "label": "Adicionar Lote",
                          "js_function": "adicionarLote()"}
        aditivar_contrato = {"value": "aditivar_contrato",
                             "label": "Aditivar Contrato",
                             "js_function": "aditivarContrato()"}
        finalizar_aditivo_quantidade = {"value": "finalizar_aditivo_quantidade",
                                        "label": "Concluir Aditivo Quantidade",
                                        "js_function": "finalizarAditivoQuantidade(this)",
                                        }
        cancelar_aditivo_quantidade = {"value": "cancelar_aditivo_quantidade",
                                       "label": "Cancelar Aditivo Quantidade",
                                       "js_function": "cancelarAditivoQuantidade(this)"}

    def definir_acoes_contrato(self):
        ### Simplificar essa função.
        match self.contrato.status:
            case Contrato.StatusChoices.CADASTRO:
                self.acoes_contrato = [self.Acoes.adicionar_lote, self.Acoes.finalizar_cadastro_contrato,
                                       self.Acoes.apagar_contrato]
            case Contrato.StatusChoices.VIGENTE:
                self.acoes_contrato = [self.Acoes.aditivar_contrato, self.Acoes.rescindir_contrato]
            case Contrato.StatusChoices.VIGENTE_ADITIVADO:
                self.acoes_contrato = self.acoes_contrato = None if self.uac.aditivo_editavel else [self.Acoes.aditivar_contrato,
                                                                              self.Acoes.rescindir_contrato]
            case Contrato.StatusChoices.ADITIVO_QUANTIDADE:
                if self.uac:
                    print("self.uac", self.uac)
                    self.acoes_contrato = [self.Acoes.finalizar_aditivo_quantidade,
                                      self.Acoes.cancelar_aditivo_quantidade] if AditivoQuantidade.objects.get(
                        aditivo_referencia=self.uac).aditivo_editavel else [
                        self.Acoes.aditivar_contrato, self.Acoes.rescindir_contrato]
                else:
                    print("self.uac 2", self.uac)
                    aditivo_quantidade = AditivoQuantidade.objects.get(
                        contrato_referencia=self.contrato)
                    print(aditivo_quantidade.aditivo_editavel)
                    self.acoes_contrato = [self.Acoes.finalizar_aditivo_quantidade,
                                      self.Acoes.cancelar_aditivo_quantidade
                                           ] if aditivo_quantidade.aditivo_editavel else [
                        self.Acoes.aditivar_contrato, self.Acoes.rescindir_contrato]

            case Contrato.StatusChoices.ENCERRADO:
                self.acoes_contrato = []
            case Contrato.StatusChoices.RESCINDIDO:
                self.acoes_contrato = []

    def processar_post(self, request, *args, **kwargs):
        post = request.POST.copy().dict()
        print(post)
        tipos_acao = {"AdicionarLotes": self.adicionar_lotes,
                      "adicionar-item-lote-contratado": self.adicionar_item_lote_contratado,
                      "excluir-item-lote-contratado": self.excluir_item_lote_contratado,
                      "excluir-lote-contratado": self.excluir_lote_contratado,
                      'finalizar_cadastro_contrato': self.finalizar_cadastro_contrato,
                      'rescindir_contrato': self.rescindir_contrato,
                      'apagar_contrato': self.apagar_contrato,
                      'aditivar_contrato': self.aditivar_contrato,
                      "aditivar-suprimir-quantidade-contratada": self.aditivar_suprimir_quantidade,
                      "salvar-item-lote-aditivo": self.salvar_item_lote_aditivo,
                      "excluir-item-lote-aditivo": self.excluir_item_lote_aditivo,
                      'adicionarLotesAditivo': self.adicionar_lotes_aditivo,
                      "excluir-lote-aditivo": self.excluir_lote_aditivo,
                      "cancelarAditivo": self.cancelar_aditivo,
                      "FinalizarEdicaoAditivo": self.Finalizar_edicao_aditivo,
                      'atualizar-item-aditivo-quantidade': self.atualizar_item_aditivo_quantidade,
                      "finalizar-aditivo-quantidade": self.finalizar_aditivo_quantidade,
                      "cancelar-aditivo-quantidade": self.cancelar_aditivo_quantidade,
                      }
        return tipos_acao[post['tipo-acao']](request, post)

    def atualizar_item_aditivo_quantidade(self, request, post):
        aditivo_quantidade = AditivoQuantidade.objects.get(id=int(post['id-aditivo-quantidade']))
        if aditivo_quantidade.contrato_referencia == self.contrato and aditivo_quantidade.aditivo_editavel:
            if aditivo_quantidade.aditivo_referencia:
                item_atualizar = ItemLoteAditivo.objects.get(id=int(post['id-item']))
                quantidade_atual = item_atualizar.quantidade_aditivada
                print("QA: ", quantidade_atual)
                quantidade_aditivada, created = QuantidadeAditivada.objects.update_or_create(
                    aditivo=aditivo_quantidade,
                    item_aditivo=item_atualizar,
                    defaults={'quantidade_aditivada': float(post['quantidade-atualizada'])},
                    create_defaults={
                        'aditivo': aditivo_quantidade,
                        'item_aditivo': item_atualizar,
                        'quantidade_original': quantidade_atual,
                        'quantidade_aditivada': float(post['quantidade-atualizada'])}
                )

                item_atualizar.quantidade_aditivada = float(post['quantidade-atualizada'])
                item_atualizar.save()

            else:
                item_atualizar = ItemLoteContrato.objects.get(id=int(post['id-item']))
                quantidade_atual = item_atualizar.quantidade_contratada

                quantidade_aditivada, created = QuantidadeAditivada.objects.update_or_create(
                    aditivo=aditivo_quantidade,
                    item_contrato=item_atualizar,
                    defaults={'quantidade_aditivada': float(post['quantidade-atualizada'])},
                    create_defaults={
                        'aditivo': aditivo_quantidade,
                        'item_contrato': item_atualizar,
                        'quantidade_original': quantidade_atual,
                        'quantidade_aditivada': float(post['quantidade-atualizada'])
                    }
                )
                item_atualizar.quantidade_contratada = float(post['quantidade-atualizada'])
                item_atualizar.save()

            return JsonResponse({"status": "success", "idIconeAtualizar": post['idIconeAtualizar']})
        else:
            return JsonResponse({"status": "error"})

    def finalizar_aditivo_quantidade(self, request, post):
        aditivo_quantidade = AditivoQuantidade.objects.get(id=int(post['id-aditivo-quantidade']))
        aditivo_quantidade.aditivo_editavel = False
        aditivo_quantidade.save()

        return JsonResponse({"status": "success"})

    def cancelar_aditivo_quantidade(self, request, post):
        aditivo_quantidade = AditivoQuantidade.objects.get(id=int(post['id-aditivo-quantidade']))
        print(aditivo_quantidade)
        self.contrato.status = Contrato.StatusChoices.VIGENTE_ADITIVADO if aditivo_quantidade.aditivo_referencia else Contrato.StatusChoices.VIGENTE
        iaqs = QuantidadeAditivada.objects.filter(aditivo=aditivo_quantidade)

        for i in iaqs:
            print(i)
            if aditivo_quantidade.aditivo_referencia:
                ia = i.item_aditivo
                ia.quantidade_aditivada = i.quantidade_original
                ia.save()
            else:
                ic = i.item_contrato
                ic.quantidade_contratada = i.quantidade_original
                ic.save()
            i.delete()
        aditivo_quantidade.delete()
        self.contrato.save()
        return JsonResponse({'status': 'success'})

    def excluir_lote_aditivo(self, request, post):
        lac = LoteAditivoContrato.objects.get(id=int(post['id-lote-aditivo-excluir']))
        if self.contrato.id == int(post['id-contrato']) == lac.aditivo_referencia.contrato_referencia.id:
            lac.delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error',
                                 'error-message': "não foi possivel excluir o item, verifique os dados do contrato"})

    def cancelar_aditivo(self, request, post):
        ac = AditivoContrato.objects.get(id=int(post['id-aditivo']))
        if self.contrato.id == int(post['id-contrato']) == ac.contrato_referencia.id:
            ac.delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error',
                                 'error-message': "não foi possivel excluir o aditivo, verifique os dados do contrato"})

    def Finalizar_edicao_aditivo(self, request, post):
        ac = AditivoContrato.objects.get(id=int(post['id-aditivo']))
        if self.contrato.id == int(post['id-contrato']) == ac.contrato_referencia.id:
            ac.aditivo_editavel = False
            ac.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error',
                                 'error-message': "não foi finalizar o aditivo, verifique os dados do contrato"})

    def finalizar_cadastro_contrato(self, request, post):
        if self.contrato.id == int(post['id-contrato-finalizar-cadastro']):
            self.contrato.status = Contrato.StatusChoices.VIGENTE
            self.contrato.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error'})

    def adicionar_lotes_aditivo(self, request, post):
        ad = AditivoContrato.objects.get(id=post['id_aditivo'])
        id_lotes_aditivo = request.POST.getlist('id-lotes-aditivados')
        if self.contrato.id == int(post['id-contrato']) == ad.contrato_referencia.id:
            for il in id_lotes_aditivo:
                ll = LoteLicitacao.objects.get(id=int(il))
                lc, lcc = LoteContrato.objects.get_or_create(contrato_referencia=self.contrato, lote_referencia=ll)
                la, lac = LoteAditivoContrato.objects.get_or_create(aditivo_referencia=ad, lote_contrato_referencia=lc)
                messages.success(request, f"Lote {ll.numero_lote} adicionado ao aditivo com sucesso.")

            return redirect("Contratos:Contrato", slug_contrato=self.contrato.slug)
        else:
            messages.error(request, "Informações de contrato e aditivo inválidas")
            return redirect("Contratos:Contrato", slug_contrato=self.contrato.slug)


    def excluir_item_lote_aditivo(self, request, post):
        item_aditivo_excluir = ItemLoteAditivo.objects.get(id=post['id-item-lote-aditivo-excluir'])
        id_lote_contrato = item_aditivo_excluir.lote_aditivo_referencia.id
        id_aditivo = item_aditivo_excluir.lote_aditivo_referencia.aditivo_referencia.id
        if item_aditivo_excluir.lote_aditivo_referencia.aditivo_referencia.aditivo_editavel:

            item_licitacao = DadosAditivoContrato.dados_item_aditivo(
                {'id_item_lote_licitacao': item_aditivo_excluir.item_contrato_referencia.item_licitacao_referencia.id,
                 'numero_item': item_aditivo_excluir.item_contrato_referencia.item_licitacao_referencia.numero_item,
                 'descricao_item': item_aditivo_excluir.item_contrato_referencia.item_licitacao_referencia.descricao_item,
                 'unidade_medida': item_aditivo_excluir.item_contrato_referencia.item_licitacao_referencia.unidade_medida,
                 'quantidade_contratada': item_aditivo_excluir.quantidade_aditivada,
                 'valor_item': item_aditivo_excluir.preco_aditivado,
                 "var_num_item": item_aditivo_excluir.item_contrato_referencia.item_licitacao_referencia.var_num_item,
                 }, 1
            )
            item_aditivo_excluir.delete()
            return JsonResponse({'status': 'success',
                                 'idLoteContrato': id_lote_contrato,
                                 "idAditivo": id_aditivo,
                                 'itemLicitacao': item_licitacao})
        else:
            return JsonResponse({'status': 'error',
                                 'error-message': "não foi possivel excluir o item, verifique o status do aditivo"})

    def rescindir_contrato(self, request, post):
        if self.contrato.id == int(post['id-contrato']) and post['input_motivo_rescisao']:
            self.contrato.motivo_rescisao = post['input_motivo_rescisao']
            self.contrato.status = Contrato.StatusChoices.RESCINDIDO
            self.contrato.save()
            messages.success(request, "Contrato rescindico com sucesso")
            return redirect("Contratos:Contrato", slug_contrato=self.contrato.slug)
        else:
            messages.error(request, "Não foi possivel rescindir o contrato, verifique as informações digitadas")
            return redirect("Contratos:Contrato", slug_contrato=self.contrato.slug)

    def apagar_contrato(self, request, post):
        id_contrato = int(post['id-contrato'])
        slug_fornecedor = self.contrato.fornecedor_contratado.slug
        if self.contrato.id == int(post['id-contrato']):
            self.contrato.delete()
            return redirect("Contratos:Fornecedor", slug_fornecedor=slug_fornecedor)
        else:
            messages.error(request, "Não foi possivel apagar o contrato")
            return redirect("Contratos:Contrato", slug_contrato=self.contrato.slug)

    def aditivar_contrato(self, request, post):
        if self.contrato.id == int(post['id-contrato']):
            self.contrato.aditivado = True
            self.contrato.status = Contrato.StatusChoices.VIGENTE_ADITIVADO
            tipo_aditivo_post = post['tipo_aditivo']
            if (tipo_aditivo_post, tipo_aditivo_post) in AditivoContrato.TIPO_ADITIVO_CHOICES:
                aditivo_cadastrar = AditivoContrato(contrato_referencia=self.contrato,
                                                    numero_aditivo=post['numero_aditivo'],
                                                    inicio_vigencia=post['inicio_vigencia'],
                                                    fim_vigencia=post['fim_vigencia'],
                                                    tipo_aditivo=tipo_aditivo_post)

                if aditivo_cadastrar.fim_vigencia >= aditivo_cadastrar.inicio_vigencia:
                    aditivo_cadastrar.save()
                    self.contrato.save()

                    lotes_contrato = LoteContrato.objects.filter(contrato_referencia=self.contrato)
                    for lote_contrato in lotes_contrato:
                        LoteAditivoContrato.objects.create(aditivo_referencia=aditivo_cadastrar,
                                                           lote_contrato_referencia=lote_contrato)

                    messages.success(self.request, "Contrato aditivado com sucesso!")
                    print(aditivo_cadastrar.inicio_vigencia, type(aditivo_cadastrar.inicio_vigencia))
                else:
                    messages.error(self.request, "Datas Inválidas")
            else:
                messages.error(self.request, "o tipo do aditivo não é valido")

        else:
            messages.error(self.request, "Não foi possivel aditivar o contrato")
        return redirect("Contratos:Contrato", slug_contrato=self.contrato.slug)

    def aditivar_suprimir_quantidade(self, request, post):
        if self.contrato.id == int(post['id-contrato']):
            self.contrato.aditivado = True
            self.contrato.status = Contrato.StatusChoices.ADITIVO_QUANTIDADE
            tipo_aditivo_post = post['tipo_aditivo']
            if (tipo_aditivo_post, tipo_aditivo_post) in AditivoContrato.TIPO_ADITIVO_CHOICES:
                aditivo_quantidade = AditivoQuantidade(contrato_referencia=self.contrato,
                                                       numero_aditivo=post['numero_aditivo'],
                                                       tipo_aditivo=tipo_aditivo_post)

                if self.uac:
                    aditivo_quantidade.aditivo_referencia=self.uac
                aditivo_quantidade.save()
                print(self.contrato)
                print(self.contrato.status)
                self.contrato.save()
                messages.success(self.request, "Contrato aditivado com sucesso!")
            else:
                messages.error(self.request, "Erro ao salvar aditivo, os dados informados são inválidos")
        else:
            messages.error(self.request, "Erro ao salvar aditivo, os dados de contrato são inválidos")

        return redirect('Contratos:Contrato', slug_contrato=self.contrato.slug)

    def salvar_item_lote_aditivo(self, request, post):
        aditivo = AditivoContrato.objects.get(id=int(post['id-aditivo']))
        if aditivo.contrato_referencia.id == int(post['id-contrato']) == self.contrato.id:
            item_licitacao = ItemLoteLicitacao.objects.get(id=post['idItemLoteLicitacao'])
            lote_contrato, lcc = LoteContrato.objects.get_or_create(
                contrato_referencia=self.contrato, lote_referencia=item_licitacao.lote_licitacao_refecencia)

            item_lote_contrato, ilcc = ItemLoteContrato.objects.get_or_create(
                lote_contrato_referencia=lote_contrato, item_licitacao_referencia=item_licitacao,
                defaults={"valor_item": 0, "quantidade_contratada": 0, 'ativo': False})

            lote_aditivo = LoteAditivoContrato.objects.get(aditivo_referencia=aditivo,
                                                           lote_contrato_referencia=lote_contrato)

            item_lote_aditivo, created = ItemLoteAditivo.objects.get_or_create(
                lote_aditivo_referencia=lote_aditivo, item_contrato_referencia=item_lote_contrato,
            defaults={'quantidade_aditivada': float(post['quantidade-item-lote']),
                      'preco_aditivado': float(post['valor-item-lote']),
                      'item_aditivo_ativo': True})

            #return JsonResponse({'status': 'success'})

            max_item = ItemLoteAditivo.objects.filter(lote_aditivo_referencia=lote_aditivo).aggregate(
                max=Max('item_contrato_referencia__item_licitacao_referencia__var_num_item'))['max']

            item_retornar = DadosAditivoContrato.dados_item_aditivo(
                {'id': item_lote_aditivo.id,
                 'id_item_lote_licitacao': item_lote_aditivo.item_contrato_referencia.item_licitacao_referencia.id,
                 'numero_item': item_lote_aditivo.item_contrato_referencia.item_licitacao_referencia.numero_item,
                 "var_num_item": item_lote_aditivo.item_contrato_referencia.item_licitacao_referencia.var_num_item,
                 'unidade_medida': item_lote_aditivo.item_contrato_referencia.item_licitacao_referencia.unidade_medida,
                 'descricao_item': item_lote_aditivo.item_contrato_referencia.item_licitacao_referencia.descricao_item,
                 'valor_item': item_lote_aditivo.preco_aditivado,
                 'quantidade_contratada': item_lote_aditivo.quantidade_aditivada,
                 'ativo': item_lote_aditivo.item_aditivo_ativo,
                 'valor_total_faturado': [0, 0]
                 }, max_item)

            return JsonResponse({'status': 'success', "idItemLoteLicitacao": post['idItemLoteLicitacao'],
                                 "idLoteContrato": lote_aditivo.id,
                                 'itemContratado': item_retornar,
                                 "idAditivo": item_lote_aditivo.lote_aditivo_referencia.aditivo_referencia.id
                                 })
        else:
            return JsonResponse({'status': 'error', 'errorMessage': "Informações de contrato e aditivo inválidas"})

    def adicionar_item_lote_contratado(self, request, post):
        dados_item_post = {"item_lote_licitacao": ItemLoteLicitacao.objects.get(id=int(post['id-item-lote-licitacao'])),
                           'quantidade_contratada': float(post['quantidade-contratada']),
                           'valor_contratado': float(post['valor-contratado']),
                           "id_contrato": int(post['id-contrato'])}

        if d := self.validar_item_licitacao_contratar(dados_item_post):

            item_contrato, created = ItemLoteContrato.objects.update_or_create(
                lote_contrato_referencia=d[0]['lote_contrato_referencia'],
                item_licitacao_referencia=d[0]['item_licitacao_referencia'],
                defaults=d[1])

            max_item = ItemLoteContrato.objects.filter(
                lote_contrato_referencia=d[0]['lote_contrato_referencia']).aggregate(
                max=Max('item_licitacao_referencia__var_num_item'))['max']

            item_retornar = dados_item_contrato(
                {'id': item_contrato.id,
                 'item_licitacao_referencia__id': item_contrato.item_licitacao_referencia.id,
                 'numero_item': item_contrato.item_licitacao_referencia.numero_item,
                 'var_num_item': item_contrato.item_licitacao_referencia.var_num_item,
                 'unidade_medida': item_contrato.item_licitacao_referencia.unidade_medida,
                 'descricao_item': item_contrato.item_licitacao_referencia.descricao_item,
                 'valor_item': item_contrato.valor_item,
                 'quantidade_contratada': item_contrato.quantidade_contratada,
                 'ativo': item_contrato.ativo,
                 'valor_total_faturado': [0, 0]
                 }, max_item)

            return JsonResponse({'status': 'success', "idItemLoteLicitacao": post['id-item-lote-licitacao'],
                                 "idLoteContrato": d[0]['lote_contrato_referencia'].id, 'itemContratado': item_retornar,
                                 })
        else:
            return JsonResponse({'status': "error"})

    def excluir_item_lote_contratado(self, request, post):
        item_contrato = ItemLoteContrato.objects.get(id=int(post['id-item-lote-contratado']))

        if item_contrato.lote_contrato_referencia.contrato_referencia == self.contrato:
            item_contrato.ativo = False
            item_contrato.save()

            max_item = ItemLoteContrato.objects.filter(
                lote_contrato_referencia=item_contrato.lote_contrato_referencia).aggregate(
                max=Max('item_licitacao_referencia__var_num_item'))['max']

            item_retornar = dados_item_contrato(
                {'id': item_contrato.id,
                 'item_licitacao_referencia__id': item_contrato.item_licitacao_referencia.id,
                 'numero_item': item_contrato.item_licitacao_referencia.numero_item,
                 'var_num_item': item_contrato.item_licitacao_referencia.var_num_item,
                 'unidade_medida': item_contrato.item_licitacao_referencia.unidade_medida,
                 'descricao_item': item_contrato.item_licitacao_referencia.descricao_item,
                 'valor_item': item_contrato.valor_item,
                 'quantidade_contratada': item_contrato.quantidade_contratada,
                 'ativo': item_contrato.ativo,
                 'valor_total_faturado': [0, 0]
                 }, max_item)

            return JsonResponse({'status': 'success', "idItemLoteLicitacao": item_retornar['item_licitacao_referencia__id'],
                                 "idLoteContrato": item_contrato.lote_contrato_referencia.id,
                                 'itemContratado': item_retornar,
                                 })
        else:
            return JsonResponse({'status': 'error'})


    def excluir_lote_contratado(self, request, post):
        lote_contrato = LoteContrato.objects.get(id=int(post['id-lote-contratado']))
        if lote_contrato.contrato_referencia == self.contrato:
            lote_contrato.delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error'})

    def validar_item_licitacao_contratar(self, i):
        if (i['item_lote_licitacao'].lote_licitacao_refecencia.licitacao_referencia == self.licitacao and
                i['id_contrato'] == self.contrato.id):
            lote_contrato = LoteContrato.objects.get(
                contrato_referencia=self.contrato,
                lote_referencia=i['item_lote_licitacao'].lote_licitacao_refecencia)

            return ({'lote_contrato_referencia': lote_contrato,
                     "item_licitacao_referencia": i['item_lote_licitacao'],
                     },
                    {'valor_item': i['valor_contratado'],
                     "quantidade_contratada": i['quantidade_contratada'],
                     'ativo': True})
        else:
            return False


    def buscar_visualizacoes_contrato(self):
        self.visualizacoes = []

        vc = {"tipo": "contrato",
              "editavel": False,
              "id": self.contrato.id,
              'ativo': True,
              'lotes_contratados': [],
              'lotes_contrataveis': [],
              }
        vp = {"tipo": "profissional",
              "descricao": "Profissionais Habilitados",
              "editavel": False if self.contrato.status in self.contrato.STATUS_ENCERADOS else True,
              "id": "profissionais",
              'ativo': False,
              "profissionais_habilitados": [],
              'profissionais_habilitaveis': [],
              }

        if self.contrato.status == Contrato.StatusChoices.CADASTRO:
            vc['editavel'] = True

        vc['aditivo_quantidade'] = self.processar_aditivo_quantidade(None)
        if vc['aditivo_quantidade']:
            vc["descricao"] = "{0}º {1} ao contrato {2} - ({3} - {4})".format(
                vc['aditivo_quantidade']['numero_aditivo'],
                vc['aditivo_quantidade']['tipo_aditivo'],
                self.contrato.numero_contrato,
                self.contrato.inicio_vigencia.strftime('%d/%m/%y'),
                self.contrato.fim_vigencia.strftime('%d/%m/%y')
            )
            if vc['aditivo_quantidade']['editavel']:
                self.Acoes.finalizar_aditivo_quantidade[
                    'data_attr'] = f"data-idAditivoQuantidade={vc['aditivo_quantidade']['id']}"
                self.Acoes.cancelar_aditivo_quantidade[
                    'data_attr'] = f"data-idAditivoQuantidade={vc['aditivo_quantidade']['id']}"
                self.acoes_contrato = [self.Acoes.finalizar_aditivo_quantidade,
                                       self.Acoes.cancelar_aditivo_quantidade]
        else:
            iv = self.contrato.inicio_vigencia
            fv = self.contrato.fim_vigencia
            vc[
                "descricao"] = f"Contrato ({iv.strftime('%d/%m/%y')} - {fv.strftime('%d/%m/%y')})"

        aditivos_contrato = AditivoContrato.objects.filter(contrato_referencia=self.contrato).values(
            'id', 'numero_aditivo', 'tipo_aditivo', 'sequencia_aditivo', 'aditivo_editavel',
            'inicio_vigencia', 'fim_vigencia', 'aditivoquantidade', 'aditivoquantidade__aditivo_editavel')

        if aditivos_contrato.count() > 0:
            vc['ativo'] = False

        self.visualizacoes.append(vc)
        self.buscar_visualizacoes_aditivos(aditivos_contrato)
        self.visualizacoes.append(vp)

        self.context['visualizacoes_contrato'] = self.visualizacoes

    def buscar_visualizacoes_aditivos(self, aditivos_contrato):
        for aditivo in aditivos_contrato:

            va = {"tipo": "aditivo",
                  "editavel": aditivo['aditivo_editavel'],
                  'aditivo_quantidade': self.processar_aditivo_quantidade(aditivo['id']),
                  "id": aditivo['id'],
                  'ativo': False}
            if aditivo['id'] == self.uac.id:
                va['ativo'] = True
            if va['aditivo_quantidade']:
                va['descricao'] = "{0}º {1} ao {2}º {3} ({4} - {5})".format(
                    va['aditivo_quantidade']['numero_aditivo'],
                    va['aditivo_quantidade']['tipo_aditivo'],
                    aditivo['numero_aditivo'],
                    aditivo['tipo_aditivo'],
                    aditivo['inicio_vigencia'].strftime('%d/%m/%y'),
                    aditivo['fim_vigencia'].strftime('%d/%m/%y'))

                if va['aditivo_quantidade']['editavel']:
                    self.Acoes.finalizar_aditivo_quantidade[
                        'data_attr'] = f"data-idAditivoQuantidade={va['aditivo_quantidade']['id']}"
                    self.Acoes.cancelar_aditivo_quantidade[
                        'data_attr'] = f"data-idAditivoQuantidade={va['aditivo_quantidade']['id']}"
                    self.acoes_contrato = [self.Acoes.finalizar_aditivo_quantidade,
                                           self.Acoes.cancelar_aditivo_quantidade]
            else:
                va['descricao'] = "{0}º {1} ({2} - {3})".format(
                    aditivo['numero_aditivo'], aditivo['tipo_aditivo'], aditivo['inicio_vigencia'].strftime('%d/%m/%y'),
                    aditivo['fim_vigencia'].strftime('%d/%m/%y'))

            va['lotes_visualizacao'] = DadosAditivoContrato(self.contrato, aditivo).processar_lotes_aditivados()
            va['lotes_contrataveis'] = DadosAditivoContrato(self.contrato, aditivo).processar_lotes_contrataveis()
            va['faturas_contrato'] = []#self.buscar_faturas(AditivoContrato.objects.get(id=aditivo['id']))

            #va['controle_faturas_contrato'] = controle_saldo_itens_contrato(self.contrato, AditivoContrato.objects.get(id=aditivo['id']))
            self.visualizacoes.append(va)

    def processar_aditivo_quantidade(self, id_aditivo):
        if AditivoQuantidade.objects.filter(contrato_referencia=self.contrato, aditivo_referencia__id=id_aditivo).exists():
            seq_ua = AditivoQuantidade.objects.filter(
                contrato_referencia=self.contrato, aditivo_referencia__id=id_aditivo
            ).aggregate(Max('sequencia_aditivo'))['sequencia_aditivo__max']

            aditivo_quantidade = AditivoQuantidade.objects.get(
                contrato_referencia=self.contrato, aditivo_referencia__id=id_aditivo, sequencia_aditivo=seq_ua)
            return {
                'id': aditivo_quantidade.id,
                'numero_aditivo': aditivo_quantidade.numero_aditivo,
                'tipo_aditivo': aditivo_quantidade.tipo_aditivo,
                'editavel': aditivo_quantidade.aditivo_editavel,
            }
        else:
            return None

    def adicionar_lotes(self, request, post):
        contrato_postado = Contrato.objects.get(id=int(post['id_contrato']))
        lotes_contratados = request.POST.getlist("id_lotes_contratados")
        if len(lotes_contratados) == 0:
            messages.error(request, "Selecione ao menos um lote")
        if contrato_postado == self.contrato:
            for lote in lotes_contratados:
                lote_licitacao = LoteLicitacao.objects.get(
                    id=lote, licitacao_referencia=self.contrato.licitacao_referencia)
                dados_lote_contrato = {'contrato_referencia': self.contrato, 'lote_referencia': lote_licitacao}
                if not LoteContrato.objects.filter(**dados_lote_contrato).exists():
                    lote_contrato = LoteContrato.objects.create(**dados_lote_contrato)
                    messages.success(request, f"Lote {lote_licitacao.numero_lote} adicionados com sucesso")
        else:
            messages.error(request, "Erro ao adicionar os lotes, se o problema persistir, feche todas as janelas do navegador e tente novamente")
        return redirect('Contratos:Contrato', slug_contrato=self.contrato.slug)

    def get(self, request, *args, **kwargs):
        self.buscar_visualizacoes_contrato()

        return render(request, 'contratos/contratos/detalhes_contrato.html', self.context)

    def post(self, request, *args, **kwargs):

        return self.processar_post(request, *args, **kwargs)


def buscar_lotes_contratados(contrato):
    lotes_contrato = LoteContrato.objects.filter(contrato_referencia=contrato)

    return lotes_contrato


def buscar_lotes_contrataveis(contrato, lotes_contratados):
    lotes_contrataveis = LoteLicitacao.objects.filter()
    LoteLicitacao.objects.filter(
        licitacao_referencia=contrato.licitacao_referencia).exclude(lotecontrato__in=lotes_contratados)

    return lotes_contrataveis


