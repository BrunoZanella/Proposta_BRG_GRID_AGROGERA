# -*- Mode: Python; coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum,Avg
from localflavor.br.br_states import STATE_CHOICES
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20, null=True)
    Cargo = models.CharField(max_length=100)
     
    def telefone_formatado(self):
        telefone = self.telefone
        return "(%s) %s-%s" % (telefone[0:2], telefone[2:7], telefone[7:11])
    telefone_formatado.short_description = 'Telefone Formatado'
	
def validate_cpf(cpf):
    if cpf == '' or cpf == 0:
        return cpf
    if not cpf.isdigit():
        raise ValidationError('CPF deve conter apenas números.')
    if len(cpf) != 11:
        raise ValidationError('CPF deve conter 11 números.')

def validate_cnpj(cnpj):
    if not cnpj.isdigit():
        raise ValidationError(' Deve conter apenas números.')
     
class Cliente(models.Model):
	nome = models.CharField(u'Nome', max_length=100, unique=True, blank=True)
	nome_pessoa_proposta = models.CharField(u'Aos cuidados de:', max_length=100, blank=True)
	cnpj = models.CharField(u'CNPJ/CPF', blank=True, max_length=18, validators=[validate_cnpj], unique=True)
	nome = models.CharField(max_length=255, blank=True)
	fantasia = models.CharField(max_length=255, blank=True)
	telefone = models.CharField(u'telefone', blank=True, max_length=50)
	email = models.EmailField(u'email', blank=True, max_length=200)
	CEP = models.CharField(u'CEP', blank=True, max_length=200)
	bairro = models.CharField(u'Bairro', blank=True, max_length=100)
	cidade = models.CharField(u'Cidade', blank=True, max_length=100)
	estado = models.CharField(u'Estado',max_length=2, null=True, blank=True)
	logradouro = models.CharField(max_length=255, blank=True)
	numero = models.CharField(max_length=255, blank=True)
	complemento = models.CharField(max_length=255, blank=True)
	abertura = models.CharField(max_length=255, blank=True)
	natureza_juridica = models.CharField(max_length=255, blank=True)
	atividade_principal = models.TextField(max_length=1000, blank=True)
	atividades_secundarias = models.TextField(max_length=4000, blank=True)
	qsa = models.TextField(max_length=1000, blank=True)
	situacao = models.CharField(max_length=255, blank=True)
	data_situacao = models.CharField(max_length=255, blank=True)
	motivo_situacao = models.CharField(max_length=255, blank=True)
	situacao_especial = models.CharField(max_length=255, blank=True)
	data_situacao_especial = models.CharField(max_length=255, blank=True)
	capital_social = models.DecimalField(u'capital social R$',max_digits=20, decimal_places=0, blank=True, null=True)
	efr = models.CharField(max_length=255, blank=True)
 
	def cnpj_formatado(self):
		cnpj = self.cnpj
		return "%s.%s.%s/%s-%s" % (cnpj[0:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:14])
	cnpj_formatado.short_description = 'CNPJ Formatado'

	def cnpj_formatado_sem_tracos(self):
		cnpj = self.cnpj
		return cnpj.replace(".", "").replace("/", "").replace("-", "")
	cnpj_formatado_sem_tracos.short_description = 'CNPJ Formatado sem traco'
    
	def cpf_formatado(self):
		cpf = self.cnpj
		return "%s.%s.%s-%s" % (cpf[0:3], cpf[3:6], cpf[6:9], cpf[9:11])
	cpf_formatado.short_description = 'CPF Formatado'

	def telefone_formatado_cliente(self):
		telefone = self.telefone
		return "(%s) %s-%s" % (telefone[0:2], telefone[2:7], telefone[7:11])
	telefone_formatado_cliente.short_description = 'Telefone Formatado'


	def __str__(self):
		return self.nome


class Desconto(models.Model):
    
    descricao = models.CharField(u'Descrição', max_length=100)
    desconto = models.DecimalField(max_digits=3, decimal_places=0)
    
    def __str__(self):
        return self.descricao


class Motor(models.Model):

