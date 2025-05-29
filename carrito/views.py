from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import CarritoItem
import requests
import json

@csrf_exempt
@login_required
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        producto_id = data.get('product_id')
        nombre = data.get('nombre')
        precio = data.get('precio')
        cantidad = data.get('cantidad', 1)

        item, created = CarritoItem.objects.get_or_create(
            usuario=request.user,
            producto_id=producto_id,
            defaults={'nombre': nombre, 'precio': precio, 'cantidad': cantidad}
        )
        if not created:
            item.cantidad += cantidad
            item.save()

        return JsonResponse({'message': 'Producto agregado al carrito'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def get_cart(request):
    items = CarritoItem.objects.filter(usuario=request.user)
    carrito = [
        {
            'producto_id': item.producto_id,
            'nombre': item.nombre,
            'precio': float(item.precio),
            'cantidad': item.cantidad,
            'subtotal': float(item.subtotal())
        }
        for item in items
    ]
    return JsonResponse({'carrito': carrito})


from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

@csrf_exempt
@require_POST
@login_required
def actualizar_cantidad(request):
    data = json.loads(request.body)
    producto_id = data.get('producto_id')
    accion = data.get('accion')  # "sumar" o "restar"

    item = get_object_or_404(CarritoItem, usuario=request.user, producto_id=producto_id)

    if accion == "sumar":
        item.cantidad += 1
        item.save()
    elif accion == "restar":
        item.cantidad -= 1
        if item.cantidad <= 0:
            item.delete()
            return JsonResponse({'message': 'Producto eliminado del carrito'})
        else:
            item.save()

    return JsonResponse({'message': 'Cantidad actualizada'})



@csrf_exempt
@require_POST
@login_required
def simular_pago(request):
    items = CarritoItem.objects.filter(usuario=request.user)

    for item in items:
        producto_id = item.producto_id
        cantidad = item.cantidad

        # Obtener producto actual desde json-server
        res = requests.get(f'http://localhost:3000/products/{producto_id}')
        if res.status_code != 200:
            continue
        producto = res.json()
        stock_actual = producto.get('stock', 0)

        # Nuevo stock
        nuevo_stock = stock_actual - cantidad
        if nuevo_stock < 0:
            nuevo_stock = 0

        # Actualizar producto en json-server
        requests.patch(
            f'http://localhost:3000/products/{producto_id}',
            json={'stock': nuevo_stock}
        )

    # Vaciar carrito
    items.delete()
    return JsonResponse({'message': 'Pago simulado con éxito. Stock actualizado y carrito vacío.'})