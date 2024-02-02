# Generated by Django 5.0.1 on 2024-01-30 16:12

import localflavor.br.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConselhoProfissional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('sigla', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnpj_fornecedor', localflavor.br.models.BRCNPJField(max_length=18)),
                ('nome_fantasia', models.CharField(max_length=200)),
                ('razao_social_fornecedor', models.CharField(max_length=200)),
                ('nome_banco', models.CharField(max_length=200)),
                ('codigo_banco', models.CharField(max_length=200)),
                ('agencia_banco', models.CharField(max_length=200)),
                ('conta_fornecedor', models.CharField(max_length=200)),
                ('endereco_fornecedor', models.CharField(max_length=200)),
                ('cep_fornecedor', localflavor.br.models.BRPostalCodeField(max_length=9)),
                ('bairro_fornecedor', models.CharField(max_length=200)),
                ('cidade_fornecedor', models.CharField(max_length=200)),
                ('estado_fornecedor', localflavor.br.models.BRStateField(max_length=2)),
                ('telefone_fornecedor', models.CharField(max_length=200)),
                ('contato_fornecedor', models.CharField(max_length=200)),
                ('email_fornecedor', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'fornecedor',
                'verbose_name_plural': 'fornecedores',
            },
        ),
        migrations.CreateModel(
            name='Ocupacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_cbo', models.CharField(max_length=6)),
                ('titulo', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='PeriodoReferencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano_referencia', models.IntegerField(choices=[(2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025)], default=2024)),
                ('mes_referencia', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)], default=1)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'ordering': ['ano_referencia', 'mes_referencia'],
            },
        ),
        migrations.CreateModel(
            name='Funcao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('ativa', models.BooleanField(default=True)),
                ('funcao_medica', models.BooleanField(default=True)),
                ('conselhos_permitidos', models.ManyToManyField(blank=True, to='comuns.conselhoprofissional')),
                ('ocupacoes_permitidas', models.ManyToManyField(blank=True, to='comuns.ocupacao')),
            ],
        ),
    ]
