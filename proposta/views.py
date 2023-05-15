from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from proposta.core.models import Cliente, Motor, Desconto
from proposta.propostas.models import Proposta_Brg,Proposta_Grid,Proposta_Agrogera,produto_proposta,Personalizar,Acessorio_propostas
import io
import requests
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Cliente)
def atualizar_dados_cliente(sender, instance, **kwargs):

    dados_cnpj = 0
    cpf = 0
    cnpj = instance.cnpj
    cpf = instance.cnpj

    if len(cnpj) == 11:
        cpf += cnpj
        pass

    if len(cnpj) == 14:
        response = requests.get(f'https://www.receitaws.com.br/v1/cnpj/{cnpj}')
        try:
            response.raise_for_status()
            dados_cnpj = response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
        else:
            cliente = Cliente.objects.filter(cnpj=cnpj).first()
            

            if cliente:
                instance.nome = dados_cnpj.get('nome', instance.nome)
                instance.fantasia = dados_cnpj.get('fantasia', instance.fantasia)
                instance.abertura = dados_cnpj.get('abertura', instance.abertura)
                instance.natureza_juridica = dados_cnpj.get('natureza_juridica', instance.natureza_juridica)
                instance.logradouro = dados_cnpj.get('logradouro', instance.logradouro)
                instance.numero = dados_cnpj.get('numero', instance.numero)
                instance.complemento = dados_cnpj.get('complemento', instance.complemento)
                instance.CEP = dados_cnpj.get('cep', instance.CEP)
                instance.bairro = dados_cnpj.get('bairro', instance.bairro)
                instance.cidade = dados_cnpj.get('municipio', instance.cidade)
                instance.estado = dados_cnpj.get('uf', instance.estado)
                if not instance.telefone:
                    instance.telefone = dados_cnpj.get('telefone', instance.telefone)
                if not instance.email:
                    instance.email = dados_cnpj.get('email', instance.email)
                instance.efr = dados_cnpj.get('efr', instance.efr)
                instance.situacao = dados_cnpj.get('situacao', instance.situacao)
                instance.data_situacao = dados_cnpj.get('data_situacao', instance.data_situacao)
                instance.motivo_situacao = dados_cnpj.get('motivo_situacao', instance.motivo_situacao)
                instance.situacao_especial = dados_cnpj.get('situacao_especial', instance.situacao_especial)
                instance.data_situacao_especial = dados_cnpj.get('data_situacao_especial', instance.data_situacao_especial)
                instance.capital_social = dados_cnpj.get('capital_social', instance.capital_social)
                instance.atividade_principal = dados_cnpj.get('atividade_principal', instance.atividade_principal)
                instance.atividades_secundarias = dados_cnpj.get('atividades_secundarias', instance.atividades_secundarias)
                instance.qsa = dados_cnpj.get('qsa', instance.qsa)

                instance.save()

