from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.home, name='home'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
]

# urlpatterns += [
#     path('api/cart/', api_views.get_cart, name='get_cart'),
#     path('api/cart/add/', api_views.add_to_cart, name='add_to_cart'),
# ]