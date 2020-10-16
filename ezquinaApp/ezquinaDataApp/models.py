from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Inventario(models.Model):
    Producto = models.CharField(max_length=100)
    Descripcion = models.CharField(max_length=250)
    Cantidad = models.IntegerField()
    PrecioCliente = models.DecimalField(max_digits=20,  decimal_places=2)
    PrecioProvedor = models.DecimalField(max_digits=20,  decimal_places=2)

    class Meta:
        verbose_name_plural = "Inventario"

    def __str__(self):
        return self.Producto

class Probedor(models.Model):
    Probedor = models.CharField(max_length=50)
    Descripcion = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Probedores"

    def __str__(self):
        return self.Probedor

class TransaccionesClientes(models.Model):
    Usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    Fecha = models.DateField(auto_now_add=True, blank=True)
    Producto = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    Cantidad = models.IntegerField()
    CostoTotal = models.DecimalField(max_digits=20,  decimal_places=2)

    class Meta:
        verbose_name_plural = "Transacciones de Clientes"

    def __str__(self):
        return self.CostoTotal

class TransaccionesProbedores(models.Model):
    Usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    Probedor = models.ForeignKey(Probedor, on_delete=models.CASCADE)
    Fecha = models.DateField(auto_now_add=True, blank=True)
    Producto = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    Cantidad = models.IntegerField()
    CostoTotal = models.DecimalField(max_digits=20,  decimal_places=2)

    class Meta:
        verbose_name_plural = "Transacciones de Probedores"

    def __str__(self):
        return self.CostoTotal

