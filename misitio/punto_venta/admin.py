from django.contrib import admin # type: ignore
from .models import Impuesto, Categoria, Producto, Cliente, Venta, Proveedor, Inventario, Empleado, Devolucion

admin.site.register(Impuesto)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Venta)
admin.site.register(Proveedor)
admin.site.register(Inventario)
admin.site.register(Empleado)
admin.site.register(Devolucion)