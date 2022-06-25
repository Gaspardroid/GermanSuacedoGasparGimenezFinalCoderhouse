from django.contrib import admin

from .models import Producto, Proveedor, Avatar

admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(Avatar)


