from django.db import models
from django.db.models import Max, Q, F
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from localflavor.br.models import *
from pessoas.models import Unidade
from comuns.models import Fornecedor

# Create your models here.


class ModalidadeLicitacao(models.Model):
    nome_modalidade = models.CharField(max_length=30, verbose_name='nome da modalidade')
    modalidade_faturavel = models.BooleanField(default=True)


class Licitacao(models.Model):
    modalidade_licitacao = models.ForeignKey(ModalidadeLicitacao, on_delete=models.PROTECT)
    numero_licitacao = models.CharField(max_length=200)
    objeto = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    cadastro_finalizado = models.BooleanField(default=False)
    licitacao_ativa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "licitação"
        verbose_name_plural = "licitações"

    def __str__(self):
        nome_str = '{0} {1}'.format(self.modalidade_licitacao, self.numero_licitacao)

        return nome_str

    def save(self, *args, **kwargs):
        super(Licitacao, self).save(*args, **kwargs)
        if not self.slug:
            nome_slug = '{0}{1}'.format(self.modalidade_licitacao, self.numero_licitacao)
            self.slug = slugify(nome_slug)
            self.save()


class LoteLicitacao(models.Model):
    numero_lote = models.IntegerField()
    descricao_lote = models.CharField(max_length=200)
    licitacao_referencia = models.ForeignKey(Licitacao, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=200)

    class Meta:
        ordering = ['numero_lote']
        verbose_name = "lote da licitação"
        verbose_name_plural = "lotes da licitação"

    def __str__(self):
        return str(self.numero_lote)

    def save(self, *args, **kwargs):
        super(LoteLicitacao, self).save(*args, **kwargs)
        if not self.slug:
            nome_slug = '{0}{1}{2}'.format(self.licitacao_referencia.id, self.numero_lote, self.descricao_lote)
            self.slug = slugify(nome_slug)
            self.save()


class ItemLoteLicitacao(models.Model):
    numero_item = models.IntegerField()
    var_num_item = models.IntegerField(default=0)
    descricao_item = models.CharField(max_length=200)
    informacoes_complementares = models.TextField(blank=True, null=True)
    lote_licitacao_refecencia = models.ForeignKey(LoteLicitacao, on_delete=models.CASCADE)
    quantidade_licitada = models.FloatField()
    valor_licitado = models.FloatField()
    slug = models.SlugField(unique=True, max_length=200)

    class Meta:
        ordering = ['lote_licitacao_refecencia']
        verbose_name = "item"
        verbose_name_plural = "itens"

    def __str__(self):
        return '{0}.{1}-{2}-{3}'.format(
            self.numero_item,
            self.lote_licitacao_refecencia.numero_lote,
            self.lote_licitacao_refecencia.licitacao_referencia.numero_licitacao,
            self.descricao_item
        )

    def save(self, *args, **kwargs):
        super(ItemLoteLicitacao, self).save(*args, **kwargs)
        if not self.slug:
            nome_slug = '{0}{1}'.format(self.id, self.descricao_item)
            self.slug = slugify(nome_slug)
            self.save()


class ItemLicitacaoUnidade(models.Model):
    item = models.ForeignKey(ItemLoteLicitacao, on_delete=models.CASCADE)
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE)


class Contrato(models.Model):
    class StatusChoices(models.TextChoices):
        CADASTRO = 'cadastro'
        VIGENTE = 'vigente'
        VIGENTE_ADITIVADO = 'vigente com aditivo'
        ENCERRADO = 'encerrdo'
        RESCINDIDO = 'rescindido'

    STATUS_VIGENTES = [StatusChoices.VIGENTE, StatusChoices.VIGENTE_ADITIVADO]

    STATUS_ENCERADOS = [StatusChoices.ENCERRADO, StatusChoices.RESCINDIDO]

    status = models.CharField(choices=StatusChoices.choices, max_length=20, default=StatusChoices.CADASTRO)
    unidade_contrato = models.ForeignKey(Unidade, on_delete=models.PROTECT)
    numero_contrato = models.CharField(max_length=200)
    licitacao_referencia = models.ForeignKey(Licitacao, on_delete=models.CASCADE)
    fornecedor_contratado = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    inicio_vigencia = models.DateField()
    fim_vigencia = models.DateField()
    aditivado = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, max_length=200)

    motivo_rescisao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "contrato"
        verbose_name_plural = "contratos"

    def __str__(self):
        return self.numero_contrato

    def save(self, *args, **kwargs):
        super(Contrato, self).save(*args, **kwargs)
        if not self.slug:
            nome_slug = '{1}-{0}'.format(self.numero_contrato, self.id)
            self.slug = slugify(nome_slug)
            self.save()


