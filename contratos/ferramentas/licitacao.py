from contratos.models import ItemLoteContrato, LoteLicitacao, UnidadesMedida, ItemLoteLicitacao, ModalidadeLicitacao
from django.db.models import Max


class DadosItemLicitacao:
    def __init__(self, item_licitacao):
        self.item = item_licitacao

    def dados_item_licitacao(self, max_var_i):
        if isinstance(self.item, ItemLoteLicitacao):
            self.item = {
                'id': self.item.id, 'numero_item':self.item.numero_item, 'var_num_item':self.item.var_num_item,
                'descricao_item':self.item.descricao_item, 'unidade_medida': self.item.unidade_medida,
                'quantidade_licitada': self.item.quantidade_licitada, 'valor_licitado': self.item.valor_licitado}

        self.item['unidade_medida'] = UnidadesMedida(self.item['unidade_medida']).label
        self.item[
            'str_numero_item'] = f"{self.item['numero_item']}.{self.item['var_num_item']}" if max_var_i >= 1 else str(
            self.item['numero_item'])

        return self.item


class DadosLoteLicitacao:
    def __init__(self, lote_licitacao):
        self.lote_licitacao = lote_licitacao

    @staticmethod
    def dados_item_licitacao(i, max_var_i):
        i['unidade_medida'] = UnidadesMedida(i['unidade_medida']).label
        i['str_numero_item'] = f"{i['numero_item']}.{i['var_num_item']}" if max_var_i >= 1 else str(i['numero_item'])

        return i

    def dados_lote_licitacao(self):
        itens_lote = ItemLoteLicitacao.objects.filter(
            lote_licitacao_refecencia__id=self.lote_licitacao['id']).values(
            'id', 'numero_item', 'var_num_item', 'descricao_item', 'unidade_medida', 'quantidade_licitada',
            'valor_licitado')
        max_var_i = itens_lote.aggregate(max=Max('var_num_item'))['max']
        self.lote_licitacao['itens_lote'] = [DadosItemLicitacao(i).dados_item_licitacao(max_var_i) for i in
                                        itens_lote] if itens_lote else []
        return self.lote_licitacao

