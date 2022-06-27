from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

from django.shortcuts import redirect, render

from .models import Avatar, Producto, Proveedor
from .forms import FormularioCompra, FormularioRegistro, FormularioProveedor, EditarUsuarioForm,FormularioAvatar

from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import DeleteView, DetailView

from django.contrib.auth.decorators import login_required

from django.contrib import messages
# Create your views here.

def index_template (request):
    productos= Producto.objects.all()
    
    return render(request, 'FinalApp/index.html', {'productos': productos})


@login_required
def publicar (request):
    
    producto_venta = None
        
    if request.method == 'POST':
        
        formulario = FormularioCompra(request.POST)
        if formulario.is_valid():
            datos_validados = formulario.cleaned_data
            producto_venta = Producto(producto= datos_validados['producto'], precio= datos_validados['precio'])

            producto_venta.save()
            
            messages.success(request, f'{producto_venta.producto} fue añadido a la lista de publicados')
            return redirect('publicar')
        
    formulario = FormularioCompra()  
    return render(request, 'FinalApp/publicar.html', {'producto_venta': producto_venta, 'formulario': formulario})

@login_required
def editar_producto (request,id):
    
    
    producto= Producto.objects.get(id=id)

    formulario = FormularioCompra({'producto': producto.producto, 'precio': producto.precio})

    if request.method == 'POST':
        
        formulario = FormularioCompra(request.POST)
        
        if formulario.is_valid():
            
            producto.producto= formulario.cleaned_data['producto']
            producto.precio= formulario.cleaned_data['precio']
           
            producto.save()
            
            messages.success(request, f'{producto.producto} fue modificado')
            return redirect('indice')

    return render(request, 'FinalApp/editar_producto.html', {'formulario': formulario})


def hacer_registro (request):
    
    if request.method == 'POST':
        formulario= FormularioRegistro(request.POST)
        
        if formulario.is_valid():
            
            formulario.save()
            
            messages.success(request, 'Se ha completado tu registro')
            return redirect('acceso')

        else:
            return render(request, 'FinalApp/registro.html', {'mensaje': 'Corrobore la validez de los datos','formulario': formulario})

    formulario= FormularioRegistro()
    
    return render(request, 'FinalApp/registro.html', {'mensaje': 'Complete el Registro para iniciar','formulario': formulario})


def verificar_registro (request):
    error=''

    if request.method == 'POST':
        formulario= AuthenticationForm(request, data=request.POST)
        
        if formulario.is_valid():
        
            username= formulario.cleaned_data['username']
            password= formulario.cleaned_data['password']
        
            user= authenticate(username=username, password=password)
        
            if user is not None:
                
                login(request,user)
                
                messages.success(request, 'Se ha loggeado exitosamente')
                return redirect('indice')
         
            else:
                error= 'Comprueba tus datos'
                return render(request, 'FinalApp/inicio.html', {'formulario':formulario, 'mensaje': error})
                
        else:
            error= 'Ingresa un usuario válido'
            return render(request, 'FinalApp/inicio.html', {'formulario':formulario, 'mensaje': error})
        
    
    formulario= AuthenticationForm()

    return render(request, 'FinalApp/inicio.html', {'formulario':formulario, 'mensaje': error})


@login_required
def editar_perfil (request):
    
    usuario= request.user
    
    if request.method == 'POST':
        formulario= EditarUsuarioForm(request.POST)
        
        if formulario.is_valid():
            
            usuario.email = formulario.cleaned_data['email']
            usuario.password1 = formulario.cleaned_data['password1']
            usuario.password2 = formulario.cleaned_data['password2']
            usuario.first_name = formulario.cleaned_data['first_name']
            usuario.last_name = formulario.cleaned_data['last_name']
            
 
            usuario.save()
          
        messages.success(request, 'Tu perfil fue modificado')
        return redirect('perfil')
            
    
    else:
                  
        formulario= EditarUsuarioForm(initial={'email': usuario.email, 'first_name': usuario.first_name, 'last_name': usuario.last_name})
    
    return render(request, 'FinalApp/editar_perfil.html', {'formulario': formulario})



