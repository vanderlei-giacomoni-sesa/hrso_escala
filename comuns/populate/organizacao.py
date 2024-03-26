import datetime
from comuns.populate.pessoas import criar_conselhos, definir_funcoes_conselhos_ocupacoes
from pessoas.models import PessoaFisica, Unidade, Fornecedor

def criar_organizacao():
    pf, created = PessoaFisica.objects.get_or_create(cpf="000.000.009-00",
                                                     data_cadastro=datetime.date.today(),
                                                     nome="Usuario de Teste")

    unidade, created_u = Unidade.objects.get_or_create(nome_unidade="HRS", sigla_unidade="HRS", diretor_unidade=pf, nome_cargo_diretor="Diretor Geral")

    funsaude, created_f = Fornecedor.objects.get_or_create(
        cnpj_fornecedor="08.597.121/0001-74",
        nome_fantasia="FUNDO ESTADUAL DE SAUDE DO PARANA - FUNSAUDE",
        razao_social_fornecedor="FUNDO ESTADUAL DE SAUDE DO PARANA - FUNSAUDE",
        nome_banco="FUNSAUDE",
        codigo_banco="FUNSAUDE",
        agencia_banco="FUNSAUDE",
        conta_fornecedor="FUNSAUDE",
        endereco_fornecedor="R PIQUIRI, 170",
        cep_fornecedor="80230-140",
        bairro_fornecedor="REBOUCAS",
        cidade_fornecedor="CURITIBA",
        estado_fornecedor="PR",
        telefone_fornecedor="41 33304339",
        contato_fornecedor="SESA",
        email_fornecedor="CONTABIL@SESA.PR.GOV.BR",
    )

    funeas, created_fu = Fornecedor.objects.get_or_create(
        cnpj_fornecedor="24.039.073/0001-55",
        nome_fantasia="FUNDACAO ESTATAL DE SAUDE DO ESTADO DO PARANA - FUNEAS",
        razao_social_fornecedor="FUNDACAO ESTATAL DE SAUDE DO ESTADO DO PARANA - FUNEAS",
        nome_banco="FUNEAS",
        codigo_banco="FUNEAS",
        agencia_banco="FUNEAS",
        conta_fornecedor="FUNEAS",
        endereco_fornecedor="RUA DO ROSARIO, 144",
        cep_fornecedor="80020-110",
        bairro_fornecedor="CENTRO",
        cidade_fornecedor="CURITIBA",
        estado_fornecedor="PR",
        telefone_fornecedor="41 33507401",
        contato_fornecedor="FUNEAS",
        email_fornecedor="atendimento@funeas.pr.gov.br",
    )


def criar_modalidaes_licitacao():
    from contratos.models import ModalidadeLicitacao
    MODALIDADES_CHOICES = (("Credenciamento", True),
                           ("Pregão", True),
                           ("concorrência", True),
                           ("diálogo competitivo", True),
                           )
    for modalidade, faturavel in MODALIDADES_CHOICES:
        modalidade, created = ModalidadeLicitacao.objects.get_or_create(nome_modalidade=modalidade, modalidade_faturavel=faturavel)



def criar_dados_iniciais():
    criar_organizacao()
    criar_conselhos()
    criar_modalidaes_licitacao()

    from comuns.populate.pessoas import processar_arquivos_meta_4
    from pessoas.ferramentas.cbo import ler_arquivo_ocupacoes
    from comuns.populate.cns import relatorio_gsus, extrair_dados_relatorio_cns_tabula

    ler_arquivo_ocupacoes(
        "C:\\Users\\vanderlei\\OneDrive - 0vmsj\\Documentos\\DEV\\hrso_escala\\comuns\\populate\\CBO\\CBO2002 - Ocupacao.csv")

    processar_arquivos_meta_4()
    extrair_dados_relatorio_cns_tabula(relatorio_gsus)
    definir_funcoes_conselhos_ocupacoes()
    ler_fornecedores()


def ler_fornecedores():
    import csv
    from comuns.models import Fornecedor
    arquivo_fornecedores = "C:\\Users\\vanderlei\\OneDrive - 0vmsj\\Documentos\\DEV\\hrso_escala\\comuns\\populate\\fornecedores\\fornecedores_sgc.csv"

    lista_tuplas = []

    with open(arquivo_fornecedores, 'r', encoding="UTF-8", newline='') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)

        for linha in leitor_csv:
            f, c = Fornecedor.objects.get_or_create(cnpj_fornecedor=linha[1],
                                                    nome_fantasia=linha[2],
                                                    razao_social_fornecedor=linha[3],
                                                    nome_banco=linha[4],
                                                    codigo_banco=linha[5],
                                                    agencia_banco=linha[6],
                                                    conta_fornecedor=linha[7],
                                                    endereco_fornecedor=linha[8],
                                                    cep_fornecedor=linha[9],
                                                    bairro_fornecedor=linha[10],
                                                    cidade_fornecedor=linha[11],
                                                    estado_fornecedor=linha[12],
                                                    telefone_fornecedor=linha[13],
                                                    contato_fornecedor=linha[14],
                                                    email_fornecedor=linha[15],
                                                    )
            print(f)
            lista_tuplas.append(tuple(linha))
    return lista_tuplas

