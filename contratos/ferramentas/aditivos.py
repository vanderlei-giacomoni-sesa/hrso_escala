from django.db.models import F, Max
from contratos.models import (LoteAditivoContrato, LoteLicitacao, ItemLoteAditivo, ItemLoteLicitacao,
                              ItemLoteContrato, AditivoContrato, Contrato, UnidadesMedida)



class DadosAditivoContrato:
    def __init__(self, contrato: Contrato, aditivo: AditivoContrato):
        self.contrato = contrato
        self.aditivo = aditivo

    @staticmethod
    def dados_item_aditivo(i, max_var_i):
        print(i, max_var_i)
        i['unidade_medida'] = UnidadesMedida(i['unidade_medida']).label
        i['str_numero_item'] = f"{i['numero_item']}.{i['var_num_item']}" if max_var_i >= 1 else str(i['numero_item'])

        return i

    def processar_lotes_contrataveis(self):
        lotes_aditivo = [l['lote_contrato_referencia__lote_referencia__numero_lote'] for l in
                         LoteAditivoContrato.objects.filter(
                             aditivo_referencia__id=self.aditivo['id']
                         ).values('lote_contrato_referencia__lote_referencia__numero_lote')]

        lotes_licitacao = LoteLicitacao.objects.filter(
            licitacao_referencia=self.contrato.licitacao_referencia
        ).values('id', 'numero_lote', 'descricao_lote')

        return [dict(l) for l in lotes_licitacao if l['numero_lote'] not in lotes_aditivo]

    def processar_lotes_aditivados(self):
        lotes_aditivo = LoteAditivoContrato.objects.filter(
            aditivo_referencia__id=self.aditivo['id']
        ).values('id', 'lote_contrato_referencia__id', 'lote_contrato_referencia__lote_referencia__id',
                 'lote_contrato_referencia__lote_referencia__numero_lote',
                 'lote_contrato_referencia__lote_referencia__descricao_lote')

        return [{'id': lote['id'],
                 'id_lote_contrato': lote['lote_contrato_referencia__id'],
                 'id_lote_licitacao': lote['lote_contrato_referencia__lote_referencia__id'],
                 'numero_lote': lote['lote_contrato_referencia__lote_referencia__numero_lote'],
                 "descricao_lote": lote['lote_contrato_referencia__lote_referencia__descricao_lote'],
                 'itens_aditivados': self.buscar_itens_lote_aditivo(lote['id']),
                 'itens_aditivaveis': self.buscar_itens_lote_aditivaveis(
                     lote['id'], lote['lote_contrato_referencia__lote_referencia__id'])
                 } for lote in lotes_aditivo]


    def buscar_itens_lote_aditivaveis(self, id_lote_aditivo, id_lote_licitacao):
        itens_aditivados = ItemLoteAditivo.objects.filter(
            lote_aditivo_referencia__id=id_lote_aditivo, item_aditivo_ativo=True
        ).values('id', 'item_contrato_referencia__id',
                 'item_contrato_referencia__item_licitacao_referencia__numero_item',
                 'item_contrato_referencia__item_licitacao_referencia__var_num_item',
                 'item_contrato_referencia__item_licitacao_referencia__id')



        itens_lote_licitacao = ItemLoteLicitacao.objects.filter(
            lote_licitacao_refecencia__id=id_lote_licitacao).values(
            'id',
            'numero_item',
            'var_num_item',
            'descricao_item',
            'unidade_medida',
            'quantidade_licitada',
            'valor_licitado',
        ).order_by('numero_item')

        max_var_i = itens_lote_licitacao.aggregate(
            max=Max('var_num_item'))['max']

        list_id_itens_lote_licitacao_itens_aditivados = [
            item['item_contrato_referencia__item_licitacao_referencia__id'] for item in itens_aditivados]

        itens_lote_contrato_aditivaveis = [
            self.buscar_dados_item_aditivavel(
                item, max_var_i
            ) for item in itens_lote_licitacao if item['id'] not in list_id_itens_lote_licitacao_itens_aditivados
        ]

        return itens_lote_contrato_aditivaveis

    def buscar_dados_item_aditivavel(self, item, max_var_i):
        item_retornar = {
            'id_item_lote_licitacao': item['id'],
            'numero_item': item['numero_item'],
            'var_num_item': item['var_num_item'],
            'descricao_item': item['descricao_item'],
            'unidade_medida': item['unidade_medida'],
            'quantidade_contratada': item['quantidade_licitada'],
            'valor_item': item['valor_licitado']
        }
        uane = self.ultimo_aditivo_nao_editavel()
        # Verificar se o item esta presente no ultimo aditivo ativo (Nao editavel)  - Verifica se o contrato
        # tem um aditivo anterior, se possuir, verifica se possui o item em questao e atualiza quantidade e preço ###
        if uane and ItemLoteAditivo.objects.filter(item_contrato_referencia__item_licitacao_referencia__id=item['id'],
                                                   lote_aditivo_referencia__aditivo_referencia=uane).exists():
            item_lote_aditivo = ItemLoteAditivo.objects.get(
                item_contrato_referencia__item_licitacao_referencia__id=item['id'],
                lote_aditivo_referencia__aditivo_referencia=uane)

            item_retornar['quantidade_contratada'] = item_lote_aditivo.quantidade_aditivada
            item_retornar['valor_item'] = item_lote_aditivo.preco_aditivado
        elif ItemLoteContrato.objects.filter(
                item_licitacao_referencia__id=item['id'],
                lote_contrato_referencia__contrato_referencia=self.contrato, ativo=True).exists():
            ilc = ItemLoteContrato.objects.get(item_licitacao_referencia__id=item['id'],
                                               lote_contrato_referencia__contrato_referencia=self.contrato, ativo=True)
            item_retornar['quantidade_contratada'] = ilc.quantidade_contratada
            item_retornar['valor_item'] = ilc.valor_item
        else:
            print("VERIFICAR: ", item)

        return self.dados_item_aditivo(item_retornar, max_var_i)

    def buscar_itens_lote_aditivo(self, id_lote_aditivo):
        aditivo_lote = LoteAditivoContrato.objects.get(id=id_lote_aditivo).aditivo_referencia
        itens_lote_aditivo = ItemLoteAditivo.objects.filter(
            lote_aditivo_referencia_id=id_lote_aditivo, item_aditivo_ativo=True,
        ).values('id',
                 'lote_aditivo_referencia__aditivo_referencia__numero_aditivo',
                 'item_contrato_referencia__item_licitacao_referencia__id',
                 'item_contrato_referencia__item_licitacao_referencia__numero_item',
                 'item_contrato_referencia__item_licitacao_referencia__var_num_item',
                 'item_contrato_referencia__item_licitacao_referencia__descricao_item',
                 'item_contrato_referencia__item_licitacao_referencia__unidade_medida',
                 'preco_aditivado', 'quantidade_aditivada')

        max_var_i = itens_lote_aditivo.aggregate(
            max=Max('item_contrato_referencia__item_licitacao_referencia__var_num_item'))['max']

        return [self.dados_item_aditivo(
            {'id': item['id'],
             'id_item_lote_licitacao': item['item_contrato_referencia__item_licitacao_referencia__id'],
             'numero_item': item['item_contrato_referencia__item_licitacao_referencia__numero_item'],
             'var_num_item': item['item_contrato_referencia__item_licitacao_referencia__var_num_item'],
             "descricao_item": item['item_contrato_referencia__item_licitacao_referencia__descricao_item'],
             'unidade_medida': item['item_contrato_referencia__item_licitacao_referencia__unidade_medida'],
             'valor_item': item['preco_aditivado'],
             'quantidade_contratada': item['quantidade_aditivada'],
             'valor_total_faturado': 0#self.calcular_valor_total_faturado(item, aditivo_lote),
             }, max_var_i) for item in itens_lote_aditivo]

    def ultimo_aditivo_nao_editavel(self):
        if AditivoContrato.objects.filter(contrato_referencia=self.contrato, aditivo_editavel=False).count() > 0:
            seq_ua = AditivoContrato.objects.filter(
                contrato_referencia=self.contrato,
                aditivo_editavel=False
            ).aggregate(Max('sequencia_aditivo'))['sequencia_aditivo__max']
            return AditivoContrato.objects.get(contrato_referencia=self.contrato, sequencia_aditivo=seq_ua)
        else:
            return None
