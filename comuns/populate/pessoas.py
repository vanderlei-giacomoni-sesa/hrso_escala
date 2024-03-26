import os
from datetime import date

from validate_docbr import CPF

from hrso_escala.settings import BASE_DIR
from pessoas.ferramentas.meta4 import ler_arquivos
from pessoas.models import PessoaFisica, VinculoFuncional, DadosCadastraisMeta4, LancamentoContrachequeMeta4, Unidade, \
    Profissional, VinculoColaboradorUnidade
from comuns.models import Funcao, Fornecedor
from escala_geral.models import DadosConselhoProfissional, Ocupacao


hrs = 'HOSPITAL REGIONAL DE FRANCISCO BELTRAO'


def string_to_float(string):
    if string == '':
        return 0
    else:
        return float(string)



FUNCOES = ['AUXILIAR DE MANUTENCAO', 'AUXILIAR OPERACIONAL', 'TECNICO DE ENFERMAGEM', 'FARMACEUTICO', 'TECNICO ADMINISTRATIVO', 'TECNICO DE SEGURANCA DO TRABALHO', 'ENFERMEIRO', 'AUXILIAR ADMINISTRATIVO', 'PSICOLOGO', 'TECNICO DE LABORATORIO', 'FISIOTERAPEUTA', 'NUTRICIONISTA', 'MOTORISTA', 'MEDICO', 'TECNICO DE RADIOLOGIA', 'ASSISTENTE SOCIAL', 'ASSISTENTE DE FARMACIA', 'TERAPEUTA OCUPACIONAL', 'FONOAUDIOLOGO', 'TELEFONISTA', 'ADMINISTRADOR']

FUNCOES_CBO = {
    "ADMINISTRADOR": "252105",
    "ASSISTENTE DE FARMACIA": "521130",
    "ASSISTENTE SOCIAL": "251605",
    "AUXILIAR ADMINISTRATIVO": "411010",
    "AUXILIAR DE MANUTENCAO": "514310",
    "AUXILIAR OPERACIONAL": "514310",
    "ENFERMEIRO": "223505",
    "FARMACEUTICO": "223405",
    "FISIOTERAPEUTA": "223605",
    "FONOAUDIOLOGO": "223810",
    "MEDICO": "225125",
    "MOTORISTA": "782310",
    "NUTRICIONISTA": "223710",
    "PSICOLOGO": "251520",
    "TECNICO ADMINISTRATIVO": "351305",
    "TECNICO DE ENFERMAGEM": "322230",
    "TECNICO DE LABORATORIO": "515215",
    "TECNICO DE RADIOLOGIA": "324120",
    "TECNICO DE SEGURANCA DO TRABALHO": "351605",
    "TELEFONISTA": "422205",
    "TERAPEUTA OCUPACIONAL": "351610"
}

FUNCAO_CBO_CONSELHO = {
    "ADMINISTRADOR": {"CBO":  "252105", "CONSELHO": "CRA"},
    "ASSISTENTE DE FARMACIA": {"CBO":  "521130", "CONSELHO": None},
    "ASSISTENTE SOCIAL": {"CBO":  "251605", "CONSELHO": "CRESS"},
    "AUXILIAR ADMINISTRATIVO": {"CBO":  "411010", "CONSELHO": None},
    "AUXILIAR DE MANUTENCAO": {"CBO":  "514310", "CONSELHO": None},
    "AUXILIAR OPERACIONAL": {"CBO":  "514310", "CONSELHO": None},
    "ENFERMEIRO": {"CBO":  "223505", "CONSELHO": "COREN"},
    "FARMACEUTICO": {"CBO":  "223405", "CONSELHO": "CRF"},
    "FISIOTERAPEUTA": {"CBO":  "223605", "CONSELHO": "CREFITO"},
    "FONOAUDIOLOGO": {"CBO":  "223810", "CONSELHO": "CREFONO"},
    "MEDICO": {"CBO":  "225125", "CONSELHO": "CRM"},
    "MOTORISTA": {"CBO":  "782310", "CONSELHO": None},
    "NUTRICIONISTA": {"CBO":  "223710", "CONSELHO": "CRN"},
    "PSICOLOGO": {"CBO":  "251520", "CONSELHO": "CRP"},
    "TECNICO ADMINISTRATIVO": {"CBO":  "351305", "CONSELHO": None},
    "TECNICO DE ENFERMAGEM": {"CBO":  "322230", "CONSELHO": "COREN"},
    "TECNICO DE LABORATORIO": {"CBO":  "515215", "CONSELHO": None},
    "TECNICO DE RADIOLOGIA": {"CBO":  "324120", "CONSELHO": "CRTR"},
    "TECNICO DE SEGURANCA DO TRABALHO": {"CBO":  "351605", "CONSELHO": None},
    "TELEFONISTA": {"CBO":  "422205", "CONSELHO": None},
    "TERAPEUTA OCUPACIONAL": {"CBO":  "351610", "CONSELHO": "CREFITO"},
}


