from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import FormularioRegistroUsuarios, FormularioAportesEmpleado
from .models import CalculoAportes
import csv
from django.http import HttpResponse
from django.contrib.auth.models import User

def home(request):
    # chequear si el usuario esta logueado
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # autenticarlo
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Ha ingresado correctamente")
            return redirect('home')
        else:
            messages.success(request, "Hubo un error, por favor revise la informacion")
            return redirect('home')
    else:
        return render(request, 'home.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "Ha salido. Lo esperamos nuevamente pronto!")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        parkerform = FormularioRegistroUsuarios(request.POST)
        if parkerform.is_valid():
            parkerform.save()
            # autenticar y loguear
            username = parkerform.cleaned_data['username']
            password = parkerform.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Se ha registrado exitosamente!")
            return redirect('empleado')
    else:
        parkerform = FormularioRegistroUsuarios()
        return render(request, 'register.html', {'form':parkerform})
    return render(request, 'register.html', {'form':parkerform})

def aportes_empleado(request):
    context = {}
    if request.method == 'POST':
        form_aportes_empleado = FormularioAportesEmpleado(request.POST)
        if form_aportes_empleado.is_valid():
            aportes_empleado = form_aportes_empleado.save()
            context['aportes_empleado'] = aportes_empleado
            form_aportes_empleado = FormularioAportesEmpleado()
    else:
        form_aportes_empleado = FormularioAportesEmpleado()
    context['form'] = form_aportes_empleado
    return render(request, 'empleado.html', context)

def historico(request):
    context = {}
    empleados = CalculoAportes.objects.all().order_by('-created_at')
    context['empleados'] = empleados
    return render(request, 'historico.html', context)

def empleado(request, id):
    empleado = CalculoAportes.objects.get(id=id)
    context = {'empleado': empleado}
    return render(request, 'empleado.html', context)

def exportar_a_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="aportes.csv"'

    writer = csv.writer(response)
    writer.writerow([
                    'Usuario',
                    'Fecha Creacion',
                    'Nombre y Apellido',
                    'Salario Base',
                    'Bonificación',
                    'Asignación',
                    'Base Imponible',
                    'Pago AFAP',
                    'Pago Fonasa'])  # Encabezados de columna

    # Traigo los datos del modelo y los itero
    datos = CalculoAportes.objects.all()

    for dato_for in datos:
        nombre_completo = f"{dato_for.nombre_empleado} {dato_for.apellido_empleado}"
        user = request.user
        username = user.username # Ahora 'username' contiene el nombre de usuario
        writer.writerow(
                        username,
                        dato_for.created_at,
                        nombre_completo,
                        dato_for.salario_base,
                        dato_for.bonifica(),
                        dato_for.asigna(),
                        dato_for.base_imponible(),
                        dato_for.pago_afap(),
                        dato_for.pago_fonasa()
                        )  # Datos que van a ir en cada fila
    return response