from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cotizacion, Cliente, ItemCotizacion
from .forms import CotizacionForm, ClienteForm, ItemCotizacionFormSet

@login_required
def lista_cotizaciones(request):
    # Obtener todas las cotizaciones del usuario actual, ordenadas por fecha de emisión
    cotizaciones = Cotizacion.objects.filter(usuario=request.user).order_by('-fecha_emision')
    return render(request, 'cotizaciones/lista_cotizaciones.html', {'cotizaciones': cotizaciones})

@login_required
def detalle_cotizacion(request, cotizacion_id):
    # Obtener la cotización específica del usuario actual
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id, usuario=request.user)
    return render(request, 'cotizaciones/detalle_cotizacion.html', {'cotizacion': cotizacion})

# @login_required
# def crear_cotizacion(request):
#     if request.method == 'POST':
#         # Procesar el formulario de cotización y el formset de ítems
#         form = CotizacionForm(request.POST, usuario=request.user)
#         formset = ItemCotizacionFormSet(request.POST)
#         if form.is_valid() and formset.is_valid():
#             # Guardar la cotización
#             cotizacion = form.save(commit=False)
#             cotizacion.usuario = request.user
#             cotizacion.save()
#             # Guardar los ítems asociados a la cotización
#             formset.instance = cotizacion
#             formset.save()
#             # Calcular el total de la cotización
#             cotizacion.calcular_total()
#             return redirect('detalle_cotizacion', cotizacion.id)
#     else:
#         # Mostrar el formulario vacío para crear una nueva cotización
#         form = CotizacionForm(usuario=request.user)
#         formset = ItemCotizacionFormSet()
#     return render(request, 'cotizaciones/cotizacion_form.html', {
#         'form': form,
#         'formset': formset,
#     })

@login_required
def crear_cotizacion(request):
    if request.method == 'POST':
        form = CotizacionForm(request.POST, usuario=request.user)
        formset = ItemCotizacionFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            try:
                # Guardar la cotización sin los campos calculados
                cotizacion = form.save(commit=False)
                cotizacion.usuario = request.user

                # Guardar la cotización para obtener un ID
                cotizacion.save()

                # Asociar los ítems a la cotización y guardarlos
                formset.instance = cotizacion
                items = formset.save()  # Guardar los ítems y obtener la lista de objetos guardados

                # Calcular el subtotal sumando los ítems
                subtotal = sum(item.subtotal() for item in items)
                cotizacion.subtotal = subtotal

                # Calcular impuestos y descuentos en función de los porcentajes
                porcentaje_impuestos = form.cleaned_data.get('porcentaje_impuestos', 0)
                porcentaje_descuentos = form.cleaned_data.get('porcentaje_descuentos', 0)

                cotizacion.impuestos = (subtotal * porcentaje_impuestos) / 100
                cotizacion.descuentos = (subtotal * porcentaje_descuentos) / 100

                # Calcular el total
                cotizacion.total = subtotal + cotizacion.impuestos - cotizacion.descuentos

                # Guardar la cotización con los valores calculados
                cotizacion.save()

                return redirect('detalle_cotizacion', cotizacion.id)
            except Exception as e:
                print("Error al guardar la cotización:", str(e))  # Depuración
        else:
            print("Errores en el formulario:", form.errors)  # Depuración
            print("Errores en el formset:", formset.errors)  # Depuración
    else:
        form = CotizacionForm(usuario=request.user)
        formset = ItemCotizacionFormSet()
    return render(request, 'cotizaciones/cotizacion_form.html', {
        'form': form,
        'formset': formset,
    })

# @login_required
# def editar_cotizacion(request, cotizacion_id):
#     # Obtener la cotización específica del usuario actual
#     cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id, usuario=request.user)
#     if request.method == 'POST':
#         # Procesar el formulario de cotización y el formset de ítems
#         form = CotizacionForm(request.POST, instance=cotizacion, usuario=request.user)
#         formset = ItemCotizacionFormSet(request.POST, instance=cotizacion)
#         if form.is_valid() and formset.is_valid():
#             # Guardar la cotización y los ítems
#             form.save()
#             formset.save()
#             # Calcular el total de la cotización
#             cotizacion.calcular_total()
#             return redirect('detalle_cotizacion', cotizacion.id)
#     else:
#         # Mostrar el formulario con los datos actuales de la cotización
#         form = CotizacionForm(instance=cotizacion, usuario=request.user)
#         formset = ItemCotizacionFormSet(instance=cotizacion)
#     return render(request, 'cotizaciones/cotizacion_form.html', {
#         'form': form,
#         'formset': formset,
#     })

