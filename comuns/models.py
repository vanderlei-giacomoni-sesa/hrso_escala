from django.db import models
from django.utils.text import slugify

from localflavor.br.models import *

from datetime import date, datetime

# Create your models here.


class PeriodoReferencia(models.Model):
    ANO_CHOICES = [(y, y) for y in range(2019, date.today().year + 2)]
    MES_CHOICES = [(m, m) for m in range(1, 13)]
    ano_referencia = models.IntegerField(choices=ANO_CHOICES, default=datetime.now().year)
    mes_referencia = models.IntegerField(choices=MES_CHOICES, default=datetime.now().month)
    slug = models.SlugField(unique=True, max_length=200)

    class Meta:
        ordering = ['ano_referencia', 'mes_referencia']

    def __str__(self):
        return '{0}/{1}'.format(self.mes_referencia, self.ano_referencia)

    def save(self, *args, **kwargs):
        if 0 < int(self.mes_referencia) < 13:
            super(PeriodoReferencia, self).save(*args, **kwargs)
            if not self.slug:
                self.slug = slugify('{0}{1}{2}'.format(self.id, self.mes_referencia, self.ano_referencia))
                self.save()
        else:
            return ValueError


class Fornecedor(models.Model):
    cnpj_fornecedor = BRCNPJField()
    nome_fantasia = models.CharField(max_length=200)
    razao_social_fornecedor = models.CharField(max_length=200)
    nome_banco = models.CharField(max_length=200)
    codigo_banco = models.CharField(max_length=200)
    agencia_banco = models.CharField(max_length=200)
    conta_fornecedor = models.CharField(max_length=200)
    endereco_fornecedor = models.CharField(max_length=200)
    cep_fornecedor = BRPostalCodeField()
    bairro_fornecedor = models.CharField(max_length=200)
    cidade_fornecedor = models.CharField(max_length=200)
    estado_fornecedor = BRStateField()
    telefone_fornecedor = models.CharField(max_length=200)
    contato_fornecedor = models.CharField(max_length=200)
    email_fornecedor = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)

    class Meta:
        verbose_name = "fornecedor"
        verbose_name_plural = "fornecedores"

    def __str__(self):
        return self.razao_social_fornecedor

    def save(self, *args, **kwargs):
        super(Fornecedor, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify('{0} {1}'.format(self.id, self.razao_social_fornecedor))
            self.save()


class Ocupacao(models.Model):
    codigo_cbo = models.CharField(max_length=6)
    titulo = models.CharField(max_length=250)

    def __str__(self):
        return self.titulo


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
