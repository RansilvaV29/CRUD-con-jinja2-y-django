import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm
from django.db.models import Q
from .forms import CSVUploadForm
from django.contrib import messages



def listar_productos(request):
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    productos = Producto.objects.all()

    if query:
        productos = productos.filter(
            Q(nombre__icontains=query)
        )

    if min_price:
        productos = productos.filter(precio__gte=min_price)

    if max_price:
        productos = productos.filter(precio__lte=max_price)

    return render(request, 'listar.html', {'productos': productos})


def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'producto_form.html', {'form': form})

def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'producto_form.html', {'form': form})

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')
    return render(request, 'confirmar_eliminar.html', {'producto': producto})



#exportacion de los productos a un CSV

def exportar_productos_csv(request):
    # Crear el objeto HttpResponse con el tipo de contenido adecuado
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="productos.csv"'

    # Crear un escritor CSV usando el objeto HttpResponse
    writer = csv.writer(response)
    writer.writerow(['nombre', 'precio', 'cantidad'])

    # Escribir datos del modelo Producto
    productos = Producto.objects.all().values_list('nombre', 'precio', 'cantidad')
    for producto in productos:
        writer.writerow(producto)

    return response


#importar de csv
def importar_productos_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                Producto.objects.create(
                    nombre=row['nombre'],
                    precio=row['precio'],
                    cantidad=row['cantidad']
                )
            messages.success(request, 'Productos importados exitosamente.')
            return redirect('listar_productos')
    else:
        form = CSVUploadForm()
    return render(request, 'importar.html', {'form': form})