# Generated by Django 5.0.3 on 2024-03-25 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escala_geral', '0003_horarioplantao_equipe_horario_equipe_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='horarioplantao',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
    ]
