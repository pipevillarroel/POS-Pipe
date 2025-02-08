from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import ProductoForm, ClienteForm, ClienteEditForm
from .models import Cliente, Producto

# Página principal
def index(request):
    return render(request, "index.html")

@login_required
def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)  # Buscar el cliente por su ID

    if request.method == 'POST':
        # Obtener los datos del formulario y actualizar el cliente
        cliente.nombre = request.POST.get('nombre')
        cliente.email = request.POST.get('email')
        cliente.telefono = request.POST.get('telefono')
        cliente.direccion = request.POST.get('direccion')

        # Guardar los cambios en la base de datos
        cliente.save()

        # Redirigir al detalle del cliente o a donde desees
        return redirect('cliente_detail', pk=cliente.pk)

    # Si no es un POST, mostrar el formulario con los datos actuales del cliente
    return render(request, 'cliente/cliente_edit.html', {'cliente': cliente})
@login_required
def menu_view(request):
    return render(request, 'menu.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('login')  # Redirige al login después de hacer logout

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")  # Corregir el nombre del campo
        password = request.POST.get("password")  # Asegúrate de que el nombre coincida
        password2 = request.POST.get("confirm_password")  # Coincide con el campo de confirmación
        
        if password != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password)
        user.save()

        messages.success(request, "Usuario registrado con éxito")
        return redirect("login")  # Redirigir al login después de registrarse

    return render(request, "register.html")

# Inicio de sesión (aún no implementado)
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Si el usuario es válido, iniciar sesión
            login(request, user)
            return redirect('menu')  # Redirige a la página de inicio, puedes cambiar 'home' por cualquier otra página
        else:
            # Si no es válido, mostrar un mensaje de error
            messages.error(request, "Nombre de usuario o contraseña incorrectos")
    
    return render(request, 'login.html')

# Listado de clientes
def clientes_list(request):
    search_query = request.GET.get('search', '')  # Obtener el término de búsqueda
    clientes = Cliente.objects.all()

    # Si hay una consulta de búsqueda, filtramos los resultados
    if search_query:
        clientes = clientes.filter(
            Q(rut__icontains=search_query) | 
            Q(nombre__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    paginator = Paginator(clientes, 20)  # Mostrar 20 clientes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    response = render(request, "cliente/cliente_list.html", {"page_obj": page_obj})
    response['Cache-Control'] = 'no-store'  # Evitar caché
    return response

# Creación de cliente
def cliente_create(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes_list')  # Redirigir correctamente a 'clientes_list'
    else:
        form = ClienteForm()
    return render(request, "cliente/cliente_create.html", {"form": form})

# Detalles de un cliente
def cliente_detail(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    # Si se recibe una solicitud POST para eliminar el cliente
    if request.method == "POST" and 'delete' in request.POST:
        cliente.delete()
        messages.success(request, "Cliente eliminado con éxito.")
        return redirect('clientes_list')
    
    return render(request, "cliente/cliente_detail.html", {"cliente": cliente})

# Vista para eliminar cliente
@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    
    # Solo eliminar si el método es POST
    if request.method == "POST":
        cliente.delete()
        messages.success(request, "Cliente eliminado con éxito.")
        return redirect('clientes_list')

    # Renderizar el cliente_detail.html si no es POST, esperando que el usuario confirme la eliminación
    return render(request, 'cliente/cliente_detail.html', {'cliente': cliente, 'confirm_delete': True})

@login_required
def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente actualizado con éxito.")
            return redirect('cliente_detail', pk=cliente.pk)
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'cliente/cliente_create.html', {'form': form, 'edit': True})