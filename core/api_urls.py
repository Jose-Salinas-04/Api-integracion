from django.urls import path
from . import api_views

urlpatterns = [
    path('cart/', api_views.CartListCreateView.as_view(), name='cart'),
    path('cart/<int:pk>/', api_views.CartItemDetailView.as_view(), name='cart-item-detail'),
]