@login_required(redirect_field_name='redirect_to')
def proposta_Brg(request, id, *args, **kwargs):
    
    proposta_brg = Proposta_Brg.objects.get(id=id)
    produtos = produto_proposta.objects.filter(proposta_Brg=proposta_brg)
    personalizacao = Personalizar.objects.filter(proposta_Brg=proposta_brg)
    acessorios = Acessorio_propostas.objects.filter(proposta_Brg=proposta_brg)
    clientes = Cliente.objects.filter(proposta_brg=proposta_brg)
    motores = Motor.objects.all()
    descontos = Desconto.objects.all()

    # Verifica se o usuário ainda não está definido na proposta
    if not proposta_brg.user:
        proposta_brg.user = request.user
        proposta_brg.save()
        
    soma_total = 0
    soma_frete = 0
    soma_instalacao = 0
    soma_gerador = 0
    soma_gera = 0
    desconto = 0
    dados_cnpj = 0
    img_personalizada = 0 
    obs_personalizada = 0
    
    soma_acessorio = 0
    soma_acess = 0 
    soma_total_acessorio = 0
    soma_frete_acessorio = 0
    soma_instalacao_acessorio = 0
    soma_gerador_acessorio = 0
    img_acessorio = 0
    
    for produto in produtos:    
        if produto.valor_transf:
            soma_gera += produto.quantidade_Gerador * produto.valor_transf * (1 - produto.Desconto.desconto/100)
        elif produto.valor_gerador:
            soma_gera += produto.quantidade_Gerador * produto.valor_gerador * (1 - produto.Desconto.desconto/100)

    for acessorio in acessorios:    
        #    if acessorio.valor_acessorio:
            soma_acess += acessorio.quantidade_acessorio * acessorio.valor_acessorio
            img_acessorio = acessorio.acessorio.imagem
   
                               
    soma_gerador += (soma_gera)
    soma_acessorio += (soma_acess)

    soma_gerador_acessorio += (soma_gera + soma_acess)


    soma_total = soma_gerador + soma_acessorio + proposta_brg.Frete + proposta_brg.Valor_Instalação
    soma_frete += soma_gerador + soma_acessorio + proposta_brg.Frete
    soma_instalacao += soma_gerador + soma_acessorio + proposta_brg.Valor_Instalação
    
    for personalizar in personalizacao:

        img_personalizada = personalizar.imagem
        obs_personalizada = personalizar.Observacao  
    
    contexto = {'proposta':proposta_brg,
                'produtos':produtos,
                'acessorios':acessorios,
                'clientes':clientes,
                'motores':motores,
                
                'personalizacao':personalizacao,
                'img_personalizada':img_personalizada,
                'obs_personalizada':obs_personalizada,
                
                'desconto':desconto,
                
                'soma_total':soma_total,
                'soma_gera':soma_gera,
                'soma_frete':soma_frete,
                'soma_gerador':soma_gerador,
                'soma_instalacao':soma_instalacao,
                
                'soma_acessorio':soma_acessorio,
                'soma_acess':soma_acess,
                'soma_gerador_acessorio':soma_gerador_acessorio,
                'img_acessorio':img_acessorio,
                }
    
    return render(request, "proposta_brg.html", contexto)

    

@login_required(redirect_field_name='redirect_to')
def proposta_Grid(request, id, *args, **kwargs):
    proposta_grid = Proposta_Grid.objects.get(id=id)
    produtos = produto_proposta.objects.filter(proposta_Grid=proposta_grid)
    personalizacao = Personalizar.objects.filter(proposta_Grid=proposta_grid)
    acessorios = Acessorio_propostas.objects.filter(proposta_Grid=proposta_grid)
    clientes = Cliente.objects.filter(propostas_grid=proposta_grid)
    motores = Motor.objects.all()
    descontos = Desconto.objects.all()
    

    # Verifica se o usuário ainda não está definido na proposta
    if not proposta_grid.user:
        proposta_grid.user = request.user
        proposta_grid.save()
        
    soma_total = 0
    soma_frete = 0
    soma_instalacao = 0
    soma_gerador = 0
    soma_gera = 0
    desconto = 0
    dados_cnpj = 0
    img_personalizada = 0 
    obs_personalizada = 0
    
    soma_acessorio = 0
    soma_acess = 0 
    soma_total_acessorio = 0
    soma_frete_acessorio = 0
    soma_instalacao_acessorio = 0
    soma_gerador_acessorio = 0
    img_acessorio = 0
    
    for produto in produtos:    
        if produto.valor_transf:
            soma_gera += produto.quantidade_Gerador * produto.valor_transf * (1 - produto.Desconto.desconto/100)
        elif produto.valor_gerador:
            soma_gera += produto.quantidade_Gerador * produto.valor_gerador * (1 - produto.Desconto.desconto/100)

    for acessorio in acessorios:    
        #    if acessorio.valor_acessorio:
            soma_acess += acessorio.quantidade_acessorio * acessorio.valor_acessorio
            img_acessorio = acessorio.acessorio.imagem
   
                               
    soma_gerador += (soma_gera)
    soma_acessorio += (soma_acess)

    soma_gerador_acessorio += (soma_gera + soma_acess)

    soma_total = soma_gerador + soma_acessorio 
    soma_frete += proposta_grid.Frete_ida + proposta_grid.Frete_volta
    soma_instalacao += proposta_grid.Frete_ida + proposta_grid.Frete_volta + proposta_grid.Valor_Instalação
    

    
    for personalizar in personalizacao:

        img_personalizada = personalizar.imagem
        obs_personalizada = personalizar.Observacao  
    
    contexto = {'proposta':proposta_grid,
                'produtos':produtos,
                'acessorios':acessorios,
                'clientes':clientes,
                'motores':motores,
                
                'personalizacao':personalizacao,
                'img_personalizada':img_personalizada,
                'obs_personalizada':obs_personalizada,
                
                'desconto':desconto,
                
                'soma_total':soma_total,
                'soma_gera':soma_gera,
                'soma_frete':soma_frete,
                'soma_gerador':soma_gerador,
                'soma_instalacao':soma_instalacao,
                
                'soma_acessorio':soma_acessorio,
                'soma_acess':soma_acess,
                'soma_gerador_acessorio':soma_gerador_acessorio,
                'img_acessorio':img_acessorio,
                }
    
    return render(request, "proposta_grid.html", contexto)




