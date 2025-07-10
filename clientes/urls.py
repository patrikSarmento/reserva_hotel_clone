from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.raiz, name='raiz'),
    path('cadastro/', views.cadastrar_cliente, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('quartos/', views.quartos, name='quartos'),
    path('quarto_standard/', views.quarto_standard, name='quarto_standard'),
    path('quarto_luxo/', views.quarto_luxo, name='quarto_luxo'),
    path('suite_presidencial/', views.suite_presidencial, name='suite_presidencial'),
    path('clientes/', views.listar_clientes, name='listar_clientes'),

    
    path('confirmar_reserva/<str:tipo_quarto>/', views.confirmar_reserva, name='confirmar_reserva'),
    path('sucesso/', views.sucesso, name='sucesso'),
    path('cancelar_reserva/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('minhas_reservas/', views.listar_reservas, name='listar_reservas'),
    path('logout/', auth_views.LogoutView.as_view(template_name='clientes/logout.html'), name='logout')

]
