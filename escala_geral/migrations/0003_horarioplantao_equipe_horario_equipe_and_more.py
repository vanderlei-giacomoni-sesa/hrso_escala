# Generated by Django 5.0.3 on 2024-03-25 13:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escala_geral', '0002_remove_plantao_indice_plantao_escala_equipe_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HorarioPlantao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horario_inicio', models.TimeField()),
                ('duracao_plantao', models.DurationField()),
                ('duracao_folga', models.DurationField()),
                ('horario_almoco', models.TimeField(blank=True, null=True)),
                ('duracao_almoco', models.DurationField(blank=True, null=True)),
                ('folga_sabado', models.BooleanField(default=False)),
                ('folga_domingo', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='equipe',
            name='horario_equipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='escala_geral.horarioplantao'),
        ),
        migrations.AddField(
            model_name='equipeescalamensal',
            name='horario_equipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='escala_geral.horarioplantao'),
        ),
    ]
