from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from datetime import date, datetime
from django.forms import model_to_dict



#Base Global para todas las tablas
class ModelBase(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.BooleanField('Status', default=True)
    date_create = models.DateField('Date of Create',auto_now = False, auto_now_add = True)
    date_change = models.DateField('Date of Change',auto_now = True, auto_now_add = False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    date_time_c = models.TimeField(auto_now = False, auto_now_add = True)
    date_time_m = models.TimeField(auto_now = True, auto_now_add = False)

    class Meta:
        abstract = True


class Categoria(ModelBase):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Gasto(ModelBase):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    descripcion = models.TextField()

    def __str__(self):
        return f' {self.categoria}: {self.cantidad}'


class Ingreso(ModelBase):
    
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    descripcion = models.TextField()

    def __str__(self):
        return f'Ingreso: {self.categoria.nombre} - {self.cantidad}'


class PagoMensual(ModelBase):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    fecha_vencimiento = models.DateField()
    

    def __str__(self):
        return f'Pago mensual: {self.descripcion} - {self.categoria.nombre}'
