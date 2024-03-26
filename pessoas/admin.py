from django.contrib import admin
from pessoas.models import (Unidade, PessoaFisica, PessoaFisicaUsuario, Setor, VinculoPessoaFisicaSetor,
                            VinculoFuncional, Profissional)
# Register your models here.

admin.site.register(Unidade)
admin.site.register(PessoaFisica)
admin.site.register(PessoaFisicaUsuario)
admin.site.register(Setor)
admin.site.register(VinculoPessoaFisicaSetor)
admin.site.register(VinculoFuncional)
admin.site.register(Profissional)
