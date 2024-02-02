import datetime

from pessoas.models import PessoaFisica, Unidade, Fornecedor

def criar_organizacao():
    pf, created = PessoaFisica.objects.get_or_create(cpf="000.000.009-00",
                                                     data_cadastro=datetime.date.today(),
                                                     nome="Usuario de Teste")

    unidade, created_u = Unidade.objects.get_or_create(nome_unidade="HRS", sigla_unidade="HRS", diretor_unidade=pf, nome_cargo_diretor="Diretor Geral")

    funsaude, created_f = Fornecedor.objects.get_or_create(
        cnpj_fornecedor="8597121000174",
        nome_fantasia="FUNDO ESTADUAL DE SAUDE DO PARANA - FUNSAUDE",
        razao_social_fornecedor="FUNDO ESTADUAL DE SAUDE DO PARANA - FUNSAUDE",
        nome_banco="FUNSAUDE",
        codigo_banco="FUNSAUDE",
        agencia_banco="FUNSAUDE",
        conta_fornecedor="FUNSAUDE",
        endereco_fornecedor="R PIQUIRI, 170",
        cep_fornecedor="80230140",
        bairro_fornecedor="REBOUCAS",
        cidade_fornecedor="CURITIBA",
        estado_fornecedor="PR",
        telefone_fornecedor="41 33304339",
        contato_fornecedor="SESA",
        email_fornecedor="CONTABIL@SESA.PR.GOV.BR",
    )

    funeas, created_fu = Fornecedor.objects.get_or_create(
        cnpj_fornecedor="24039073000155",
        nome_fantasia="FUNDACAO ESTATAL DE SAUDE DO ESTADO DO PARANA - FUNEAS",
        razao_social_fornecedor="FUNDACAO ESTATAL DE SAUDE DO ESTADO DO PARANA - FUNEAS",
        nome_banco="FUNEAS",
        codigo_banco="FUNEAS",
        agencia_banco="FUNEAS",
        conta_fornecedor="FUNEAS",
        endereco_fornecedor="RUA DO ROSARIO, 144",
        cep_fornecedor="80020110",
        bairro_fornecedor="CENTRO",
        cidade_fornecedor="CURITIBA",
        estado_fornecedor="PR",
        telefone_fornecedor="41 33507401",
        contato_fornecedor="FUNEAS",
        email_fornecedor="atendimento@funeas.pr.gov.br",
    )



def criar_dados_iniciais():
    criar_organizacao()

    from comuns.populate.pessoas import processar_arquivos_meta_4
    from pessoas.ferramentas.cbo import ler_arquivo_ocupacoes

    ler_arquivo_ocupacoes(
        "C:\\Users\\vanderlei\\OneDrive - 0vmsj\\Documentos\\DEV\\hrso_escala\\comuns\\populate\\CBO\\CBO2002 - Ocupacao.csv")

    processar_arquivos_meta_4()

