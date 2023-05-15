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
from proposta.core.models import Cliente,Motor, Condicao_Pagamento_Gerador,Validade_Proposta,Prazo_Entrega,Garantia_Gerador,Operacao_Gerador,Franquia_Gerador,Locacao_Gerador, Desconto, UserProfile, Acessorio,Tensao_Gerador,Qta_Gerador,Nivel_Ruido,Controlador_gerador


class produto_proposta(models.Model):
	proposta_Brg = models.ForeignKey("Proposta_Brg",  on_delete=models.CASCADE, null=True, related_name='propostas_brg')
	proposta_Grid = models.ForeignKey("Proposta_Grid", on_delete=models.CASCADE, null=True, related_name='propostas_grid')
	proposta_Agrogera = models.ForeignKey("Proposta_Agrogera", on_delete=models.CASCADE, null=True, related_name='propostas_agrogera')
	produto = models.ForeignKey(Motor, on_delete=models.CASCADE)
	personalizar_nome = models.CharField(u'Adicionar descrição', blank=True, max_length=100)
	Tensão_Gerador = models.ForeignKey(Tensao_Gerador, on_delete=models.CASCADE)
	QTA_Gerador = models.ForeignKey(Qta_Gerador, on_delete=models.CASCADE)
	Controlador_Gerador = models.ForeignKey(Controlador_gerador, on_delete=models.CASCADE, null=True)
	Nivel_de_ruído = models.ForeignKey(Nivel_Ruido, on_delete=models.CASCADE, null=True)
	quantidade_Gerador = models.DecimalField(blank=True, max_digits=15, decimal_places=0,default='1')
	valor_gerador = models.DecimalField(max_digits=15, blank=True, null=True, decimal_places=2, default= '0')
	Desconto = models.ForeignKey(Desconto, on_delete=models.CASCADE,default='0%')
	Observacao = models.CharField(u'Observação',max_length=100, blank=True, null=True)

	@property
	def valor_transf(self):
     
		return self.produto.get_valor_transf(self.Tensão_Gerador.Tensao_gerador,self.QTA_Gerador.Qta_gerador,self.valor_gerador)

	def soma_gerador(self):
		desconto= self.Desconto.desconto/100
		if self.valor_transf:
			return (self.valor_transf*self.quantidade_Gerador * (1-desconto))
		if self.valor_gerador is not None:
			return (self.valor_gerador*self.quantidade_Gerador * (1-desconto))
	soma_gerador.description = 'Total_Gerador'
 
	def soma_quantidade_gerador(self):
		if self.valor_transf:
			return (self.valor_transf)
		if self.valor_gerador is not None:
			return (self.valor_gerador)
	soma_quantidade_gerador.description = 'soma_quantidade_gerador'

	class Meta:
	#	ordering = ['-produto__Modelo_Gerador']  # Ordena por nome do gerador em ordem decrescente
		ordering = ['-produto']
		verbose_name = u'Produto'
		verbose_name_plural = u'Produtos'
  
	def __str__(self):
		if self.proposta_Brg:
			return f"BRG - {self.proposta_Brg.cliente.nome} - {self.produto.Modelo_Gerador}"
		elif self.proposta_Grid:
			return f"Grid - {self.proposta_Grid.cliente.nome} - {self.produto.Modelo_Gerador}"
		elif self.proposta_Agrogera:
			return f"AgroGera - {self.proposta_Agrogera.cliente.nome} - {self.produto.Modelo_Gerador}"
		else:
			return "Produto sem proposta associada"


class Acessorio_propostas(models.Model):
	proposta_Brg = models.ForeignKey("Proposta_Brg",  on_delete=models.CASCADE, null=True, related_name='acessorio_propostas_brg')
	proposta_Grid = models.ForeignKey("Proposta_Grid", on_delete=models.CASCADE, null=True, related_name='acessorio_propostas_grid')
	proposta_Agrogera = models.ForeignKey("Proposta_Agrogera", on_delete=models.CASCADE, null=True, related_name='acessorio_propostas_agrogera')
	acessorio = models.ForeignKey(Acessorio, on_delete=models.CASCADE)
	Observacao = models.CharField(u'Observação',max_length=100, blank=True, null=True)
	quantidade_acessorio = models.DecimalField(u'Quantidade Acessório',blank=True, max_digits=15, decimal_places=0,default='1')
	valor_acessorio = models.DecimalField(u'Valor Acessório',max_digits=15, blank=True, null=True, decimal_places=2, default= '0')
 
	def soma_quantidade_acessorio(self):
		return (self.valor_acessorio*self.quantidade_acessorio)
	soma_quantidade_acessorio.description = 'soma_quantidade_acessorio'

	class Meta:
		verbose_name = u'Acessórios Proposta'
		verbose_name_plural = u'Acessório Proposta'
  
	def __str__(self):
		if self.proposta_Brg:
			return f"BRG - {self.proposta_Brg.cliente.nome} - {self.proposta_Brg.Ordem}"
		elif self.proposta_Grid:
			return f"Grid - {self.proposta_Grid.cliente.nome} - {self.proposta_Grid.Ordem}"
		elif self.proposta_Agrogera:
			return f"AgroGera - {self.proposta_Agrogera.cliente.nome} - {self.proposta_Agrogera.Ordem}"
		else:
			return "Acessórios sem proposta associada"

	