class LoteContrato(models.Model):
    contrato_referencia = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    lote_referencia = models.ForeignKey(LoteLicitacao, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=200)

    class Meta:
        ordering = ['lote_referencia']

    def __str__(self):
        return str(self.lote_referencia.numero_lote)

    def save(self, *args, **kwargs):
        nome_salvar = '{0}{1}{2}'.format(self.contrato_referencia.id,
                                       self.lote_referencia.numero_lote, self.lote_referencia.id)
        self.slug = slugify(nome_salvar)
        super(LoteContrato, self).save(*args, **kwargs)


class UnidadesMedida(models.TextChoices):
    UNIDADE = "UNID", _("unidade")
    HORA = "H", _("hora")
    DIAS = "D", _('dia')


class ItemLoteContrato(models.Model):
    unidade_medida = models.CharField(choices=UnidadesMedida.choices, max_length=15)
    lote_contrato_referencia = models.ForeignKey(LoteContrato, on_delete=models.CASCADE)
    item_licitacao_referencia = models.ForeignKey(ItemLoteLicitacao, on_delete=models.CASCADE)
    valor_item = models.FloatField()
    quantidade_contratada = models.FloatField()
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['item_licitacao_referencia']
        verbose_name = "item do contrato"
        verbose_name_plural = "itens do contrato"

    def __str__(self):
        return '{3} - L{0}I{1} - {2}'.format(self.lote_contrato_referencia.lote_referencia.numero_lote,
                                      self.item_licitacao_referencia.numero_item,
                                      self.item_licitacao_referencia.descricao_item,
                                      self.lote_contrato_referencia.contrato_referencia.numero_contrato)


class AditivoContrato(models.Model):

    ADITIVO = 'Aditivo'
    APOSTILAMENTO = 'Apostilamento'
    TIPO_ADITIVO_CHOICES = [
        (ADITIVO, ADITIVO),
        (APOSTILAMENTO, APOSTILAMENTO)
    ]

    numero_aditivo = models.IntegerField()
    contrato_referencia = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    inicio_vigencia = models.DateField()
    fim_vigencia = models.DateField()
    slug = models.SlugField(unique=True, max_length=200)

    tipo_aditivo = models.CharField(choices=TIPO_ADITIVO_CHOICES, max_length=50, default=ADITIVO)
    sequencia_aditivo = models.IntegerField()

    aditivo_editavel = models.BooleanField(default=True)

    class Meta:
        ordering = ['numero_aditivo']
        verbose_name = "aditivo"
        verbose_name_plural = "aditivos"

    def __str__(self):
        nome_aditivo = '{0}º {1} {2}'.format(self.numero_aditivo, self.tipo_aditivo, self.contrato_referencia.numero_contrato)
        return nome_aditivo

    def save(self, *args, **kwargs):
        if not self.sequencia_aditivo:
            if not AditivoContrato.objects.filter(contrato_referencia=self.contrato_referencia).exists():
                self.sequencia_aditivo = 1
            else:
                #self.sequencia_aditivo = AditivoContrato.objects.filter(contrato_referencia=self.contrato_referencia).count() + 1
                self.sequencia_aditivo = AditivoContrato.objects.filter(
                    contrato_referencia=self.contrato_referencia
                ).aggregate(Max('sequencia_aditivo'))['sequencia_aditivo__max'] + 1
        super(AditivoContrato, self).save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify('{0} {1} {2} {3}'.format(self.id, self.numero_aditivo,
                                                         self.contrato_referencia.id, self.contrato_referencia.numero_contrato))
            self.save()


class LoteAditivoContrato(models.Model):
    aditivo_referencia = models.ForeignKey(AditivoContrato, on_delete=models.CASCADE)
    lote_contrato_referencia = models.ForeignKey(LoteContrato, on_delete=models.CASCADE)

    class Meta:
        ordering = ['lote_contrato_referencia']

    def __str__(self):
        nome = 'lote {0} {1} Aditivo contrato {2}'.format(self.lote_contrato_referencia.lote_referencia.numero_lote,
                                             self.aditivo_referencia.numero_aditivo,
                                                          self.aditivo_referencia.contrato_referencia.numero_contrato)
        return nome


class ItemLoteAditivo(models.Model):
    lote_aditivo_referencia = models.ForeignKey(LoteAditivoContrato, on_delete=models.CASCADE)
    item_contrato_referencia = models.ForeignKey(ItemLoteContrato, on_delete=models.CASCADE)
    quantidade_aditivada = models.FloatField()
    preco_aditivado = models.FloatField()
    item_aditivo_ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['item_contrato_referencia']
        verbose_name = "item do aditivo"
        verbose_name_plural = "itens dos aditivos"

    def __str__(self):
        return "{1}-{2}-{0}".format(self.item_contrato_referencia.item_licitacao_referencia.numero_item,
                                self.lote_aditivo_referencia.aditivo_referencia.contrato_referencia.numero_contrato,
                                self.lote_aditivo_referencia.aditivo_referencia.numero_aditivo)



