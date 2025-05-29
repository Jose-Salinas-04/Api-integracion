from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('', views.get_cart, name='get_cart'),
    path('update/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('pagar/', views.simular_pago, name='simular_pago'),
]