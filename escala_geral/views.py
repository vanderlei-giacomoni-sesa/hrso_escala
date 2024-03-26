from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, resolve_url
from datetime import time, timedelta, datetime

from escala_geral.models import HorarioPlantao


def inicio(request):
    return render(request, 'escala_geral/base.html')


class BaseViewConfiguracoesEscala(LoginRequiredMixin, View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = None
        self.configuracoes = None

    def setup(self, request, *args, **kwargs):
        print('1', request)

        self.nav_path = [{"nome": "Escala",
                          'href': resolve_url("Escala:inicio"),
                          'ativo': False, 'options': None},
                         ]
        self.configuracoes = [
            {'nome': "Horários Padronizados", 'url': resolve_url("Escala:Configurar Horários"), 'slug': "horarios"}
        ]
        self.context = {'configuracoes': self.configuracoes}

        return super().setup(request, *args, **kwargs)


class Configuracoes(BaseViewConfiguracoesEscala):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        print("2", request)
        self.nav_path.append({"nome": "Configurações",
                              'href': resolve_url("Escala:Configurações"),
                              'ativo': True, 'options': None})

        self.context['nav_path'] = self.nav_path


    def get(self, request, *args, **kwargs):

        return render(request, 'escala_geral/configuracoes/inicio.html', self.context)


class ConfigurarHorarios(BaseViewConfiguracoesEscala):

    def dispatch(self, request, *args, **kwargs):
        print('1', request)
        return super().dispatch(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.nav_path.extend([
            {"nome": "Configurações", 'href': resolve_url("Escala:Configurações"), 'ativo': False, 'options': None},
            {"nome": "Horarios", 'href': "#", 'ativo': True, 'options': None}])

        self.context['nav_path'] = self.nav_path

    def processar_post(self, request, *args, **kwargs):
        post = request.POST.copy().dict()
        tipos_acao = {"AdicionarHorario": self.adicionar_horario}
        return tipos_acao[post['tipo-acao']](request, post)

    def validar_horario(self, request, post):
        horario_inicio = time.fromisoformat(post['horario_inicio'])
        duracao_plantao = self._calcular_duracao(post['duracao_plantao'])
        duracao_folga = self._calcular_duracao(post['duracao_folga'])
        horario_almoco, duracao_almoco = self._obter_horario_e_duracao_almoco(request)

        if not self._sao_duracoes_validas(duracao_plantao, duracao_folga, duracao_almoco):
            return None

        if horario_almoco:
            if not self._horario_almoco_eh_valido(horario_inicio, duracao_plantao, horario_almoco):
                return None

        folga_sabado = 'folga_sabado' in post
        folga_domingo = 'folga_domingo' in post

        return {'horario_inicio': horario_inicio,
                'duracao_plantao': duracao_plantao,
                'duracao_folga': duracao_folga,
                'horario_almoco': horario_almoco,
                'duracao_almoco': duracao_almoco,
                'folga_sabado': folga_sabado,
                'folga_domingo': folga_domingo}

    @staticmethod
    def _calcular_duracao(duracao_str):
        horas, minutos = map(int, duracao_str.split(":"))
        return timedelta(hours=horas, minutes=minutos)


    def _obter_horario_e_duracao_almoco(self, request):
        horario_almoco = request.POST.get('horario_almoco')
        duracao_almoco = request.POST.get('duracao_almoco')

        if horario_almoco and duracao_almoco:
            return time.fromisoformat(horario_almoco), self._calcular_duracao(duracao_almoco)
        else:
            return None, None

    @staticmethod
    def _sao_duracoes_validas(duracao_plantao, duracao_folga, duracao_almoco):
        soma_duracao = duracao_plantao + duracao_folga
        if duracao_almoco:
            soma_duracao += duracao_almoco
        print("soma_duracao.total_seconds() % timedelta(days=1).total_seconds()", soma_duracao.total_seconds() % timedelta(days=1).total_seconds())
        return soma_duracao.total_seconds() % timedelta(days=1).total_seconds() == 0

    @staticmethod
    def _horario_almoco_eh_valido(horario_inicio, duracao_plantao, horario_almoco):
        print(horario_inicio, duracao_plantao, horario_almoco)
        inicio_validar = datetime.combine(datetime.today(), horario_inicio)
        limite_almoco = inicio_validar + duracao_plantao
        horaio_almoco_1 = datetime.combine(datetime.today(), horario_almoco)
        horaio_almoco_2 = datetime.combine(limite_almoco.date(), horario_almoco)

        return inicio_validar < horaio_almoco_1 < limite_almoco or inicio_validar < horaio_almoco_2 < limite_almoco

    def adicionar_horario(self, request, post):
        if (dados := self.validar_horario(request, post)):
            hp = HorarioPlantao(**dados)
            print(hp.horario_inicio, hp.duracao_plantao, hp.duracao_folga, hp.horario_almoco, hp.duracao_almoco, hp.folga_sabado, hp.folga_domingo)
            print(type(hp.horario_inicio), type(hp.duracao_plantao), type(hp.duracao_folga), type(hp.horario_almoco), type(hp.duracao_almoco),
                  hp.folga_sabado, hp.folga_domingo)
            hp.save()
        else:
            messages.error(request, 'Horario invalido')
        return redirect("Escala:Configurar Horários")

    @staticmethod
    def dados_adicionais_horario(horario):
        horario = dict(horario)
        inicio = datetime.combine(datetime.today(),  horario['horario_inicio'])
        fim = inicio + horario['duracao_plantao'] + horario['duracao_almoco'] if horario['duracao_almoco'] else inicio + horario['duracao_plantao'] + horario['duracao_almoco']



    def get(self, request, *args, **kwargs):

        return render(request, 'escala_geral/configuracoes/horarios_padronizados.html', self.context)

    def post(self, request, *args, **kwargs):

        return self.processar_post(request, *args, **kwargs)




