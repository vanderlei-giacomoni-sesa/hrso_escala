# Generated by Django 5.0.2 on 2024-02-21 20:04

import django.db.models.deletion
import localflavor.br.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comuns', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PessoaFisica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_cadastro', models.DateField(auto_now=True)),
                ('nome', models.CharField(max_length=200)),
                ('cpf', localflavor.br.models.BRCPFField(max_length=14)),
                ('slug', models.SlugField(max_length=250)),
                ('cns', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='PessoaFisicaUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pessoa_fisica', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pessoas.pessoafisica')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profissional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('cbo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='comuns.ocupacao')),
                ('funcao', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='comuns.funcao')),
                ('pessoa_fisica', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pessoas.pessoafisica')),
            ],
        ),
        migrations.CreateModel(
            name='Unidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_unidade', models.CharField(max_length=100)),
                ('sigla_unidade', models.CharField(max_length=100)),
                ('nome_cargo_diretor', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=125)),
                ('diretor_unidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pessoas.pessoafisica')),
            ],
        ),
        migrations.CreateModel(
            name='Setor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_setor', models.CharField(max_length=100)),
                ('sigla_setor', models.CharField(max_length=10)),
                ('cargo_responsavel_setor', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('setor_ativo', models.BooleanField(default=True)),
                ('responsavel_setor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pessoas.pessoafisica')),
                ('setor_pai', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pessoas.setor')),
                ('unidade_referencia', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pessoas.unidade')),
            ],
            options={
                'verbose_name': 'setor',
                'verbose_name_plural': 'setores',
                'ordering': ['nome_setor'],
            },
        ),
        migrations.CreateModel(
            name='VinculoFuncional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vinculo_ativo', models.BooleanField(default=True)),
                ('tipo_vinculo', models.IntegerField(choices=[(1, 'SESA'), (2, 'FUNEAS'), (3, 'CONTRATO'), (4, 'ACADEMICO')])),
                ('id_meta4', models.IntegerField(blank=True, null=True)),
                ('id_ato_formal', models.CharField(blank=True, null=True)),
                ('cnpj_vinculo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='comuns.fornecedor')),
                ('profissional', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pessoas.profissional')),
            ],
        ),
        migrations.CreateModel(
            name='VinculoColaboradorUnidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('inicio_vinculo', models.DateField(auto_now_add=True)),
                ('fim_vinculo', models.DateField(blank=True, null=True)),
                ('unidade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pessoas.unidade')),
                ('vinculo_funcional', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pessoas.vinculofuncional')),
            ],
        ),
        migrations.CreateModel(
            name='LancamentoContrachequeMeta4',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_lancamento', models.IntegerField()),
                ('descricao_lancamento', models.CharField(max_length=200)),
                ('valor_vantagem', models.FloatField()),
                ('valor_desconto', models.FloatField()),
                ('periodo_referencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comuns.periodoreferencia')),
                ('vinculo_funcional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pessoas.vinculofuncional')),
            ],
        ),
        migrations.CreateModel(
            name='DadosCadastraisMeta4',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rg', models.CharField(max_length=200)),
                ('t_emp', models.CharField(max_length=200)),
                ('nascimento', models.DateField()),
                ('pis', models.CharField(max_length=200)),
                ('admissao', models.DateField()),
                ('carga_horaria', models.IntegerField()),
                ('cargo', models.CharField(max_length=200)),
                ('classe', models.CharField(max_length=200)),
                ('referencia_classe', models.CharField(max_length=200)),
                ('cidade', models.CharField(max_length=200)),
                ('estado', models.CharField(max_length=200)),
                ('local', models.CharField(max_length=200)),
                ('quadro', models.TextField(max_length=200)),
                ('funcao', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='comuns.funcao')),
                ('periodo_referencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comuns.periodoreferencia')),
                ('vinculo_funcional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pessoas.vinculofuncional')),
            ],
        ),
        migrations.CreateModel(
            name='VinculoPessoaFisicaSetor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio_vinculo', models.DateField(auto_now_add=True)),
                ('ativo', models.BooleanField(default=True)),
                ('fim_vinculo', models.DateField(blank=True, null=True)),
                ('setor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pessoas.setor')),
                ('vinculo_unidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pessoas.vinculocolaboradorunidade')),
            ],
        ),
    ]
