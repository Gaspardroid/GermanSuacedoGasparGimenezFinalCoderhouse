from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    producto= models.CharField(max_length=40)
    precio= models.FloatField()
    
    def __str__(self):
        return f"$ {self.precio} la unidad de {self.producto}"
        

class Proveedor(models.Model):
    nombre= models.CharField(max_length=20)
    tipo= models.CharField(max_length=20)
    email= models.EmailField()
    
    def __str__(self):
        return f"Nombre: {self.nombre} Tipo de produccion: {self.tipo} Contacto {self.email}"
                
    
class Avatar (models.Model):
    
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    avatar= models.ImageField(upload_to='avatares', null=True, blank=True)
    