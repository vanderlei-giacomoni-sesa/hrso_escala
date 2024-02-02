import os
from comuns.models import Ocupacao


def ler_arquivo_ocupacoes(a):
    with open(a) as f:
        linhas_relatorio = [l.replace('\n', '').split(';') for l in f.readlines()]

        for l in linhas_relatorio[1:]:
            ocupacao, created = Ocupacao.objects.update_or_create(codigo_cbo=l[0], defaults={'titulo': l[1]})
            print(ocupacao, created)