#	Modelo_Gerador = models.ForeignKey(Grupo_Gerador, on_delete=models.CASCADE)
	Modelo_Gerador = models.CharField('Grupo Gerador', max_length=100)
	codigo_produto = models.CharField('Código do produto', max_length=9, blank=True, null=True, default='')
	Fabricante_Motor = models.CharField(u'Fabricante motor', max_length=100)
	Modelo_Motor = models.CharField(u'Modelo Motor', max_length=100)
	imagem = models.ImageField(upload_to='produtos', default= '/produtos/geradorr.png')
	ICAMENTO_CHOICES = (
		('Único','Único'),
		('Duplo','Duplo'),
		)
	Içamento = models.CharField(u'Içamento', max_length=100 , choices = ICAMENTO_CHOICES, default='Único')
	Tanque_de_combustivel = models.CharField(u'Tanque de combustivel', max_length=100)
	Dimensoes = models.CharField(u'Dimensões',blank=True, max_length=100)
	Peso = models.CharField(u'Peso',blank=True, max_length=100)
	Silenciador_CHOICES = (
		('Silencioso Hospitalar','Silencioso Hospitalar'),
		('Silencioso Industrial','Silencioso Industrial'),
		)
	Silenciador_Gerador = models.CharField(blank=True, max_length=200, choices = Silenciador_CHOICES, default='Silencioso Hospitalar')

	valor_transf_seca_manual_220V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00) 
	valor_transf_seca_manual_220_127V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
	valor_transf_seca_manual_380_220V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
	valor_transf_seca_manual_480_277V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
	valor_transf_seca_manual_440_254V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
	valor_transf_seca_manual_440_220V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
 
	valor_transf_seca_com_qta_220V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
	valor_transf_seca_com_qta_220_127V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
	valor_transf_seca_com_qta_380_220V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
	valor_transf_seca_com_qta_480_277V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
	valor_transf_seca_com_qta_440_254V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
	valor_transf_seca_com_qta_440_220V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
 
	valor_transf_rampa_manual_220V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
	valor_transf_rampa_manual_220_127V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
	valor_transf_rampa_manual_380_220V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
	valor_transf_rampa_manual_480_277V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
	valor_transf_rampa_manual_440_254V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
	valor_transf_rampa_manual_440_220V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
 
	valor_transf_rampa_com_qta_220V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
	valor_transf_rampa_com_qta_220_127V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
	valor_transf_rampa_com_qta_380_220V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
	valor_transf_rampa_com_qta_480_277V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
	valor_transf_rampa_com_qta_440_254V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00)
	valor_transf_rampa_com_qta_440_220V = models.DecimalField(max_digits=15,blank=True, decimal_places=2, default=0.00) 
 
	def get_valor_transf(self, tensao, qta, valor_gerador):
     
		if valor_gerador:
			return valor_gerador
    
		if tensao == '220V' and qta == 'Transferência em rampa manual':
			return self.valor_transf_rampa_manual_220V
		elif tensao == '220V' and qta == 'Transferência em rampa com QTA':
			return self.valor_transf_rampa_com_qta_220V	
		elif tensao == '220V' and qta == 'Transferência seca manual':
			return self.valor_transf_seca_manual_220V 
		elif tensao == '220V' and qta == 'Transferência seca com QTA':
			return self.valor_transf_seca_com_qta_220V 

		if tensao == '220/127V' and qta == 'Transferência em rampa manual':
			return self.valor_transf_rampa_manual_220_127V
		elif tensao == '220/127V' and qta == 'Transferência em rampa com QTA':
			return self.valor_transf_rampa_com_qta_220_127V	
		elif tensao == '220/127V' and qta == 'Transferência seca manual':
			return self.valor_transf_seca_manual_220_127V 
		elif tensao == '220/127V' and qta == 'Transferência seca com QTA':
			return self.valor_transf_seca_com_qta_220_127V

		if tensao == '380/220V' and qta == 'Transferência em rampa manual':
			return self.valor_transf_rampa_manual_380_220V
		elif tensao == '380/220V' and qta == 'Transferência em rampa com QTA':
			return self.valor_transf_rampa_com_qta_380_220V	
		elif tensao == '380/220V' and qta == 'Transferência seca manual':
			return self.valor_transf_seca_manual_380_220V 
		elif tensao == '380/220V' and qta == 'Transferência seca com QTA':
			return self.valor_transf_seca_com_qta_380_220V

		if tensao == '480/277V' and qta == 'Transferência em rampa manual':
			return self.valor_transf_rampa_manual_480_277V
		elif tensao == '480/277V' and qta == 'Transferência em rampa com QTA':
			return self.valor_transf_rampa_com_qta_480_277V
		elif tensao == '480/277V' and qta == 'Transferência seca manual':
			return self.valor_transf_seca_manual_480_277V
		elif tensao == '480/277V' and qta == 'Transferência seca com QTA':
			return self.valor_transf_seca_com_qta_480_277V

		if tensao == '440/254V' and qta == 'Transferência em rampa manual':
			return self.valor_transf_rampa_manual_440_254V
		elif tensao == '440/254V' and qta == 'Transferência em rampa com QTA':
			return self.valor_transf_rampa_com_qta_440_254V
		elif tensao == '440/254V' and qta == 'Transferência seca manual':
			return self.valor_transf_seca_manual_440_254V
		elif tensao == '440/254V' and qta == 'Transferência seca com QTA':
			return self.valor_transf_seca_com_qta_440_254V

		if tensao == '440/220V - Monofásico' and qta == 'Transferência em rampa manual':
			return self.valor_transf_rampa_manual_440_220V
		elif tensao == '440/220V - Monofásico' and qta == 'Transferência em rampa com QTA':
			return self.valor_transf_rampa_com_qta_440_220V
		elif tensao == '440/220V - Monofásico' and qta == 'Transferência seca manual':
			return self.valor_transf_seca_manual_440_220V
		elif tensao == '440/220V - Monofásico' and qta == 'Transferência seca com QTA':
			return self.valor_transf_seca_com_qta_440_220V

		else:
			return None
 
	class Meta:
		ordering = ['Modelo_Gerador']
		verbose_name = u'Especificações Gerador'
		verbose_name_plural = u'Especificações Gerador'

	def __str__(self):
	    return self.Modelo_Gerador