class Personalizar(models.Model):

	proposta_Brg = models.ForeignKey("Proposta_Brg",  on_delete=models.CASCADE, null=True, related_name='personalizar_propostas_brg')
	proposta_Grid = models.ForeignKey("Proposta_Grid", on_delete=models.CASCADE, null=True, related_name='personalizar_propostas_grid')
	proposta_Agrogera = models.ForeignKey("Proposta_Agrogera", on_delete=models.CASCADE, null=True, related_name='personalizar_propostas_agrogera')
	imagem = models.ImageField(blank=True,upload_to='produtos/personalizar')
	Observacao = models.CharField(u'Observação',max_length=100, blank=True, null=True)

	class Meta:
		verbose_name = u'Personalizações'
		verbose_name_plural = u'Personalizações'
  
	def __str__(self):
		if self.proposta_Brg:
			return f"BRG - {self.proposta_Brg.cliente.nome} - {self.proposta_Brg.Ordem}"
		elif self.proposta_Grid:
			return f"Grid - {self.proposta_Grid.cliente.nome} - {self.proposta_Grid.Ordem}"
		elif self.proposta_Agrogera:
			return f"AgroGera - {self.proposta_Agrogera.cliente.nome} - {self.proposta_Agrogera.Ordem}"
		else:
			return "Personalizações sem proposta associada"


def nova_ordem():
    latest_proposta = Proposta_Brg.objects.order_by('-Ordem').first()
    if latest_proposta is None:
        return '1'
    else:
        latest_ordem = latest_proposta.Ordem[0:]
        new_ordem_int = int(latest_ordem) + 1
        new_ordem_str = str(new_ordem_int)
        return new_ordem_str   
    
class Proposta_Brg(models.Model):
    
	cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='proposta_brg')
	Ordem = models.CharField(u'Número da proposta',max_length=200, unique=True, default=nova_ordem)
	revisão = models.CharField(u'Revisão',max_length=5, default='001')
	data = models.DateTimeField(auto_now_add=True ) # hora que fez a proposta
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='proposta_brg', unique=False)

	garantia_gerador = models.ForeignKey(Garantia_Gerador, on_delete=models.CASCADE)
	Condições_de_Pagamento = models.ForeignKey(Condicao_Pagamento_Gerador, on_delete=models.CASCADE, default='1x sem juros', related_name='proposta_brg')
	validade = models.ForeignKey(Validade_Proposta, on_delete=models.CASCADE, default= 'Sete', related_name='proposta_brg')
	Prazo_de_Entrega = models.ForeignKey(Prazo_Entrega, on_delete=models.CASCADE, default='Sete', related_name='proposta_brg')

	Frete = models.DecimalField(blank=True, max_digits=15, decimal_places=2, default=0.00)

	Valor_Instalação = models.DecimalField(blank=True, max_digits=15, decimal_places=2, default=0.00)

	def imprimir(self):
		return mark_safe("""<a href=\"/proposta_Brg/%s/\" target="_blank"><img src=\"/static/images/b_print.png\"></a>""" % self.id)
        
	def save(self, *args, **kwargs):
		if self.pk:
			original = Proposta_Brg.objects.get(pk=self.pk)
			if original.revisão != self.revisão:
				self.data = timezone.now().date()
		super().save(*args, **kwargs)
          
	class Meta:
		ordering = ['-data']
		verbose_name = 'Proposta BRG'
		verbose_name_plural = 'Propostas BRG'

	def __str__(self):
		return 'BRG ' + self.cliente.nome + ' - Proposta nº ' + self.Ordem


def nova_ordem2():
    latest_proposta = Proposta_Grid.objects.order_by('-Ordem').first()
    if latest_proposta is None:
        return '1'
    else:
        latest_ordem = latest_proposta.Ordem
        new_ordem_int = int(latest_ordem) + 1
        new_ordem_str = str(new_ordem_int)
        return new_ordem_str


