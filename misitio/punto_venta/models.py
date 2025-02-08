from django.db import models
from django.contrib.auth.models import User

# Modelos base
class Impuesto(models.Model):
    nombre = models.CharField(max_length=50)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} ({self.porcentaje}%)"

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Relación con User
    rut = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(blank=True, null=True, max_length=15)
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.cargo})"

class Producto(models.Model):
    codigo_barras = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, blank=True, null=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    impuesto = models.ForeignKey(Impuesto, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} (${self.precio})"

class Venta(models.Model):
    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta de crédito/débito'),
        ('transferencia', 'Transferencia bancaria'),
    ]
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, blank=True, null=True)
    cantidad = models.IntegerField()
    metodo_pago = models.CharField(max_length=50, choices=METODOS_PAGO, default='efectivo')
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    impuesto = models.ForeignKey(Impuesto, on_delete=models.SET_NULL, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        precio_total_sin_impuesto = self.producto.precio * self.cantidad
        if self.impuesto:
            self.monto_total = precio_total_sin_impuesto * (1 + self.impuesto.porcentaje / 100)
        else:
            self.monto_total = precio_total_sin_impuesto
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venta de {self.cantidad} x {self.producto.nombre} a {self.cliente.nombre if self.cliente else 'Cliente anónimo'}"

class Factura(models.Model):
    venta = models.OneToOneField(Venta, on_delete=models.CASCADE)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    numero_factura = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"Factura {self.numero_factura} - {self.venta}"

class Proveedor(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.rut})"

class Inventario(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    cantidad_disponible = models.IntegerField(default=0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inventario de {self.producto.nombre}: {self.cantidad_disponible} unidades"

class Devolucion(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    razon = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Devolución de {self.venta.producto.nombre} ({self.fecha})"
