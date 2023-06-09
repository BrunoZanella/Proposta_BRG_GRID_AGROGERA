# Generated by Django 3.0.6 on 2023-05-12 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import proposta.core.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Acessorio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_acessorio', models.CharField(blank=True, max_length=9, unique=True, verbose_name='Código')),
                ('descricao', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nome')),
                ('imagem', models.ImageField(blank=True, upload_to='produtos/Acessorio_proposta')),
            ],
            options={
                'verbose_name': 'Acessórios',
                'verbose_name_plural': 'Acessório',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_pessoa_proposta', models.CharField(blank=True, max_length=100, verbose_name='Aos cuidados de:')),
                ('cnpj', models.CharField(blank=True, max_length=18, unique=True, validators=[proposta.core.models.validate_cnpj], verbose_name='CNPJ/CPF')),
                ('nome', models.CharField(blank=True, max_length=255)),
                ('fantasia', models.CharField(blank=True, max_length=255)),
                ('telefone', models.CharField(blank=True, max_length=50, verbose_name='telefone')),
                ('email', models.EmailField(blank=True, max_length=200, verbose_name='email')),
                ('CEP', models.CharField(blank=True, max_length=200, verbose_name='CEP')),
                ('bairro', models.CharField(blank=True, max_length=100, verbose_name='Bairro')),
                ('cidade', models.CharField(blank=True, max_length=100, verbose_name='Cidade')),
                ('estado', models.CharField(blank=True, max_length=2, null=True, verbose_name='Estado')),
                ('logradouro', models.CharField(blank=True, max_length=255)),
                ('numero', models.CharField(blank=True, max_length=255)),
                ('complemento', models.CharField(blank=True, max_length=255)),
                ('abertura', models.CharField(blank=True, max_length=255)),
                ('natureza_juridica', models.CharField(blank=True, max_length=255)),
                ('atividade_principal', models.TextField(blank=True, max_length=1000)),
                ('atividades_secundarias', models.TextField(blank=True, max_length=4000)),
                ('qsa', models.TextField(blank=True, max_length=1000)),
                ('situacao', models.CharField(blank=True, max_length=255)),
                ('data_situacao', models.CharField(blank=True, max_length=255)),
                ('motivo_situacao', models.CharField(blank=True, max_length=255)),
                ('situacao_especial', models.CharField(blank=True, max_length=255)),
                ('data_situacao_especial', models.CharField(blank=True, max_length=255)),
                ('capital_social', models.DecimalField(blank=True, decimal_places=0, max_digits=20, null=True, verbose_name='capital social R$')),
                ('efr', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Condicao_Pagamento_Gerador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condicao_pagamento', models.CharField(max_length=100, verbose_name='Condição de Pagamento')),
            ],
            options={
                'verbose_name': 'Condição de Pagamento Gerador',
                'verbose_name_plural': 'Condições de Pagamento Gerador',
            },
        ),
        migrations.CreateModel(
            name='Controlador_gerador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('controlador', models.CharField(max_length=100, verbose_name='Controlador')),
            ],
            options={
                'verbose_name': 'Controlador Gerador',
                'verbose_name_plural': 'Controladores Gerador',
            },
        ),
        migrations.CreateModel(
            name='Desconto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100, verbose_name='Descrição')),
                ('desconto', models.DecimalField(decimal_places=0, max_digits=3)),
            ],
        ),
        migrations.CreateModel(
            name='Franquia_Gerador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Franquia', models.CharField(max_length=100, verbose_name='Franquia')),
            ],
            options={
                'verbose_name': 'Franquia Gerador',
                'verbose_name_plural': 'Franquia Gerador',
            },
        ),
        migrations.CreateModel(
            name='Garantia_Gerador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('garantia', models.CharField(max_length=100, verbose_name='Garantia')),
            ],
            options={
                'verbose_name': 'Garantia Gerador',
                'verbose_name_plural': 'Garantias Gerador',
            },
        ),
        migrations.CreateModel(
            name='Locacao_Gerador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Locação', models.CharField(max_length=100, verbose_name='Prazo da Locação')),
            ],
            options={
                'verbose_name': 'Locação Gerador',
                'verbose_name_plural': 'Locação Gerador',
            },
        ),
        migrations.CreateModel(
            name='Motor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Modelo_Gerador', models.CharField(max_length=100, verbose_name='Grupo_Gerador')),
                ('codigo_produto', models.CharField(blank=True, default='', max_length=9, null=True, verbose_name='Código do produto')),
                ('Fabricante_Motor', models.CharField(max_length=100, verbose_name='Fabricante motor')),
                ('Modelo_Motor', models.CharField(max_length=100, verbose_name='Modelo Motor')),
                ('imagem', models.ImageField(default='/produtos/geradorr.png', upload_to='produtos')),
                ('Içamento', models.CharField(choices=[('Único', 'Único'), ('Duplo', 'Duplo')], default='Único', max_length=100, verbose_name='Içamento')),
                ('Tanque_de_combustivel', models.CharField(max_length=100, verbose_name='Tanque de combustivel')),
                ('Dimensoes', models.CharField(blank=True, max_length=100, verbose_name='Dimensões')),
                ('Peso', models.CharField(blank=True, max_length=100, verbose_name='Peso')),
                ('Silenciador_Gerador', models.CharField(blank=True, choices=[('Silencioso Hospitalar', 'Silencioso Hospitalar'), ('Silencioso Industrial', 'Silencioso Industrial')], default='Silencioso Hospitalar', max_length=200)),
                ('valor_transf_seca_manual_220V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_seca_manual_220_127V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_seca_manual_380_220V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_seca_manual_480_277V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_seca_manual_440_254V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_seca_manual_440_220V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_seca_com_qta_220V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_seca_com_qta_220_127V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_seca_com_qta_380_220V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_seca_com_qta_480_277V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_seca_com_qta_440_254V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_seca_com_qta_440_220V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_rampa_manual_220V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_rampa_manual_220_127V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_rampa_manual_380_220V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_rampa_manual_480_277V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_rampa_manual_440_254V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_rampa_manual_440_220V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_rampa_com_qta_220V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_rampa_com_qta_220_127V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_rampa_com_qta_380_220V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_rampa_com_qta_480_277V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_rampa_com_qta_440_254V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
                ('valor_transf_rampa_com_qta_440_220V', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15)),
            ],
            options={
                'verbose_name': 'Especificações Gerador',
                'verbose_name_plural': 'Especificações Gerador',
                'ordering': ['-Modelo_Gerador'],
            },
        ),
        migrations.CreateModel(
            name='Nivel_Ruido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nivel_ruido', models.CharField(max_length=100, verbose_name='Nivel Ruido Gerador')),
            ],
            options={
                'verbose_name': 'Nivel Ruido Gerador',
                'verbose_name_plural': 'Nivel Ruido Gerador',
            },
        ),
        migrations.CreateModel(
            name='Operacao_Gerador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Operação', models.CharField(max_length=100, verbose_name='Operação')),
            ],
            options={
                'verbose_name': 'Operação Gerador',
                'verbose_name_plural': 'Operação Gerador',
            },
        ),
        migrations.CreateModel(
            name='Prazo_Entrega',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prazo_entrega', models.CharField(max_length=100, verbose_name='Prazo de Entrega')),
            ],
            options={
                'verbose_name': 'Prazo de Entrega',
                'verbose_name_plural': 'Prazos de Entrega',
            },
        ),
        migrations.CreateModel(
            name='Qta_Gerador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Qta_gerador', models.CharField(max_length=100, verbose_name='QTA Gerador')),
            ],
            options={
                'verbose_name': 'QTA Gerador',
                'verbose_name_plural': 'QTA Gerador',
            },
        ),
        migrations.CreateModel(
            name='Tensao_Gerador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tensao_gerador', models.CharField(max_length=100, verbose_name='Tensão Gerador')),
            ],
            options={
                'verbose_name': 'Tensão Gerador',
                'verbose_name_plural': 'Tensão Gerador',
            },
        ),
        migrations.CreateModel(
            name='Validade_Proposta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('validade_proposta', models.CharField(max_length=100, verbose_name='Validade da proposta')),
            ],
            options={
                'verbose_name': 'Validade Proposta',
                'verbose_name_plural': 'Validades Proposta',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefone', models.CharField(max_length=20, null=True)),
                ('Cargo', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
