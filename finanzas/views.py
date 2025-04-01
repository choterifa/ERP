# from django.shortcuts import render
# from .models import Ingreso, Egreso
# from django.contrib.auth.decorators import login_required

# @login_required
# def lista_ingresos(request):
#     ingresos = Ingreso.objects.filter(usuario=request.user).order_by('-fecha')
#     return render(request, 'finanzas/lista_ingresos.html', {'ingresos': ingresos})

# @login_required
# def lista_egresos(request):
#     egresos = Egreso.objects.filter(usuario=request.user).order_by('-fecha')
#     return render(request, 'finanzas/lista_egresos.html', {'egresos': egresos})
# # Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Ingreso, Egreso
from .forms import IngresoForm, EgresoForm
from datetime import datetime


@login_required
def lista_ingresos(request):
    ingresos = Ingreso.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'finanzas/lista_ingresos.html', {'ingresos': ingresos})

@login_required
def lista_egresos(request):
    egresos = Egreso.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'finanzas/lista_egresos.html', {'egresos': egresos})

@login_required
def crear_ingreso(request):
    if request.method == 'POST':
        form = IngresoForm(request.POST)
        if form.is_valid():
            ingreso = form.save(commit=False)
            ingreso.usuario = request.user
            ingreso.save()
            return redirect('lista_ingresos')
    else:
        form = IngresoForm()
    return render(request, 'finanzas/ingreso_form.html', {'form': form})

@login_required
def editar_ingreso(request, pk):
    ingreso = get_object_or_404(Ingreso, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = IngresoForm(request.POST, instance=ingreso)
        if form.is_valid():
            form.save()
            return redirect('lista_ingresos')
    else:
        form = IngresoForm(instance=ingreso)
    return render(request, 'finanzas/ingreso_form.html', {'form': form})

@login_required
def eliminar_ingreso(request, pk):
    ingreso = get_object_or_404(Ingreso, pk=pk, usuario=request.user)
    if request.method == 'POST':
        ingreso.delete()
        return redirect('lista_ingresos')
    return render(request, 'finanzas/confirmar_eliminar_ingreso.html', {'ingreso': ingreso})

# Vistas para egresos (similares a las de ingresos)
@login_required
def crear_egreso(request):
    if request.method == 'POST':
        form = EgresoForm(request.POST)
        if form.is_valid():
            egreso = form.save(commit=False)
            egreso.usuario = request.user
            egreso.save()
            return redirect('lista_egresos')
    else:
        form = EgresoForm()
    return render(request, 'finanzas/egreso_form.html', {'form': form})

@login_required
def editar_egreso(request, pk):
    egreso = get_object_or_404(Egreso, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = EgresoForm(request.POST, instance=egreso)
        if form.is_valid():
            form.save()
            return redirect('lista_egresos')
    else:
        form = EgresoForm(instance=egreso)
    return render(request, 'finanzas/egreso_form.html', {'form': form})

@login_required
def eliminar_egreso(request, pk):
    egreso = get_object_or_404(Egreso, pk=pk, usuario=request.user)
    if request.method == 'POST':
        egreso.delete()
        return redirect('lista_egresos')
    return render(request, 'finanzas/confirmar_eliminar_egreso.html', {'egreso': egreso})

@login_required
def resumen_finanzas(request):
    # Obtener parámetros de fecha del request
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    # Filtrar ingresos y egresos por usuario
    ingresos = Ingreso.objects.filter(usuario=request.user)
    egresos = Egreso.objects.filter(usuario=request.user)

     # Aplicar filtros de fecha si existen
    if fecha_inicio:
        try:
            # Convertir string a objeto date
            fecha_inicio_obj = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            ingresos = ingresos.filter(fecha__gte=fecha_inicio_obj)
            egresos = egresos.filter(fecha__gte=fecha_inicio_obj)
        except ValueError:
            # Manejar error si la fecha no tiene formato correcto
            pass
    
    if fecha_fin:
        try:
            fecha_fin_obj = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            ingresos = ingresos.filter(fecha__lte=fecha_fin_obj)
            egresos = egresos.filter(fecha__lte=fecha_fin_obj)
        except ValueError:
            pass

    # Calcular totales (manteniendo tu enfoque actual)
    ingresos_totales = sum(ingreso.monto for ingreso in ingresos)
    egresos_totales = sum(egreso.monto for egreso in egresos)
    saldo = ingresos_totales - egresos_totales    
    
    # # Calcular el total de ingresos
    # ingresos_totales = sum(ingreso.monto for ingreso in Ingreso.objects.filter(usuario=request.user))

    # # Calcular el total de egresos
    # egresos_totales = sum(egreso.monto for egreso in Egreso.objects.filter(usuario=request.user))

    # # Calcular el saldo
    # saldo = ingresos_totales - egresos_totales

    # Pasar los datos a la plantilla
    context = {
        'ingresos_totales': ingresos_totales,
        'egresos_totales': egresos_totales,
        'saldo': saldo,
        'fecha_inicio': fecha_inicio,  # Para mantener el valor en el formulario
        'fecha_fin': fecha_fin,        # Para mantener el valor en el formulario
    }
    return render(request, 'finanzas/resumen.html', context)


