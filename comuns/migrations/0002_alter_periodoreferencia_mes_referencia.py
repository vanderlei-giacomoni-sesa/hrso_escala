# Generated by Django 5.0.1 on 2024-02-02 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comuns', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodoreferencia',
            name='mes_referencia',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)], default=2),
        ),
    ]