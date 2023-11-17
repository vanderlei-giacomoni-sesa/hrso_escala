from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from localflavor.br.models import *

from comuns.models import PeriodoReferencia
from pessoas.models import PessoaFisica, Setor

from datetime import date, datetime

# Create your models here.

# Substitui Especialidade
class Ocupacao(models.Model):
    codigo_cbo = models.CharField(max_length=6)
    titulo = models.CharField(max_length=250)


class ConselhoProfissional(models.Model):
    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=20)

    def __str__(self):
        return self.sigla


class Funcao(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=200)
    ativa = models.BooleanField(default=True)
    funcao_medica = models.BooleanField(default=True)
    conselhos_permitidos = models.ManyToManyField(ConselhoProfissional, blank=True)
    ocupacoes_permitidas = models.ManyToManyField(Ocupacao, blank=True)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        super(Funcao, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify('{0}{1}'.format(self.id, self.nome))
            self.save()


class Profissional(models.Model):
    pessoa_fisica = models.ForeignKey(PessoaFisica, on_delete=models.PROTECT)
    funcao = models.ForeignKey(Funcao, on_delete=models.PROTECT)
    cbo = models.ForeignKey(Ocupacao, on_delete=models.PROTECT)


class DadosConselhoProfissional(models.Model):
    profissional = models.ForeignKey(Profissional, on_delete=models.PROTECT)
    conselho = models.ForeignKey(ConselhoProfissional, on_delete=models.PROTECT)
    estado_conselho = BRStateField()
    numero = models.CharField(max_length=30)


class RegimeEscala(models.TextChoices):
    PRESENCIAL = "P", _("presencial")
    SOBREAVISO = "S", _("sobreaviso")


class Escala(models.Model):
    escala_ativa = models.BooleanField(default=True)
    regime_escala = models.CharField(choices=RegimeEscala.choices, max_length=2)

    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)
    nome_escala = models.CharField(max_length=50, verbose_name="Nome da Escala")

    slug = models.SlugField(unique=True, max_length=200)

    class Meta:
        verbose_name = "escala"
        verbose_name_plural = "escalas"
        ordering = ['nome_escala']

    def __str__(self):
        return '{0}'.format(self.nome_escala)

    def save(self, *args, **kwargs):
        super(Escala, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify('{0}{1}'.format(self.id, self.nome_escala))
            self.save()


class EscalaMensal(models.Model):
    escala_referencia = models.ForeignKey(Escala, on_delete=models.PROTECT)
    escala_ativa = models.BooleanField(default=True)
    regime_escala = models.CharField(choices=RegimeEscala.choices, max_length=2)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)
    nome_escala = models.CharField(max_length=50, verbose_name="Nome da Escala")
    periodo = models.ForeignKey(PeriodoReferencia, on_delete=models.CASCADE)

    slug = models.SlugField(unique=True, max_length=200)

    class Meta:
        verbose_name = "escala"
        verbose_name_plural = "escalas"
        ordering = ['nome_escala']

    def __str__(self):
        return '{0}-{1}-{0}'.format(self.periodo.ano_referencia, self.periodo.mes_referencia, self.nome_escala)

    def save(self, *args, **kwargs):
        super(EscalaMensal, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify('{0}{1}{2}{3}'.format(
                self.periodo.ano_referencia, self.periodo.mes_referencia, self.id,self.nome_escala))
            self.save()


class Plantao(models.Model):
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    dia_plantao = models.DateField(db_index=True)

    indice_plantao_escala = models.IntegerField(null=True, blank=True)
    horario_entrada = models.TimeField(null=True, blank=True)
    duracao_plantao = models.DurationField(null=True, blank=True)
    saida = models.DateTimeField(null=True, blank=True)
    plantao_faturado = models.BooleanField(default=False)