class Proposta_Grid(models.Model):
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='propostas_grid')
    Ordem = models.CharField(u'Número da proposta',max_length=20, unique=True, default=nova_ordem2)
    revisão = models.CharField(u'Revisão',max_length=5, default='001')
    data = models.DateTimeField(auto_now_add=True ) # hora que fez a proposta
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='propostas_grid', unique=False)
    Operação = models.ForeignKey(Operacao_Gerador, on_delete=models.CASCADE, related_name='propostas_grid')
    Hora_extra = models.DecimalField(u'Horas extras',blank=True, max_digits=15, decimal_places=2, default=0.00)
    Franquia = models.ForeignKey(Franquia_Gerador, on_delete=models.CASCADE, related_name='propostas_grid')
    Prazo_da_Locação = models.ForeignKey(Locacao_Gerador, on_delete=models.CASCADE, related_name='propostas_grid')

    garantia_gerador = models.ForeignKey(Garantia_Gerador, on_delete=models.CASCADE, related_name='propostas_grid', null=True)

    Condições_de_Pagamento = models.ForeignKey(Condicao_Pagamento_Gerador, on_delete=models.CASCADE, default='1x sem juros', related_name='propostas_grid')

    validade = models.ForeignKey(Validade_Proposta, on_delete=models.CASCADE, default= 'Sete', related_name='propostas_grid')

    Prazo_de_Entrega = models.ForeignKey(Prazo_Entrega, on_delete=models.CASCADE, default='Sete', related_name='propostas_grid')

    Frete_ida = models.DecimalField(blank=True, max_digits=15, decimal_places=2, default=0.00)
    Frete_volta = models.DecimalField(blank=True, max_digits=15, decimal_places=2, default=0.00)
 
    Valor_Instalação = models.DecimalField(blank=True, max_digits=15, decimal_places=2, default=0.00)

    def imprimir(self):
        return mark_safe("""<a href=\"/proposta_Grid/%s/\" target="_blank"><img src=\"/static/images/b_print.png\"></a>""" % self.id)

    def save(self, *args, **kwargs):
        if self.pk:
            original = Proposta_Grid.objects.get(pk=self.pk)
            if original.revisão != self.revisão:
                self.data = timezone.now().date()
        super().save(*args, **kwargs)
          
    class Meta:
        ordering = ['-data']
        verbose_name = 'Proposta Grid'
        verbose_name_plural = 'Propostas Grid'

    def __str__(self):
        return 'Grid ' + self.cliente.nome + ' - Proposta nº ' + self.Ordem


def nova_ordem3():
    latest_proposta = Proposta_Agrogera.objects.order_by('-Ordem').first()
    if latest_proposta is None:
        return '1'
    else:
        latest_ordem = latest_proposta.Ordem
        new_ordem_int = int(latest_ordem) + 1
        new_ordem_str = str(new_ordem_int)
        return new_ordem_str


class Proposta_Agrogera(models.Model):
    
	cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='propostas_agrogera')
	Ordem = models.CharField(u'Número da proposta',max_length=20, unique=True, default=nova_ordem3)
	revisão = models.CharField(u'Revisão',max_length=5, default='001')
	data = models.DateTimeField(auto_now_add=True ) # hora que fez a proposta
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='propostas_agrogera', unique=False)
	Operação = models.ForeignKey(Operacao_Gerador, on_delete=models.CASCADE, related_name='propostas_agrogera')
	Hora_extra = models.DecimalField(u'Horas extras',blank=True, max_digits=15, decimal_places=2, default=0.00)
	Franquia = models.ForeignKey(Franquia_Gerador, on_delete=models.CASCADE, related_name='propostas_agrogera')
	Prazo_da_Locação = models.ForeignKey(Locacao_Gerador, on_delete=models.CASCADE, related_name='propostas_agrogera')

	garantia_gerador = models.ForeignKey(Garantia_Gerador, on_delete=models.CASCADE, related_name='propostas_agrogera', null=True)

	Condições_de_Pagamento = models.ForeignKey(Condicao_Pagamento_Gerador, on_delete=models.CASCADE, default='1x sem juros', related_name='propostas_agrogera')

	validade = models.ForeignKey(Validade_Proposta, on_delete=models.CASCADE, default= 'Sete', related_name='propostas_agrogera')

	Prazo_de_Entrega = models.ForeignKey(Prazo_Entrega, on_delete=models.CASCADE, default='Sete', related_name='propostas_agrogera')

	Frete_ida = models.DecimalField(blank=True, max_digits=15, decimal_places=2, default=0.00)
	Frete_volta = models.DecimalField(blank=True, max_digits=15, decimal_places=2, default=0.00)

	Valor_Instalação = models.DecimalField(blank=True, max_digits=15, decimal_places=2, default=0.00)

	def imprimir(self):
		return mark_safe("""<a href=\"/proposta_Agrogera/%s/\" target="_blank"><img src=\"/static/images/b_print.png\"></a>""" % self.id)

	def save(self, *args, **kwargs):
		if self.pk:
			original = Proposta_Agrogera.objects.get(pk=self.pk)
			if original.revisão != self.revisão:
				self.data = timezone.now().date()
		super().save(*args, **kwargs)
          
	class Meta:
		ordering = ['-data']
		verbose_name = 'Proposta AgroGera'
		verbose_name_plural = 'Propostas AgroGera'

	def __str__(self):
		return 'AgroGera ' + self.cliente.nome + ' - Proposta nº ' + self.Ordem

