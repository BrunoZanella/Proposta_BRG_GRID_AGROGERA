# Generated by Django 3.0.6 on 2023-05-15 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('propostas', '0003_auto_20230512_1348'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='produto_proposta',
            options={'ordering': ['-produto'], 'verbose_name': 'Produto', 'verbose_name_plural': 'Produtos'},
        ),
    ]
