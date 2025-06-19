from django.db import models
from django.urls import reverse
# Create your models here.
class Categoria(models.Model):

    nombre = models.CharField(max_length=30)
    descripcion =  models.TextField()   
    fermentacion = models.CharField(max_length=20)
    sabor = models.CharField(max_length=30)

    # el metodo se usa para mostrar su nombre cuando se muestre el objeto en el panel de administracion
    def __str__(self):
        return self.nombre
    
class GraduacionAlcoholica(models.Model):

    porcentaje = models.FloatField()

    # metodo para mostrar el porcentaje de alcohol
    def __str__(self):
        return f"{self.porcentaje}%"

class Cerveza(models.Model):

    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()
    estilo = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    porcentaje_alcohol = models.ForeignKey(GraduacionAlcoholica, on_delete=models.SET_NULL, null=True)
    ibu = models.IntegerField()
    foto = models.ImageField(upload_to='cervezas/', null=True, blank=True)
    disponible =  models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('cervezaInfo', args=[str(self.id)])
    def __str__(self):
        return self.nombre

class Envasado(models.Model):
    tipo = models.CharField(max_length=30)          # barril, lata, botella
    volumen_ml = models.CharField(max_length=30)     # 500, 1000, 30000, 50000

    def __str__(self):
        return f"{self.tipo} {self.volumen_ml}ml"
    
class Formato(models.Model):

    cerveza = models.ForeignKey(Cerveza, on_delete=models.SET_NULL, null=True)
    envasado = models.ForeignKey(Envasado, on_delete=models.SET_NULL, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)                    
    foto = models.ImageField(upload_to = 'catalogo/upload/img/', null=True)

    def __str__(self):
        return f"{self.envasado.tipo} {self.envasado.volumen_ml}ml - {self.cerveza.nombre}"
    
class Servicio(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    foto = foto = models.ImageField(upload_to = 'catalogo/upload/img/', null=True)

    def __str__(self):
        return self.nombre
    
class Chopera(Servicio):
    litros = models.IntegerField()

class Barra(Servicio):
    canillas = models.IntegerField()
    disponible = models.BooleanField()

class Bar(models.Model): 
    nombre = models.CharField(max_length=30)
    lugar = models.TextField()
    hora_habre = models.TimeField()
    hora_cierra = models.TimeField()


class Usuario(models.Model):
    nombre = models.CharField(max_length=30)
    contraseña = models.CharField(max_length=30)

