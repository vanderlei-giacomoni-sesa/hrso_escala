from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from localflavor.br.models import *

from comuns.models import PeriodoReferencia, Ocupacao, ConselhoProfissional, Funcao
from pessoas.models import PessoaFisica, Setor, Profissional


# Create your models here.


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
    regime_escala = models.CharField(choices=RegimeEscala, max_length=10)

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


class HorarioPlantao(models.Model):
    ativo = models.BooleanField(default=True)
    horario_inicio = models.TimeField()
    duracao_plantao = models.DurationField()
    duracao_folga = models.DurationField()
    inicio_almoco = models.DurationField(blank=True, null=True)
    duracao_almoco = models.DurationField(blank=True, null=True)
    folga_sabado = models.BooleanField(default=False)
    folga_domingo = models.BooleanField(default=False)


class Equipe(models.Model):
    escala = models.ForeignKey(Escala, on_delete=models.PROTECT)
    nome = models.CharField(max_length=50, verbose_name="Equipe")
    horario_equipe = models.ForeignKey(HorarioPlantao, on_delete=models.PROTECT, blank=True, null=True)


class EquipeEscalaMensal(models.Model):
    escala_mensal = models.ForeignKey(EscalaMensal, on_delete=models.PROTECT)
    equipe_referencia = models.ForeignKey(Equipe, on_delete=models.PROTECT)
    horario_equipe = models.ForeignKey(HorarioPlantao, on_delete=models.PROTECT, blank=True, null=True)


class Plantao(models.Model):
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    dia_plantao = models.DateField(db_index=True)

    horario_entrada = models.TimeField(null=True, blank=True)
    duracao_plantao = models.DurationField(null=True, blank=True)
    saida = models.DateTimeField(null=True, blank=True)
    plantao_faturado = models.BooleanField(default=False)


class Folga(models.Model):
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    dia_folga = models.DateField(db_index=True)









