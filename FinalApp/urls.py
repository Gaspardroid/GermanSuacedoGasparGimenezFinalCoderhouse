
from django.urls import path

from FinalApp.views import index_template, publicar, hacer_registro,verificar_registro, buscar_producto, asociar, perfil,editar_perfil, cambiar_avatar,editar_producto,about,ver_proveedores,editar_proveedor
from . import views

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path ('publicar/', publicar, name='publicar'),
    path ('about/', about, name='about'),
    path ('editar_producto/<int:id>', editar_producto, name='editar_producto'),
    path ('index/', index_template, name= 'indice'),
    path ('registrar/', hacer_registro, name= 'registrar'),
    path ('', verificar_registro, name= 'acceso'),
    path ('logout/', LogoutView.as_view(template_name='FinalApp/logout.html'), name= 'salir'),
    path ('buscar/', buscar_producto, name= 'buscar'),
    path ('asociar/', asociar, name= 'asociar'),
    path ('index/ver_proveedores/', ver_proveedores, name= 'lista_proveedores'),
    path ('editar_proveedores/<int:id>', editar_proveedor, name= 'editar_proveedor'),
    path ('profile/', perfil, name= 'perfil'),
    path ('ver_producto/<int:pk>', views.ProductoDetailView.as_view(), name='ver_producto'),
    path ('<int:pk>', views.ProductoEliminar.as_view(), name='eliminar_producto'),
    path ('index/<int:pk>', views.ProveedorEliminar.as_view(), name='eliminar_proveedor'),
    path ('edit_profile/', editar_perfil, name= 'editar_perfil'),
    path ('edit_avatar/', cambiar_avatar, name= 'editar_avatar'),
]