def processar_arquivos_meta_4():
    from unidecode import unidecode
    unidade = Unidade.objects.get(sigla_unidade="HRS")
    pasta_arquivos = os.path.join(BASE_DIR, "comuns\\populate\\meta4")
    sesa = Fornecedor.objects.get(contato_fornecedor="SESA")
    arquivos = [os.path.join(pasta_arquivos, a) for a in os.listdir(pasta_arquivos)]
    dados = ler_arquivos(arquivos)

    lista_id, lista_dados, lista_lancamentos, arquivos_processados, arquivos_nao_processados = dados

    ili = 0

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
        funcao, funcao_created = Funcao.objects.get_or_create(
            nome=unidecode(dados_servidor[11]).upper(), funcao_medica=True if dados_servidor[11] == "MEDICO" else False)
        classe = dados_servidor[12]
        referencia_classe = dados_servidor[13]
        cidade = dados_servidor[14]
        estado = dados_servidor[15]
        quadro = dados_servidor[16]
        periodo_referencia = dados_servidor[17]

        lancamentos_servidor = lista_lancamentos[ili]

        cpf = CPF().mask(cpf.zfill(11))
        if CPF().validate(cpf) is True:
            # Se Pessoa fisica ja esta cadastrada
            if PessoaFisica.objects.filter(cpf=cpf).exists():
                pessoa_fisica = PessoaFisica.objects.get(cpf=cpf)
            else:
                pessoa_fisica = PessoaFisica(nome=nome, cpf=cpf, data_cadastro=date.today())
                pessoa_fisica.save()

            codigo_ocupacao = FUNCOES_CBO[unidecode(funcao.nome).upper()]
            ocupacao = Ocupacao.objects.get(codigo_cbo=codigo_ocupacao)
            profissional, created = Profissional.objects.get_or_create(
                pessoa_fisica=pessoa_fisica, funcao=funcao, cbo=ocupacao)

            if VinculoFuncional.objects.filter(
                    profissional=profissional, id_ato_formal=id_ato_formal, id_meta4=n_id,
                    tipo_vinculo=VinculoFuncional.Vinculo.SESA
            ).exists():
                vinculo_meta4 = VinculoFuncional.objects.get(profissional=profissional,
                                                             id_ato_formal=id_ato_formal,
                                                             id_meta4=n_id,
                                                             tipo_vinculo=VinculoFuncional.Vinculo.SESA)
            else:
                print(profissional,id_ato_formal, n_id, VinculoFuncional.Vinculo.SESA, sesa)
                vinculo_meta4, vinculo_created = VinculoFuncional.objects.get_or_create(
                    profissional=profissional, id_ato_formal=id_ato_formal, id_meta4=n_id,
                    tipo_vinculo=VinculoFuncional.Vinculo.SESA, cnpj_vinculo=sesa)

            dia_nascimento, mes_nascimento, ano_nascimento = nascimento.split('/')
            data_dascimento = date(day=int(dia_nascimento), month=int(mes_nascimento), year=int(ano_nascimento))

            dia_admissao, mes_admissao, ano_admissao = admissao.split('/')
            data_admissao = date(day=int(dia_admissao), month=int(mes_admissao), year=int(ano_admissao))

            vcu, created = VinculoColaboradorUnidade.objects.get_or_create(unidade=unidade,
                                                                           vinculo_funcional=vinculo_meta4,
                                                                           inicio_vinculo=data_admissao)

            print(pessoa_fisica, vinculo_meta4, data_dascimento, data_admissao)
            print(int(carga_horaria), pis, quadro, len(quadro))

            print(lancamentos_servidor)

            if DadosCadastraisMeta4.objects.filter(vinculo_funcional=vinculo_meta4,
                                                   periodo_referencia=periodo_referencia).exists():
                dados_cadastrais = DadosCadastraisMeta4.objects.get(vinculo_funcional=vinculo_meta4,
                                                                    periodo_referencia=periodo_referencia)
            else:
                dados_cadastrais = DadosCadastraisMeta4(vinculo_funcional=vinculo_meta4,
                                                        periodo_referencia=periodo_referencia,
                                                        rg=rg,
                                                        t_emp=t_emp,
                                                        nascimento=data_dascimento,
                                                        pis=pis,
                                                        admissao=data_admissao,
                                                        carga_horaria=int(carga_horaria),
                                                        cargo=cargo,
                                                        funcao=funcao,
                                                        classe=classe,
                                                        referencia_classe=referencia_classe,
                                                        cidade=cidade,
                                                        estado=estado,
                                                        local=hrs,
                                                        quadro=quadro,
                                                        )

                dados_cadastrais.save()

            if LancamentoContrachequeMeta4.objects.filter(vinculo_funcional=vinculo_meta4,
                                                          periodo_referencia=periodo_referencia).exists():
                for lancamento in LancamentoContrachequeMeta4.objects.filter(vinculo_funcional=vinculo_meta4,
                                                                             periodo_referencia=periodo_referencia):
                    lancamento.delete()

            for lancamento in lancamentos_servidor:
                id_lancamento = int(lancamento[0])
                descricao_lancamento = lancamento[1]
                valor_vantagem = string_to_float(lancamento[2])
                valor_desconto = string_to_float(lancamento[3])

                lancamento_salvar = LancamentoContrachequeMeta4(
                    periodo_referencia=periodo_referencia,
                    vinculo_funcional=vinculo_meta4,
                    id_lancamento=id_lancamento,
                    descricao_lancamento=descricao_lancamento,
                    valor_vantagem=valor_vantagem,
                    valor_desconto=valor_desconto,
                )
                lancamento_salvar.save()

        ili += 1


