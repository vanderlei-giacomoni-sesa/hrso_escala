# Generated by Django 5.0.2 on 2024-03-02 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0003_alter_contrato_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='status',
            field=models.CharField(choices=[('cadastro', 'Cadastro'), ('vigente', 'Vigente'), ('vigente com aditivo', 'Vigente Aditivado'), ('aditivado em quantidade', 'Aditivo Quantidade'), ('encerrdo', 'Encerrado'), ('rescindido', 'Rescindido')], default='cadastro', max_length=30),
        ),
    ]
