from django.db import models

class ScrapyWebFarmatodo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=250)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.CharField(max_length=500)
    fecha = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
