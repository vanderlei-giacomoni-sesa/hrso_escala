import os
from datetime import date
import xlsxwriter
from validate_docbr import CPF

from hrso_escala.settings import BASE_DIR
from pessoas.ferramentas.meta4 import ler_arquivos

from comuns.models import Funcao, PeriodoReferencia
from escala_geral.models import DadosConselhoProfissional
from pessoas.models import Profissional, PessoaFisica, VinculoFuncional, DadosCadastraisMeta4, \
    LancamentoContrachequeMeta4
from comuns.populate.pessoas import FUNCOES_CBO
from comuns.models import Ocupacao

from django.db.models import Max, Min, Sum


def funcoes_meta_4():
    from unidecode import unidecode
    pasta_arquivos = os.path.join(BASE_DIR, "comuns\\populate\\meta4")
    arquivos = [os.path.join(pasta_arquivos, a) for a in os.listdir(pasta_arquivos)]
    dados = ler_arquivos(arquivos)

    lista_id, lista_dados, lista_lancamentos, arquivos_processados, arquivos_nao_processados = dados

    ili = 0

    lista_funcoes = []

    for id_servidor in lista_id:
        dados_servidor = lista_dados[ili]

        n_id = id_servidor[0]
        id_ato_formal = id_servidor[1]

        nome = dados_servidor[0]
        rg = dados_servidor[1]
        t_emp = dados_servidor[3]
        nascimento = dados_servidor[4]
        pis = dados_servidor[5]
        cpf = dados_servidor[6]
        admissao = dados_servidor[7]
        carga_horaria = dados_servidor[9]
        cargo = dados_servidor[10]
        nome_funcao = unidecode(dados_servidor[11]).upper()
        # funcao, funcao_created = Funcao.objects.get_or_create(
        #     nome=nome_funcao, funcao_medica=True if nome_funcao == "MEDICO" else False)
        if nome_funcao in lista_funcoes:
            pass
        else:
            codigo_ocupacao = FUNCOES_CBO[nome_funcao]
            ocupacao = Ocupacao.objects.get(codigo_cbo=codigo_ocupacao)
            lista_funcoes.append(nome_funcao)
            print(nome_funcao, codigo_ocupacao, ocupacao)

        ili += 1
    #print(lista_funcoes)


def relatorio_nascimento_colaboradores():
    funcionarios = VinculoFuncional.objects.filter(tipo_vinculo=VinculoFuncional.Vinculo.SESA).values(
        'profissional__pessoa_fisica__nome',
        'profissional__pessoa_fisica__cpf',
        'dadoscadastraismeta4__nascimento',
        'dadoscadastraismeta4__admissao',
        'dadoscadastraismeta4__cargo',
        'dadoscadastraismeta4__funcao',
        'dadoscadastraismeta4__classe',
        'dadoscadastraismeta4__referencia_classe',
        'dadoscadastraismeta4__quadro',

    )

    wb = xlsxwriter.Workbook("relatorio.xlsx")
    ws = wb.add_worksheet('funcionarios')

    linha = 0

    ws.write(linha, 0, "Nome")
    ws.write(linha, 1, "cpf")
    ws.write(linha, 2, "nascimento")

    ws.write(linha, 3, "admissao")
    ws.write(linha, 4, "cargo")
    ws.write(linha, 5, "funcao")

    ws.write(linha, 6, "classe")
    ws.write(linha, 7, "referencia_classe")
    ws.write(linha, 8, "Quadro")

    linha = 1
    for f in funcionarios:
        ws.write(linha, 0, f['profissional__pessoa_fisica__nome'])
        ws.write(linha, 1, f['profissional__pessoa_fisica__cpf'])
        ws.write(linha, 2, f['dadoscadastraismeta4__nascimento'])

        ws.write(linha, 3, f['dadoscadastraismeta4__admissao'])
        ws.write(linha, 4, f['dadoscadastraismeta4__cargo'])
        ws.write(linha, 5, f['dadoscadastraismeta4__funcao'])

        ws.write(linha, 6, f['dadoscadastraismeta4__classe'])
        ws.write(linha, 7, f['dadoscadastraismeta4__referencia_classe'])
        ws.write(linha, 8, f['dadoscadastraismeta4__quadro'])

        linha += 1

    wb.close()



def lista_remuneracao_colaboradores():
    codigos_buscar = [1005,
                      1056,
                      1059,
                      1079,
                      1229,
                      1469,
                      1476,
                      1533,
                      1553,
                      1788,
                      1923,
                      2187,
                      2214,
                      2308,
                      2394,
                      2399,
                      2487,
                      2533,
                      3533,
                      3540,
                      5713,
                      5736,
                      5739,
                      5773,
                      5796,
                      6023,
                      6026,
                      6033,
                      6040,
                      6053,
                      6253,
                      ]
    periodo = PeriodoReferencia.objects.get(ano_referencia=2024, mes_referencia=2)
    descricoes = LancamentoContrachequeMeta4.objects.filter(periodo_referencia=periodo).values('descricao_lancamento', 'id_lancamento').distinct()

    x = LancamentoContrachequeMeta4.objects.filter(periodo_referencia=periodo).values(
        'valor_desconto', 'valor_vantagem').aggregate(menor_lancamento=Min('valor_vantagem'),
                                                      menor_desconto=Min('valor_vantagem'))

    colaboradores_periodo = VinculoFuncional.objects.filter(
        dadoscadastraismeta4__periodo_referencia=periodo
    ).values('id', "id_ato_formal", 'profissional__pessoa_fisica__nome', 'dadoscadastraismeta4__funcao__nome', 'dadoscadastraismeta4__cargo'
             ).order_by('profissional__pessoa_fisica__nome')

    for c in colaboradores_periodo:
        lc = LancamentoContrachequeMeta4.objects.filter(
            vinculo_funcional__id=c['id'], periodo_referencia=periodo, id_lancamento__in=codigos_buscar
        ).values('valor_vantagem', 'valor_desconto').aggregate(
            vantagens_totais=Sum('valor_vantagem'), descontos_totais=Sum('valor_desconto')
        )
        total = lc['vantagens_totais'] - lc['descontos_totais']
        st = "{:.2f}".format(total)
        print(f"{c['profissional__pessoa_fisica__nome']};{c['dadoscadastraismeta4__funcao__nome']};{c['dadoscadastraismeta4__cargo']};{st}")









