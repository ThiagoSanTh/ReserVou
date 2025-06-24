"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ReserVou import views
from ReserVou.views import (paginaInicial, selecionarDatas, reservarListarHoteis, listarQuartos, fazerReserva, fazerPagamento, cancelarReserva,
                            
                            gerenciarHoteis, cadastrarHotel, editarHotel, deletarHotel, 
                            
                            editarQuarto, deletarQuarto, cadastrarQuarto, 
                            
                            cadastrarCliente, editarCliente, deletarCliente, perfilCliente, loginCliente, logoutCliente,                                         
                           
                            cadastrarGerente, loginGerente, logoutGerente, perfilGerente, editarGerente, deletarGerente
                            )

urlpatterns = [
    path('admin/', admin.site.urls),


        #pagina inicial
    path('', paginaInicial.as_view(), name='home'),

        #gerente
    path('gerente/cadastrar/', cadastrarGerente.as_view(), name='cadastrar_gerente'),
    path('gerente/login/', loginGerente.as_view(), name='login_gerente'),
    path('gerente/logout/', logoutGerente.as_view(), name='logout_gerente'),
    path('gerente/perfil/<int:pk>/', perfilGerente.as_view(), name='perfil_gerente'),
    path('gerente/editar/<int:pk>/', editarGerente.as_view(), name='editar_gerente'),
    path('gerente/deletar/<int:pk>/', deletarGerente.as_view(), name='deletar_gerente'),

        #hotel
    path('hoteis/', gerenciarHoteis.as_view(), name = 'gerenciar_hoteis'),
    path('hoteis/cadastrar', cadastrarHotel.as_view(), name = 'cadastrar_hotel'),
    path('editar_hotel/<int:pk>/', editarHotel.as_view(), name = 'editar_hotel'),
    path('deletar_hotel/<int:pk>/', deletarHotel.as_view(), name = 'deletar_hotel'),


        #quarto
    path('hotel/<int:pk>/quartos/', listarQuartos.as_view(), name = 'listar_quartos'),
    path('hotel/<int:hotel_id>/quarto/cadastrar/', cadastrarQuarto.as_view(), name = 'cadastrar_quarto'),
    path('editar_quarto/<int:pk>/', editarQuarto.as_view(), name = 'editar_quarto'),
    path('deletar_quarto/<int:pk>/', deletarQuarto.as_view(), name = 'deletar_quarto'),
    

        #Interface
    path('reserva/<int:quarto_id>/reservar/', fazerReserva.as_view(), name = 'fazer_reserva'),
    path('reserva/<int:reserva_id>/cancelar/', cancelarReserva.as_view(), name='cancelar_reserva'),
    path('selecionar_datas/', selecionarDatas.as_view(), name='selecionar_datas'),
    path('reserva/pagamento/', fazerPagamento.as_view(), name = 'fazer_pagamento'),
    path('reservar_listar_hoteis/', reservarListarHoteis.as_view(), name = 'reservar_listar_hoteis'),


        #cliente
    path('clientes/novo/', cadastrarCliente.as_view(), name = 'cadastrar_cliente'),
    path('deletar_cliente/<int:pk>/', deletarCliente.as_view(), name = 'deletar_cliente'),
    path('editar_cliente/<int:pk>/', editarCliente.as_view(), name = 'editar_cliente'),
    path('clientes/<int:pk>/', perfilCliente.as_view(), name = 'perfil_cliente'),
    path('clientes/login/', loginCliente.as_view(), name = 'login_cliente'),
    path('clientes/logout/', logoutCliente.as_view(), name = 'logout_cliente'),






]