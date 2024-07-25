from django.db import models
import datetime

class Piscinas(models.Model):
    nombre = models.CharField(max_length=45, unique=True)
    ubicacion = models.CharField(max_length=45)

    def __str__(self) -> str:
        return self.nombre

class Parametros(models.Model):
    nombre = models.CharField(max_length=20, null=False, blank=False)
    unidad = models.CharField(max_length=10, blank=True)
    rango_max = models.DecimalField(max_digits=4, decimal_places=2)
    rango_min = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self) -> str:
        return self.nombre

class Mediciones(models.Model):
    piscina = models.ForeignKey(Piscinas, on_delete=models.DO_NOTHING, default="Eliminada")
    oxigeno = models.DecimalField(max_digits=4, decimal_places=2)
    ph = models.DecimalField(max_digits=4, decimal_places=2)
    salinidad = models.DecimalField(max_digits=4, decimal_places=2)
    fecha = models.DateField(default=datetime.date.today)
    hora = models.TimeField(default=datetime.time(0, 0))

    def __str__(self) -> str:
        return f"{self.piscina.nombre} - {self.fecha}"

