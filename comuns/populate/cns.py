relatorio_gsus = "C:\\Users\\vanderlei\\OneDrive - 0vmsj\\Documentos\\DEV\\hrso_escala\\comuns\\populate\\CNS\\RelatorioUsuariosGSUS_2024-02-06_09h38min31s.pdf"

def remover_quebra_linha_r(info_str):
    info_str = info_str.replace('\r', ' ')
    info_str = info_str.replace('- ', '-')
    info_str = info_str.replace(' -', '-')
    return info_str


def processar_celula_linha(celula):
    import math
    if isinstance(celula, str):
        celula = remover_quebra_linha_r(celula)
    if isinstance(celula, float):
        if math.isnan(celula) or math.isinf(celula):
            celula = None
    return celula


def parse_conselhos(string_conselhos):
    import re
    conselhos = []

    regex = r'([A-Za-z]+-[A-Za-z]+) (\d+) \((.+?)\)'

    matches = re.findall(regex, string_conselhos)

    for match in matches:
        estado_conselho, numero_conselho, ocupacao = match

        conselho, estado = estado_conselho.split('-')

        conselhos.append((conselho, estado, numero_conselho, ocupacao))
    return conselhos

def extrair_dados_relatorio_cns_tabula(arquivo):
    from pessoas.models import PessoaFisica, Profissional, Ocupacao, Funcao
    from comuns.models import ConselhoProfissional
    from escala_geral.models import DadosConselhoProfissional
    from tabula import read_pdf
    from validate_docbr import CPF
    from comuns.populate.pessoas import FUNCOES_CBO
    from unidecode import unidecode

    dataframes = read_pdf(arquivo, pages='all')
    for dtf in dataframes:
        for dados_linha in dtf.itertuples(index=False):
            dados_linha = [processar_celula_linha(d) for d in dados_linha]
            #print(dados_linha)
            cpf = dados_linha[0]
            #cpf = CPF().mask(cpf.zfill(11))
            nome = dados_linha[1]
            nascimento = dados_linha[2]
            celular = dados_linha[3]
            if CPF().validate(cpf) is True:
                print(nome)
                colaborador, created = PessoaFisica.objects.get_or_create(cpf=cpf, defaults={'nome': nome})

                conselhos = parse_conselhos(dados_linha[4])
                if len(conselhos) == 1:
                    conselho = conselhos[0]
                    # print(cpf, nome, nascimento, celular, conselhos,type(conselhos))
                elif len(conselhos) == 2:
                    if conselhos[0] == conselhos[1]:
                        conselho = conselhos[0]
                    else:
                        continue
                else:
                    continue

                nome_conselho = conselho[0]
                if nome_conselho == "OUTROS":
                    continue

                estado = conselho[1]
                numero = conselho[2]
                funcao = "MEDICO" if 'MEDICO' in unidecode(conselho[3]).upper() else unidecode(conselho[3]).upper()
                print(funcao)
                print(nome_conselho)

                conselho_profissional = ConselhoProfissional.objects.get(sigla=nome_conselho)

                print(conselho_profissional)

                funcao, funcao_created = Funcao.objects.get_or_create(
                    nome=funcao,
                    funcao_medica=True if funcao == "MEDICO" else False)

                try:
                    codigo_ocupacao = FUNCOES_CBO[unidecode(funcao.nome).upper()]
                    ocupacao = Ocupacao.objects.get(codigo_cbo=codigo_ocupacao)
                except Exception as e:
                    print(e)
                    print(funcao.nome)
                    continue

                profissional, created = Profissional.objects.get_or_create(
                    pessoa_fisica=colaborador, funcao=funcao, cbo=ocupacao)

                dados_conselho, dc_created = DadosConselhoProfissional.objects.get_or_create(
                    profissional=profissional, conselho=conselho_profissional, estado_conselho=estado, numero=numero)