class Qta_Gerador(models.Model):
    
    Qta_gerador = models.CharField(u'QTA Gerador', max_length=100)
    
    class Meta:
        verbose_name = u'QTA Gerador'
        verbose_name_plural = u'QTA Gerador'
  
    def __str__(self):
        return self.Qta_gerador
    
class Tensao_Gerador(models.Model):
    
    Tensao_gerador = models.CharField(u'Tensão Gerador', max_length=100)
    
    class Meta:
        verbose_name = u'Tensão Gerador'
        verbose_name_plural = u'Tensão Gerador'
  
    def __str__(self):
        return self.Tensao_gerador

class Controlador_gerador(models.Model):
    
    controlador = models.CharField(u'Controlador', max_length=100)
    
    class Meta:
        verbose_name = u'Controlador Gerador'
        verbose_name_plural = u'Controladores Gerador'
  
    def __str__(self):
        return self.controlador
    
class Nivel_Ruido(models.Model):
    
    Nivel_ruido = models.CharField(u'Nivel Ruido Gerador', max_length=100)
    
    class Meta:
        verbose_name = u'Nivel Ruido Gerador'
        verbose_name_plural = u'Nivel Ruido Gerador'
  
    def __str__(self):
        return self.Nivel_ruido


class Acessorio(models.Model):

	codigo_acessorio = models.CharField(u'Código',max_length=9, unique=True, blank=True)
	descricao = models.CharField(u'Nome',max_length=100, blank=True, null=True)
	imagem = models.ImageField(blank=True,upload_to='produtos/Acessorio_proposta')

	class Meta:
		verbose_name = u'Acessórios'
		verbose_name_plural = u'Acessório'
  
	def __str__(self):
		return self.codigo_acessorio  + ' - ' + self.descricao


class Condicao_Pagamento_Gerador(models.Model):
    
    condicao_pagamento = models.CharField(u'Condição de Pagamento', max_length=100)
    
    class Meta:
        verbose_name = u'Condição de Pagamento Gerador'
        verbose_name_plural = u'Condições de Pagamento Gerador'
    
    def __str__(self):
        return self.condicao_pagamento      
        
class Validade_Proposta(models.Model):
    
    validade_proposta = models.CharField(u'Validade da proposta', max_length=100)
    
    class Meta:
        verbose_name = u'Validade Proposta'
        verbose_name_plural = u'Validades Proposta'
  
    def __str__(self):
        return self.validade_proposta 
   
class Prazo_Entrega(models.Model):
    
    prazo_entrega = models.CharField(u'Prazo de Entrega', max_length=100)
    
    class Meta:
        verbose_name = u'Prazo de Entrega'
        verbose_name_plural = u'Prazos de Entrega'
  
    def __str__(self):
        return self.prazo_entrega 
             
class Garantia_Gerador(models.Model):
    
    garantia = models.CharField(u'Garantia', max_length=100)
    
    class Meta:
        verbose_name = u'Garantia Gerador'
        verbose_name_plural = u'Garantias Gerador'
  
    def __str__(self):
        return self.garantia

    
class Operacao_Gerador(models.Model):
    
    Operação = models.CharField(u'Operação', max_length=100)
    
    class Meta:
        verbose_name = u'Operação Gerador'
        verbose_name_plural = u'Operação Gerador'
  
    def __str__(self):
        return self.Operação
    
class Franquia_Gerador(models.Model):
    
    Franquia = models.CharField(u'Franquia', max_length=100)
    
    class Meta:
        verbose_name = u'Franquia Gerador'
        verbose_name_plural = u'Franquia Gerador'
  
    def __str__(self):
        return self.Franquia           

class Locacao_Gerador(models.Model):
    
    Locação = models.CharField(u'Prazo da Locação', max_length=100)
    
    class Meta:
        verbose_name = u'Locação Gerador'
        verbose_name_plural = u'Locação Gerador'
  
    def __str__(self):
        return self.Locação           

