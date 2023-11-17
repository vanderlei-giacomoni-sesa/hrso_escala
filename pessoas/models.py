from django.contrib.auth.models import User, Group
from django.db import models
from django.utils.text import slugify
from localflavor.br.models import *
from django.core.exceptions import ValidationError

from comuns.models import PeriodoReferencia, Fornecedor


class PessoaFisica(models.Model):
    data_cadastro = models.DateField()
    nome = models.CharField(max_length=200)
    cpf = BRCPFField()
    slug = models.SlugField(max_length=250)
    cns = models.SlugField(max_length=30, blank=True, null=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        super(PessoaFisica, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify('{0}-{1}'.format(self.id, self.nome))
            self.save()


class PessoaFisicaUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    pessoa_fisica = models.ForeignKey(PessoaFisica, on_delete=models.PROTECT)


class Unidade(models.Model):
    nome_unidade = models.CharField(max_length=100)
    sigla_unidade = models.CharField(max_length=100)
    diretor_unidade = models.ForeignKey(PessoaFisica, on_delete=models.CASCADE)
    nome_cargo_diretor = models.CharField(max_length=100)
    slug = models.SlugField(max_length=125)

    def __str__(self):
        return self.sigla_unidade

    def save(self, *args, **kwargs):
        super(Unidade, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify('{0}-{1}'.format(self.id, self.sigla_unidade))
            self.save()


class Setor(models.Model):
    unidade_referencia = models.ForeignKey(Unidade, on_delete=models.PROTECT)
    nome_setor = models.CharField(max_length=100)
    sigla_setor = models.CharField(max_length=10)
    responsavel_setor = models.ForeignKey(PessoaFisica, on_delete=models.PROTECT)
    cargo_responsavel_setor = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=200)
    setor_ativo = models.BooleanField(default=True)
    setor_pai = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        ordering = ['nome_setor']
        verbose_name = "setor"
        verbose_name_plural = "setores"

    def __str__(self):
        return self.nome_setor

    def save(self, *args, **kwargs):
        super(Setor, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify('{0}{1}'.format(self.id, self.nome_setor))
            self.save()


# Criar multiplos vinculos, manter apenas 1 ativo
class VinculoPessoaFisicaSetor(models.Model):
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT)
    pessoa_fisica = models.ForeignKey(PessoaFisica, on_delete=models.CASCADE)
    inicio_vinculo = models.DateField()
    ativo = models.BooleanField(default=True)
    fim_vinculo = models.DateField()

    def clean(self):
        if VinculoPessoaFisicaSetor.objects.filter(
                setor=self.setor, pessoa_fisica=self.pessoa_fisica, ativo=True).exists():
            raise ValidationError("Ja existe um vinculo vijente entre colaborador e setor")


#Strategy
class VinculoFuncional(models.Model):
    cpf = models.ForeignKey(PessoaFisica, on_delete=models.CASCADE)
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE)
    vinculo_ativo = models.BooleanField(default=True)

    class Meta:
        abstract = True


class VinculoMeta4(VinculoFuncional):
    id_meta4 = models.IntegerField()
    id_ato_formal = models.CharField(max_length=200)


class VinculoCnpj(VinculoFuncional):
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)


class VinculoFuneas(VinculoFuncional):
    pass


class LancamentoContrachequeMeta4(models.Model):
    periodo_referencia = models.ForeignKey(PeriodoReferencia, on_delete=models.CASCADE)
    vinculo_meta4 = models.ForeignKey(VinculoMeta4, on_delete=models.CASCADE)
    id_lancamento = models.IntegerField()
    descricao_lancamento = models.CharField(max_length=200)
    valor_vantagem = models.FloatField()
    valor_desconto = models.FloatField()


class DadosCadastraisMeta4(models.Model):
    id_vinculo_meta4 = models.ForeignKey(VinculoMeta4, on_delete=models.CASCADE)
    periodo_referencia = models.ForeignKey(PeriodoReferencia, on_delete=models.CASCADE)
    rg = models.CharField(max_length=200)
    t_emp = models.CharField(max_length=200)
    nascimento = models.DateField()
    pis = models.CharField(max_length=200)
    admissao = models.DateField()
    carga_horaria = models.IntegerField()
    cargo = models.CharField(max_length=200)
    funcao = models.CharField(max_length=200)
    classe = models.CharField(max_length=200)
    referencia_classe = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    local = models.CharField(max_length=200)
    quadro = models.TextField(max_length=200)














