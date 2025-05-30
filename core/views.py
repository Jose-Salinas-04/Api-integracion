from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from carrito.models import CarritoItem
import requests



@login_required
def ver_carrito(request):
    items = CarritoItem.objects.filter(usuario=request.user)
    total = sum(item.subtotal() for item in items)
    return render(request, 'core/carrito.html', {'items': items, 'total': total})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def home(request):
    response = requests.get('http://localhost:3000/products')  # json-server
    products = response.json()
    return render(request, 'core/home.html', {'products': products})