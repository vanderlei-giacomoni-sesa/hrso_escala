import re
from comuns.models import PeriodoReferencia

def ler_arquivos(arquivos):
    MESES = {'JANEIRO': 1,
             'FEVEREIRO': 2,
             'MARÇO': 3,
             'ABRIL': 4,
             'MAIO': 5,
             'JUNHO': 6,
             'JULHO': 7,
             'AGOSTO': 8,
             'SETEMBRO': 9,
             'OUTUBRO': 10,
             'NOVEMBRO': 11,
             'DEZEMBRO': 12,
             }

    hrs = 'HOSPITAL REGIONAL DE FRANCISCO BELTRAO'

    allowed_types = ['application/vnd.ms-excel', 'text/plain']
    max_file_size = 26214400

    lista_id_id_ato_formal = []
    lista_dados = []
    lista_lancamentos = []
    padrao_id = re.compile(r'\d+')

    arquivos_nao_processados = []

    arquivos_processados = []

    padrao_referencia = re.compile(r'[A-Z]+/\d+$')

    for a in arquivos:
        mes_referencia_arquivo = None
        ano_referencia_arquivo = None
        periodo_referencia = None

        arquivo = a
        with open(arquivo) as f:
            linhas_relatorio = f.readlines()
            linhas_arquivo_validas = 0
            for linha_relatorio in linhas_relatorio:
                linha_relatorio = linha_relatorio.replace('\n', '').split(',')

                if len(linha_relatorio) == 22 and mes_referencia_arquivo is not None and periodo_referencia is not None:
                    if linha_relatorio[16] == hrs:
                        nome = linha_relatorio[0]
                        rg = linha_relatorio[1]
                        n_id = int(linha_relatorio[2])
                        t_emp = linha_relatorio[3]
                        nascimento = linha_relatorio[4]
                        pis = linha_relatorio[5]
                        cpf = linha_relatorio[6]
                        admissao = linha_relatorio[7]
                        id_ato_formal = linha_relatorio[8]
                        carga_horaria = linha_relatorio[9]
                        cargo = linha_relatorio[10]
                        funcao = linha_relatorio[11]
                        classe = linha_relatorio[12]
                        referencia_classe = linha_relatorio[13]
                        cidade = linha_relatorio[14]
                        estado = linha_relatorio[15]
                        quadro = linha_relatorio[17]
                        try:
                            descricao = linha_relatorio[18]

                            id_descricao = re.search(padrao_id, descricao).group()
                            descricao = descricao.replace(id_descricao, '').strip()
                            vantagem = linha_relatorio[19]
                            desconto = linha_relatorio[20]

                            try:
                                indice_id = lista_id_id_ato_formal.index((n_id, id_ato_formal))
                                lista_lancamentos[indice_id].append(
                                    (id_descricao, descricao, vantagem, desconto))
                                linhas_arquivo_validas += 1
                            except:
                                lista_id_id_ato_formal.append((n_id, id_ato_formal))
                                lista_lancamentos.append([(id_descricao, descricao, vantagem, desconto)])
                                lista_dados.append(
                                    (nome, rg, n_id, t_emp, nascimento, pis, cpf, admissao, id_ato_formal,
                                     carga_horaria, cargo, funcao, classe, referencia_classe, cidade, estado,
                                     quadro, periodo_referencia))
                                linhas_arquivo_validas += 1
                        except Exception as e:
                            print(linha_relatorio)
                            print(descricao)
                            print(e)

                elif len(linha_relatorio) == 2:
                    buscar_referencia = re.search(padrao_referencia, linha_relatorio[0])
                    if buscar_referencia is not None:
                        nome_mes_referencia_arquivo, ano_referencia_arquivo = buscar_referencia.group().split(
                            '/')
                        mes_referencia_arquivo = MESES[nome_mes_referencia_arquivo]
                        ano_referencia_arquivo = int(ano_referencia_arquivo)

                        if PeriodoReferencia.objects.filter(mes_referencia=mes_referencia_arquivo,
                                                            ano_referencia=ano_referencia_arquivo).exists():
                            periodo_referencia = PeriodoReferencia.objects.get(
                                mes_referencia=mes_referencia_arquivo,
                                ano_referencia=ano_referencia_arquivo)
                        else:
                            periodo_referencia = PeriodoReferencia(
                                mes_referencia=mes_referencia_arquivo,
                                ano_referencia=ano_referencia_arquivo
                            )

                            periodo_referencia.save()

    return [lista_id_id_ato_formal, lista_dados, lista_lancamentos, arquivos_processados, arquivos_nao_processados]