@login_required(redirect_field_name='redirect_to')
def proposta_Agrogera(request, id, *args, **kwargs):
    proposta_agrogera = Proposta_Agrogera.objects.get(id=id)
    produtos = produto_proposta.objects.filter(proposta_Agrogera=proposta_agrogera)
    personalizacao = Personalizar.objects.filter(proposta_Agrogera=proposta_agrogera)
    acessorios = Acessorio_propostas.objects.filter(proposta_Agrogera=proposta_agrogera)
    clientes = Cliente.objects.filter(propostas_agrogera=proposta_agrogera)
    motores = Motor.objects.all()
    descontos = Desconto.objects.all()

    # Verifica se o usuário ainda não está definido na proposta
    if not proposta_agrogera.user:
        proposta_agrogera.user = request.user
        proposta_agrogera.save()
        
    soma_total = 0
    soma_frete = 0
    soma_instalacao = 0
    soma_gerador = 0
    soma_gera = 0
    desconto = 0
    dados_cnpj = 0
    img_personalizada = 0 
    obs_personalizada = 0
    
    soma_acessorio = 0
    soma_acess = 0 
    soma_gerador_acessorio = 0
    img_acessorio = 0
    
    for produto in produtos:    
        if produto.valor_transf:
            soma_gera += produto.quantidade_Gerador * produto.valor_transf * (1 - produto.Desconto.desconto/100)
        elif produto.valor_gerador:
            soma_gera += produto.quantidade_Gerador * produto.valor_gerador * (1 - produto.Desconto.desconto/100)

    for acessorio in acessorios:    
        #    if acessorio.valor_acessorio:
            soma_acess += acessorio.quantidade_acessorio * acessorio.valor_acessorio
            img_acessorio = acessorio.acessorio.imagem
   
                               
    soma_gerador += (soma_gera)
    soma_acessorio += (soma_acess)

    soma_gerador_acessorio += (soma_gera + soma_acess)


    soma_total = soma_gerador + soma_acessorio 
    soma_frete += proposta_agrogera.Frete_ida + proposta_agrogera.Frete_volta
    soma_instalacao += proposta_agrogera.Frete_ida + proposta_agrogera.Frete_volta + proposta_agrogera.Valor_Instalação
    
    
    for personalizar in personalizacao:

        img_personalizada = personalizar.imagem
        obs_personalizada = personalizar.Observacao  
    
    contexto = {'proposta':proposta_agrogera,
                'produtos':produtos,
                'acessorios':acessorios,
                'clientes':clientes,
                'motores':motores,
                
                'personalizacao':personalizacao,
                'img_personalizada':img_personalizada,
                'obs_personalizada':obs_personalizada,
                
                'desconto':desconto,
                
                'soma_total':soma_total,
                'soma_gera':soma_gera,
                'soma_frete':soma_frete,
                'soma_gerador':soma_gerador,
                'soma_instalacao':soma_instalacao,
                
                'soma_acessorio':soma_acessorio,
                'soma_acess':soma_acess,
                'soma_gerador_acessorio':soma_gerador_acessorio,
                'img_acessorio':img_acessorio,
                }
    
    return render(request, "proposta_agrogera.html", contexto)
