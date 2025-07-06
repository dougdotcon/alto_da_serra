from django.urls import path
from . import views

app_name = 'mesas'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('mesa/<str:mesa_id>/', views.mesa_detail_view, name='mesa_detail'),
    path('produtos/', views.produtos_view, name='produtos'),
    path('estoque/', views.estoque_view, name='estoque'),
    path('cozinha/', views.cozinha_view, name='cozinha'),
    path('api/mesas/', views.api_mesas, name='api_mesas'),
    path('api/consumo/<str:mesa_id>/', views.api_consumo, name='api_consumo'),
    path('api/produtos/', views.api_produtos, name='api_produtos'),
    path('api/adicionar-pedido/', views.api_adicionar_pedido, name='api_adicionar_pedido'),
    path('api/abater-consumo/', views.api_abater_consumo, name='api_abater_consumo'),
    path('api/atualizar-mesa/', views.api_atualizar_mesa, name='api_atualizar_mesa'),
    path('api/editar-mesa/', views.api_editar_mesa, name='api_editar_mesa'),
    path('api/finalizar-conta/', views.api_finalizar_conta, name='api_finalizar_conta'),
]
