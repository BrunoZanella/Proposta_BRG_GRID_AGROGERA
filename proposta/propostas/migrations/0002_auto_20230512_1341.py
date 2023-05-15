# Generated by Django 3.0.6 on 2023-05-12 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_produto'),
        ('propostas', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='produto_proposta',
            options={'verbose_name': 'Produto', 'verbose_name_plural': 'Produtos'},
        ),
        migrations.AlterField(
            model_name='produto_proposta',
            name='produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Produto'),
        ),
    ]