def buscar_producto (request):
    compra= None
    error= None
    if request.method == 'GET':
        producto= request.GET.get('producto', '')
        if producto == '':
            error= 'ingresa una compra'
        else:
            try:
                compra=Producto.objects.filter(producto=producto)
                if compra:
                    compra
                else:
                    error= 'No se encontraron coincidencias \n Intenta con otro producto'
            except:
                error= 'No se encontraron coincidencias \n Intenta con otro producto'
    
    productos= Producto.objects.all()
                
    return render(request, 'FinalApp/index.html', {'compra': compra, 'error': error, 'productos': productos})

@login_required
def asociar (request):
    registro= None
    if request.method == 'POST':
        
        formulario= FormularioProveedor(request.POST)
        if formulario.is_valid():
            datos= formulario.cleaned_data
            registro= Proveedor(nombre= datos['nombre'], tipo= datos['tipo'], email= datos['email'])
            registro.save()
            
            messages.success(request, 'Ya sos parte de la comunidad')
            return redirect('publicar')
 
            
    formulario= FormularioProveedor()
    return render(request, 'FinalApp/proveedor.html', {'registro': registro, 'formulario': formulario})


@login_required
def perfil (request):
    
    usuario= request.user
    username= usuario.username
    nombre= usuario.first_name
    apellido= usuario.last_name
    email=usuario.email

    try:
        avatar=Avatar.objects.get(user=usuario)
    except:  
        avatar= None

    return render(request, 'FinalApp/perfil.html', {'mensaje': f'Bienvenido a tu perfil {username}', 'nombre':nombre, 'apellido':apellido, 'email':email, 'avatar':avatar})

@login_required
def cambiar_avatar (request):
    
    usuario= request.user
    
    if request.method == 'POST':
        formulario= FormularioAvatar(request.POST, request.FILES)
        
        if formulario.is_valid():
            try:
                avatar= Avatar.objects.get(user=usuario)
                avatar.avatar = formulario.cleaned_data['avatar']
                avatar.save()
                
            except:
                avatar=Avatar(user=usuario,avatar=formulario.cleaned_data['avatar'])
                avatar.save()
                
            messages.success(request, 'Tu avatar fue modificado')
            return redirect('perfil')
            #return render(request, 'FinalApp/perfil.html', {'mensaje': 'Tu avatar fue modificado'})

            
    else:
                  
        formulario= FormularioAvatar
    
    return render(request, 'FinalApp/editar_avatar.html', {'formulario': formulario, 'mensaje':''})


class ProductoDetailView (DetailView):
    model= Producto
    template_name= 'FinalApp/productoid.html'
    
class ProductoEliminar (LoginRequiredMixin,DeleteView):
    model= Producto
    success_url = 'index/'
    template_name= 'FinalApp/producto_confirm_elim.html'
    
    
def about (request):
    
    return render(request, 'FinalApp/about.html', {})

    
def ver_proveedores (request):
    mensaje= ''
    proveedores= Proveedor.objects.all()
    if proveedores:
        mensaje='Estos son nuestros proveedores.'
    else:
        
        mensaje='No hay proveedores en la lista aun.'
    
    return render(request, 'FinalApp/proveedor_lista.html', {'proveedores': proveedores, 'mensaje': mensaje})

@login_required
def editar_proveedor (request,id):
    
    proveedor= Proveedor.objects.get(id=id)

    formulario = FormularioProveedor({'nombre': proveedor.nombre, 'tipo': proveedor.tipo, 'email': proveedor.email})

    if request.method == 'POST':
        
        formulario = FormularioProveedor(request.POST)
        
        if formulario.is_valid():
            
            proveedor.nombre= formulario.cleaned_data['nombre']
            proveedor.tipo= formulario.cleaned_data['tipo']
            proveedor.email= formulario.cleaned_data['email']
           
            proveedor.save()
            
            messages.success(request, f'{proveedor.nombre} fue modificado')
            return redirect('lista_proveedores')

    return render(request, 'FinalApp/editar_proveedor.html', {'formulario': formulario})


class ProveedorEliminar (LoginRequiredMixin,DeleteView):
    model= Proveedor
    success_url = 'ver_proveedores/'
    template_name= 'FinalApp/proveedor_confirm_elim.html'
    