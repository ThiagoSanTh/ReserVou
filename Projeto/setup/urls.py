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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.pagina_inicial, name='home'),
    path('hoteis/', views.gerenciar_hoteis, name = 'gerenciar_hoteis'),
    path('hoteis/cadastrar', views.cadastrar_hotel, name = 'cadastrar_hotel'),
    path('hotel/<int:hotel_id>/quarto/cadastrar/', views.cadastrar_quarto, name = 'cadastrar_quarto'),
    path('clientes/novo/', views.cadastrar_cliente, name = 'cadastrar_cliente'),
    path('clientes/<int:id>/', views.perfil_cliente, name = 'perfil_cliente'),
    path('reservar_listar_hoteis/', views.reservar_listar_hoteis, name = 'reservar_listar_hoteis'),
    path('hotel/<int:hotel_id>/quartos/', views.listar_quartos, name = 'listar_quartos'),
    path('reserva/<int:quarto_id>/reservar/', views.fazer_reserva, name = 'fazer_reserva'),
    path('reserva/pagamento/', views.fazer_pagamento, name = 'fazer_pagamento'),
    path('deletar_cliente/<int:id>/', views.deletar_cliente, name = 'deletar_cliente'),
    path('editar_cliente/<int:id>/', views.editar_cliente, name = 'editar_cliente'),
]