def criar_conselhos():
    CONSELHOS_CRIAR = [
        ('COREN', 'Conselho Regional de Enfermagem'),
        ('CRF', 'Conselho Regional de Farmácia'),
        ('CRM', 'Conselho Regional de Medicina'),
        ('CREFITO', 'Conselho Regional de Fisioterapia e Terapia Ocupacional'),
        ("CREFONO", "Conselho Regional de Fonoaudiologia"),
        ("CRFa", "Conselho Regional de Fonoaudiologia"),
        ('CRP', 'Conselho Regional de Psicologia'),
        ('CRO', 'Conselho Regional de Odontologia'),
        ('CRN', 'Conselho Regional de Nutrição'),
        ('CRTR', 'Conselho Regional de Técnicos em Radiologia'),
        ('CRESS', 'Conselho Regional de Serviço Social'),
        ('CRBM', 'Conselho Regional de Biomedicina'),
        ('CRA', 'Conselho Regional de Administração')
    ]

    from comuns.models import ConselhoProfissional
    for c in CONSELHOS_CRIAR:
        conselho, crated = ConselhoProfissional.objects.get_or_create(sigla=c[0], defaults={"nome": c[1]})


def definir_funcoes_conselhos_ocupacoes():
    from comuns.models import ConselhoProfissional
    for f in FUNCAO_CBO_CONSELHO.keys():
        cbo = FUNCAO_CBO_CONSELHO[f]['CBO']
        conselho = FUNCAO_CBO_CONSELHO[f]['CONSELHO']
        funcao, created = Funcao.objects.get_or_create(nome=f)
        ocupacao = Ocupacao.objects.get(codigo_cbo=cbo)
        try:
            conselho = ConselhoProfissional.objects.get(sigla=conselho) if conselho else None

            if conselho:
                funcao.conselhos_permitidos.add(conselho)
        except Exception as e:
            print(e)

        try:
            funcao.ocupacoes_permitidas.add(ocupacao)
        except Exception as e:
            print(e)

