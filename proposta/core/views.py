from django.shortcuts import render
from .models import Cliente, Proposta , Produto , Motor
from django.shortcuts import render, redirect

propostas = Proposta.objects.all()

produtos = Produto.objects.all()

motores = Motor.objects.all()

for Proposta in propostas:
    Frete = 0.00
    Valor_Instalação = 0.00
    Subtotal = 0.00
    quantidade_Gerador = 0.00
    valor_gerador = 0.00

    total_Frete = 0.00
    Valor_total_Instalação = 0.00
    valor_total_gerador = 0.00
    Total = 0.00

    Frete += Frete
    Valor_Instalação += Valor_Instalação
    Subtotal += Subtotal
    quantidade_Gerador += quantidade_Gerador
    
    Total= (quantidade_Gerador*(valor_gerador) + Frete + Valor_Instalação)
 

    for i in propostas:
        valor_total_gerador += i.quantidade_Gerador * i.valor_gerador


for Motor in motores:
    
    Modelo_Gerador = 0 
    Dimensoes = 0
    
    if(Modelo_Gerador == 'Slim_40_kVA_Carenado_Silenciado'):
        Dimensoes += 'perkins'
    else:
        Dimensoes += 'Volvo'
