# -*- Mode: Python; coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.db.models import Sum, Avg
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput
from django.db import models
from django import forms
from django.contrib import admin
from .models import Proposta_Brg, Proposta_Agrogera, Proposta_Grid,produto_proposta,Personalizar,Acessorio_propostas
from proposta.core.models import Motor

class PersonalizarInline(admin.StackedInline):
    model = Personalizar
    extra = 0
    max_num = 1
    can_add_related = False
    fields = ['imagem','Observacao']

class Acessorio_propostaInline(admin.StackedInline):
    model = Acessorio_propostas
    extra = 0
    autocomplete_fields = ['acessorio']
    can_add_related = False
    fields = ['acessorio','Observacao','quantidade_acessorio','valor_acessorio']
    search_fields = ['acessorio']

class ProdutoInline(admin.StackedInline):
    model = produto_proposta
    extra = 0
    autocomplete_fields = ['produto']
    fields = ['produto','personalizar_nome','Tensão_Gerador','QTA_Gerador','Controlador_Gerador','quantidade_Gerador','valor_gerador','Desconto',('Nivel_de_ruído','Observacao')]
#    search_fields = ['produto']
      
class ProdutoGridAgrogeraInline(admin.StackedInline):
    model = produto_proposta
    extra = 0
    autocomplete_fields = ['produto']
    fields = ['produto','personalizar_nome','Tensão_Gerador','QTA_Gerador','quantidade_Gerador','valor_gerador','Desconto',('Observacao')]
    search_fields = ['produto__Modelo_Gerador']
   
    
class PropostaBrgAdmin(admin.ModelAdmin):
    inlines = [ProdutoInline, Acessorio_propostaInline, PersonalizarInline]
    list_display = ['cliente', 'Ordem', 'data', 'user', 'imprimir']  # incluir o campo data_proposta_editavel na lista
    search_fields = ['cliente__nome', 'cliente__cnpj']
    list_filter = ['cliente__nome', 'data', 'Ordem']
    fields = ['cliente', 'Ordem', 'revisão',('Condições_de_Pagamento', 'validade', 'Prazo_de_Entrega'),('Frete', 'Valor_Instalação', 'garantia_gerador')]
    autocomplete_fields = ['cliente']
    list_per_page = 30
    save_on_top = True
    collapse_all = True
    
    
class PropostaAgrogeraAdmin(admin.ModelAdmin):
    inlines = [ProdutoGridAgrogeraInline, Acessorio_propostaInline]
    list_display = ['cliente', 'Ordem', 'data', 'user', 'imprimir']  # incluir o campo data_proposta_editavel na lista
    list_filter = ['cliente__nome', 'data', 'Ordem']
    fields = ['cliente', ('Ordem', 'revisão'),('Operação','Franquia','Prazo_da_Locação'),('Condições_de_Pagamento', 'validade', 'Prazo_de_Entrega'),('Frete_ida','Frete_volta'),('Hora_extra','Valor_Instalação')]
    autocomplete_fields = ['cliente']
    
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '26'})},  # Tamanho do campo "Ordem"
        models.CharField: {'widget': TextInput(attrs={'size': '5', 'maxlength': '5'})},   # Tamanho do campo "Revisão"
    }

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'Ordem':
            kwargs['widget'] = TextInput(attrs={'size': '26'})  # Tamanho do campo "Ordem"
        elif db_field.name == 'revisão':
            kwargs['widget'] = TextInput(attrs={'size': '5', 'maxlength': '5','style': 'margin-left: -100px;'})  # Tamanho do campo "Revisão"
        return super().formfield_for_dbfield(db_field, **kwargs)
        
    list_per_page = 30
    save_on_top = True
    collapse_all = True
    
class PropostaGridAdmin(admin.ModelAdmin):
    inlines = [ProdutoGridAgrogeraInline, Acessorio_propostaInline]
    list_display = ['cliente', 'Ordem', 'data', 'user', 'imprimir']  # incluir o campo data_proposta_editavel na lista
    list_filter = ['cliente__nome', 'data', 'Ordem']
    fields = ['cliente', ('Ordem', 'revisão'),('Operação','Franquia','Prazo_da_Locação'),('Condições_de_Pagamento', 'validade', 'Prazo_de_Entrega'),('Frete_ida','Frete_volta'),('Hora_extra','Valor_Instalação')]
    autocomplete_fields = ['cliente']
    
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '26'})},  # Tamanho do campo "Ordem"
        models.CharField: {'widget': TextInput(attrs={'size': '5', 'maxlength': '5'})},   # Tamanho do campo "Revisão"
    }

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'Ordem':
            kwargs['widget'] = TextInput(attrs={'size': '26'})  # Tamanho do campo "Ordem"
        elif db_field.name == 'revisão':
            kwargs['widget'] = TextInput(attrs={'size': '5', 'maxlength': '5','style': 'margin-left: -100px;'})  # Tamanho do campo "Revisão"
        return super().formfield_for_dbfield(db_field, **kwargs)
        
    list_per_page = 30
    save_on_top = True
    collapse_all = True

class produto_propostaAdmin(admin.ModelAdmin):
    pass

#admin.site.register(produto_proposta, produto_propostaAdmin)

admin.site.register(Proposta_Brg, PropostaBrgAdmin)
admin.site.register(Proposta_Grid, PropostaGridAdmin)
admin.site.register(Proposta_Agrogera, PropostaAgrogeraAdmin)