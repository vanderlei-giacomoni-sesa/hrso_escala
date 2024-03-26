from django.db.models import F, Max
from contratos.models import LoteContrato, LoteLicitacao, ItemLoteContrato, \
    ItemLoteLicitacao, AditivoContrato, UnidadesMedida


def dados_contratos(filter_contratos):
    return filter_contratos.values(
            'numero_contrato', 'id', 'slug').annotate(fornecedor=F('fornecedor_contratado__razao_social_fornecedor'))


def dados_item_contrato(i, max_var_i):
    print(i, max_var_i)
    i['unidade_medida'] = UnidadesMedida(i['unidade_medida']).label
    i['str_numero_item'] = f"{i['numero_item']}.{i['var_num_item']}" if max_var_i >= 1 else str(i['numero_item'])
    return i


def buscar_ultimo_aditivo_contrato(contrato_referencia):
    if AditivoContrato.objects.filter(contrato_referencia=contrato_referencia).count() > 0:
        seq_ua = AditivoContrato.objects.filter(
            contrato_referencia=contrato_referencia
        ).aggregate(Max('sequencia_aditivo'))['sequencia_aditivo__max']  # seq_ua

        return AditivoContrato.objects.get(contrato_referencia=contrato_referencia, sequencia_aditivo=seq_ua)
    else:
        return None


def buscar_lotes_contrato(contrato_referencia):
    lotes_licitacao = LoteLicitacao.objects.filter(
        licitacao_referencia=contrato_referencia.licitacao_referencia
    ).values('id', 'numero_lote', "descricao_lote")

    lotes_contrato = LoteContrato.objects.filter(contrato_referencia=contrato_referencia).values(
        'id', 'lote_referencia__id', 'lote_referencia__numero_lote', 'lote_referencia__descricao_lote',
        'contrato_referencia__id').order_by('lote_referencia__numero_lote')

    lista_lotes_licitacao = list(lotes_licitacao)
    lista_lotes_vinculados_contrato = [{'id': lote['lote_referencia__id'],
                                        'numero_lote': lote['lote_referencia__numero_lote'],
                                        "descricao_lote": lote['lote_referencia__descricao_lote'],
                                        } for lote in lotes_contrato]

    lista_lotes_contrataveis = [lote for lote in lista_lotes_licitacao if lote not in lista_lotes_vinculados_contrato]

    lista_lotes_contratados = [buscar_itens_lote_contrato(lote) for lote in lotes_contrato]

    return lista_lotes_contratados, lista_lotes_contrataveis


def buscar_itens_lote_contrato(lote_contrato):
    itens_lote_licitacao = ItemLoteLicitacao.objects.filter(
        lote_licitacao_refecencia__id=lote_contrato['lote_referencia__id']
    ).values('id', 'numero_item', 'var_num_item', 'descricao_item', 'unidade_medida', 'quantidade_licitada', 'valor_licitado').order_by('numero_item')

    max_item = itens_lote_licitacao.aggregate(
        max=Max('var_num_item'))['max']

    itens_lote_vinculados_contrato = ItemLoteContrato.objects.filter(
        lote_contrato_referencia__id=lote_contrato['id'], ativo=True
    ).values('id',
             'item_licitacao_referencia__id',
             'item_licitacao_referencia__numero_item',
             'item_licitacao_referencia__var_num_item',
             'item_licitacao_referencia__unidade_medida',
             'item_licitacao_referencia__descricao_item',
             'valor_item',
             'quantidade_contratada',
             'ativo').order_by('item_licitacao_referencia__numero_item')

    lista_id_itens_lote_vinculados_contrato = [item['item_licitacao_referencia__id'] for item in itens_lote_vinculados_contrato]

    lista_itens_lote_vinculados_contrato = [dados_item_contrato(
        {'id': item['id'],
         'item_licitacao_referencia__id': item['item_licitacao_referencia__id'],
         'numero_item': item['item_licitacao_referencia__numero_item'],
         'var_num_item': item['item_licitacao_referencia__var_num_item'],
         'unidade_medida': item['item_licitacao_referencia__unidade_medida'],
         'descricao_item': item['item_licitacao_referencia__descricao_item'],
         'valor_item': item['valor_item'],
         'quantidade_contratada': item['quantidade_contratada'],
         'ativo': item['ativo'],
         'valor_total_faturado': [0 , 0] # calcular_valor_total_faturado_item_contrato - plantoes_pagos['pagamentos_totais'] or 0, segundos_totais
         }, max_item) for item in itens_lote_vinculados_contrato]

    lista_itens_lote_licitacao_vinculaveis = [dados_item_contrato(item, max_item) for item in itens_lote_licitacao if item['id'] not in lista_id_itens_lote_vinculados_contrato]

    return {'id': lote_contrato['id'],
            'lote_referencia__id': lote_contrato['lote_referencia__id'],
            'numero_lote': lote_contrato['lote_referencia__numero_lote'],
            'descricao_lote': lote_contrato['lote_referencia__descricao_lote'],
            'itens_vinculados': lista_itens_lote_vinculados_contrato, #list(itens_lote_vinculados_contrato),
            'itens_vinculaveis': lista_itens_lote_licitacao_vinculaveis}

