# -*- Mode: Python; coding: utf-8 -*-
from django import forms
from django.contrib import admin
from .models import Cliente, Motor, Desconto, UserProfile, Acessorio,Condicao_Pagamento_Gerador,Validade_Proposta,Prazo_Entrega,Garantia_Gerador,Tensao_Gerador,Qta_Gerador,Nivel_Ruido,Controlador_gerador,Locacao_Gerador,Franquia_Gerador,Operacao_Gerador
from django.contrib.admin.views.main import ChangeList
from django.db.models import Sum, Avg
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil'

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

class ClienteAdmin(admin.ModelAdmin):
	list_display = ['nome', 'cnpj', 'telefone']
	search_fields = ['nome','cnpj']
	list_filter = ['nome', 'cnpj']

class MotorAdmin(admin.ModelAdmin):
    search_fields = ['Modelo_Gerador','codigo_produto']
    list_display = ['Modelo_Gerador','codigo_produto', 'Fabricante_Motor',  'Modelo_Motor', 'Tanque_de_combustivel', 'Dimensoes', 'Peso']

class AcessorioInline(admin.StackedInline):
    model = Acessorio
    extra = 0
    can_add_related = False
    fields = ['codigo_acessorio','descricao','Observacao','quantidade_acessorio','valor_acessorio']

class ProdutoAdmin(admin.ModelAdmin):
	pass
class PersonalizarAdmin(admin.ModelAdmin):
	pass
class DescontoAdmin(admin.ModelAdmin):
    pass
class Grupo_GeradorAdmin(admin.ModelAdmin):
    pass
class Acessorio_propostaAdmin(admin.ModelAdmin):
    pass
class AcessorioAdmin(admin.ModelAdmin):
    search_fields = ['descricao']
    pass
class Condicao_Pagamento_GeradorAdmin(admin.ModelAdmin):
    pass
class Validade_PropostaAdmin(admin.ModelAdmin):
    pass
class Prazo_EntregaAdmin(admin.ModelAdmin):
    pass
class Garantia_GeradorAdmin(admin.ModelAdmin):
    pass
class Qta_GeradorAdmin(admin.ModelAdmin):
    pass
class Tensao_GeradorAdmin(admin.ModelAdmin):
    pass
class Nivel_RuidoAdmin(admin.ModelAdmin):
    pass
class Controlador_geradorAdmin(admin.ModelAdmin):
    pass
class Operacao_GeradorAdmin(admin.ModelAdmin):
	pass
class Franquia_GeradorAdmin(admin.ModelAdmin):
	pass
class Locacao_GeradorAdmin(admin.ModelAdmin):
	pass

admin.site.register(Motor, MotorAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Desconto, DescontoAdmin)
admin.site.register(Acessorio, AcessorioAdmin)
admin.site.register(Condicao_Pagamento_Gerador, Condicao_Pagamento_GeradorAdmin)
admin.site.register(Validade_Proposta, Validade_PropostaAdmin)
admin.site.register(Prazo_Entrega, Prazo_EntregaAdmin)
admin.site.register(Garantia_Gerador, Garantia_GeradorAdmin)
admin.site.register(Qta_Gerador, Qta_GeradorAdmin)
admin.site.register(Tensao_Gerador, Tensao_GeradorAdmin)
admin.site.register(Nivel_Ruido, Nivel_RuidoAdmin)
admin.site.register(Controlador_gerador, Controlador_geradorAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Franquia_Gerador, Franquia_GeradorAdmin)
admin.site.register(Operacao_Gerador, Operacao_GeradorAdmin)
admin.site.register(Locacao_Gerador, Locacao_GeradorAdmin)