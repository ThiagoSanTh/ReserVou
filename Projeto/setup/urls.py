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
from ReserVou.views import (paginaInicial, 
                            gerenciarHoteis, cadastrarHotel, editarHotel, deletarHotel, 
                            editarQuarto, deletarQuarto, cadastrarQuarto, 
                            cadastrarCliente, editarCliente, deletarCliente, perfilCliente,
                            selecionarDatas, reservarListarHoteis, listarQuartos, fazerReserva, fazerPagamento, cancelarReserva
                            )

urlpatterns = [
    path('admin/', admin.site.urls),


        #pagina inicial
    path('', paginaInicial.as_view(), name='home'),


        #hotel
    path('hoteis/', gerenciarHoteis.as_view(), name = 'gerenciar_hoteis'),
    path('hoteis/cadastrar', cadastrarHotel.as_view(), name = 'cadastrar_hotel'),
    path('editar_hotel/<int:pk>/', editarHotel.as_view(), name = 'editar_hotel'),
    path('deletar_hotel/<int:pk>/', deletarHotel.as_view(), name = 'deletar_hotel'),


        #quarto
    path('hotel/<int:pk>/quartos/', listarQuartos.as_view(), name = 'listar_quartos'),
    path('hotel/<int:pk>/quarto/cadastrar/', cadastrarQuarto.as_view(), name = 'cadastrar_quarto'),
    path('editar_quarto/<int:pk>/', editarQuarto.as_view(), name = 'editar_quarto'),
    path('deletar_quarto/<int:pk>/', deletarQuarto.as_view(), name = 'deletar_quarto'),
    

        #Interface
    path('reserva/<int:quarto_id>/reservar/', fazerReserva.as_view(), name = 'fazer_reserva'),
    path('reserva/<int:reserva_id>/cancelar/', cancelarReserva.as_view(), name='cancelar_reserva'),
    path('selecionar_datas/', selecionarDatas.as_view(), name='selecionar_datas'),
    path('reserva/pagamento/', fazerPagamento.as_view(), name = 'fazer_pagamento'),
    path('reservar_listar_hoteis/', reservarListarHoteis.as_view(), name = 'reservar_listar_hoteis'),
    path('login_hotel/', views.loginHotel.as_view(), name='login_hotel'),
    path('login_cliente/', views.loginCliente.as_view(), name='login_cliente'),
    path('logout/', views.LogoutView.as_view(), name='logout'),


        #cliente
    path('clientes/novo/', cadastrarCliente.as_view(), name = 'cadastrar_cliente'),
    path('deletar_cliente/<int:pk>/', deletarCliente.as_view(), name = 'deletar_cliente'),
    path('editar_cliente/<int:pk>/', editarCliente.as_view(), name = 'editar_cliente'),
    path('clientes/<int:pk>/', perfilCliente.as_view(), name = 'perfil_cliente'),


]