@login_required
def editar_cotizacion(request, cotizacion_id):
    # Obtener la cotización específica del usuario actual
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id, usuario=request.user)
    if request.method == 'POST':
        # Procesar el formulario de cotización y el formset de ítems
        form = CotizacionForm(request.POST, instance=cotizacion, usuario=request.user)
        formset = ItemCotizacionFormSet(request.POST, instance=cotizacion)
        if form.is_valid() and formset.is_valid():
            try:
                # Guardar la cotización sin los campos calculados
                cotizacion = form.save(commit=False)

                # Actualizar los porcentajes de impuestos y descuentos
                cotizacion.porcentaje_impuestos = form.cleaned_data.get('porcentaje_impuestos', 0)
                cotizacion.porcentaje_descuentos = form.cleaned_data.get('porcentaje_descuentos', 0)

                # Guardar los ítems asociados a la cotización
                formset.instance = cotizacion
                items = formset.save()  # Guardar los ítems y obtener la lista de objetos guardados
                
                # Depuración: Verificar los ítems guardados
                print("Ítems guardados:", items)

                  # Recalcular el subtotal usando TODOS los ítems de la cotización
                subtotal = sum(item.subtotal() for item in cotizacion.items.all())
                cotizacion.subtotal = subtotal

                # Calcular impuestos y descuentos en función de los porcentajes
                cotizacion.impuestos = (subtotal * cotizacion.porcentaje_impuestos) / 100
                cotizacion.descuentos = (subtotal * cotizacion.porcentaje_descuentos) / 100

                # Calcular el total
                cotizacion.total = subtotal + cotizacion.impuestos - cotizacion.descuentos

                # Guardar la cotización con los valores calculados
                cotizacion.save()

                return redirect('detalle_cotizacion', cotizacion.id)
            except Exception as e:
                print("Error al guardar la cotización:", str(e))  # Depuración
        else:
            print("Errores en el formulario:", form.errors)  # Depuración
            print("Errores en el formset:", formset.errors)  # Depuración
    else:
        # Mostrar el formulario con los datos actuales de la cotización
        form = CotizacionForm(instance=cotizacion, usuario=request.user)
       
        formset = ItemCotizacionFormSet(instance=cotizacion)
    return render(request, 'cotizaciones/cotizacion_form.html', {
        'form': form,
        'formset': formset,
    })


@login_required
def eliminar_cotizacion(request, cotizacion_id):
    # Obtener la cotización específica del usuario actual
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id, usuario=request.user)
    if request.method == 'POST':
        # Eliminar la cotización
        cotizacion.delete()
        return redirect('lista_cotizaciones')
    return render(request, 'cotizaciones/confirmar_eliminar_cotizacion.html', {'cotizacion': cotizacion})

@login_required
def lista_clientes(request):
    # Obtener todos los clientes
    clientes = Cliente.objects.all()
    return render(request, 'cotizaciones/lista_clientes.html', {'clientes': clientes})

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        # Procesar el formulario de cliente
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.usuario = request.user  # Asocia el cliente al usuario actual
            # Guardar el cliente
            form.save()
            return redirect('lista_clientes')
    else:
        # Mostrar el formulario vacío para crear un nuevo cliente
        form = ClienteForm()
    return render(request, 'cotizaciones/cliente_form.html', {'form': form})

@login_required
def editar_cliente(request, cliente_id):
    # Obtener el cliente específico
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        # Procesar el formulario de cliente
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            # Guardar los cambios del cliente
            form.save()
            return redirect('lista_clientes')
    else:
        # Mostrar el formulario con los datos actuales del cliente
        form = ClienteForm(instance=cliente)
    return render(request, 'cotizaciones/cliente_form.html', {'form': form})

@login_required
def eliminar_cliente(request, cliente_id):
    # Obtener el cliente específico
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        # Eliminar el cliente
        cliente.delete()
        return redirect('lista_clientes')
    return render(request, 'cotizaciones/confirmar_eliminar_cliente.html', {'cliente': cliente})
