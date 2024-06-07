from django.urls import path
from . import views

urlpatterns = [
    # URLs de vistas normales
    path('', views.listar_productos, name='listar_productos'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    # Nueva ruta para exportar CSV
    path('exportar/', views.exportar_productos_csv, name='exportar_productos_csv'),
    # Nueva ruta para importar SCV  
    path('importar/', views.importar_productos_csv, name='importar_productos_csv'),
]