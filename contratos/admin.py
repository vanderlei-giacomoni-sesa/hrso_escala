from django.contrib import admin

from contratos.models import *

# Register your models here.

admin.site.register(Licitacao)
admin.site.register(LoteLicitacao)
admin.site.register(ItemLoteLicitacao)
admin.site.register(Contrato)
admin.site.register(ItemLoteContrato)
admin.site.register(ItemLoteAditivo)
admin.site.register(LoteContrato)
admin.site.register(LoteAditivoContrato)
admin.site.register(AditivoContrato)
admin.site.register(AditivoQuantidade)
admin.site.register(QuantidadeAditivada)


