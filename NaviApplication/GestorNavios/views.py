from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Navio, Puerto
from django.db.models import CharField
from django.db.models.functions import Cast
from .forms import NavioForm
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from NaviApplication.views import login_general
from GestorRecursos.models import Recurso, GestorRecursos
from .models import Navio, Escala, EscalaPuerto, AsignacionRecursos
from django.db.models import Count
from django.http import HttpResponse, HttpResponseForbidden
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from decimal import Decimal
from django.db.models import Exists, OuterRef
from django.db.models import CharField
from django.db.models.functions import Cast
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.db.models import Max
from django.utils import timezone
from django.db.models import Max, Min
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from django.core.paginator import Paginator

"""""
#Login de Navios
def login_navios(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user and user.is_superuser:
            login(request,user)
            return render (request,"gestionarNavios.html")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")
"""
@login_required 
def get_escalas_con_recursos(request, navio_id):
    # Obtener escalas del navío que tienen al menos un recurso asignado
    escalas = Escala.objects.filter(
        navio_id=navio_id,
        escalapuerto__asignacionrecursos__isnull=False
    ).distinct().values('id', 'nombre')

    return JsonResponse({
        'escalas': list(escalas)
    })

@login_required
def gestionar_navios(request):
    alerta = request.session.pop('alerta', None)
    query = request.GET.get('q', "").strip()

    # Subconsulta para verificar si el navío tiene escalas con recursos asignados
    tiene_recursos = Exists(
        AsignacionRecursos.objects.filter(
            escala_puerto__escala__navio=OuterRef('pk')
        )
    )

    if query:
        navios = Navio.objects.annotate(
            imo_str=Cast('imoNumero', CharField()),
            tiene_recursos=tiene_recursos
        ).filter(imo_str__startswith=query)
    else:
        navios = Navio.objects.annotate(
            tiene_recursos=tiene_recursos
        )

    return render(request, "gestionarNavios.html", {
        'navios': navios,
        'busqueda': query,
        'alerta': alerta  
    })



@login_required
def crear_editar_navio(request, navio_id=None):
    if navio_id:
        navio = get_object_or_404(Navio, id=navio_id)
        accion = "Editar"
    else:
        navio = None
        accion = "Crear"

    if request.method == 'POST':
        form = NavioForm(request.POST, instance=navio)
        if form.is_valid():
            form.save()
            # Establecer alerta de éxito
            mensaje = "Navío actualizado correctamente" if navio_id else "Navío creado correctamente"
            request.session['alerta'] = {
                'tipo': 'success',
                'mensaje': mensaje
            }
            return redirect('gestionar_navios')
    else:
        form = NavioForm(instance=navio)

    return render(request, 'crearEditarNavio.html', {
        'form': form,
        'accion': accion,
        'navio': navio, 
    })


@login_required
@require_POST
def eliminar_navio(request, navio_id):
    navio = get_object_or_404(Navio, id=navio_id)

    if navio.escala_set.exists():
        # Usar el sistema de alertas para mostrar el error
        request.session['alerta'] = {
            'tipo': 'error',
            'mensaje': 'No se puede eliminar navíos con escalas asignadas'
        }
        return redirect(reverse('editar_navio', args=[navio_id]))

    navio.delete()
    # Alerta de éxito al eliminar
    request.session['alerta'] = {
        'tipo': 'success',
        'mensaje': 'Navío eliminado correctamente'
    }
    return redirect(reverse('gestionar_navios'))


@login_required
def gestionar_recursos(request, escala_id):
    # Obtener la escala y sus puertos
    escala = get_object_or_404(Escala, id=escala_id)
    puertos_escala = EscalaPuerto.objects.filter(escala=escala).select_related('puerto')
    
    # Obtener todos los recursos disponibles agrupados por puerto
    recursos_por_puerto = {}
    for ep in puertos_escala:
        recursos = Recurso.objects.filter(
            puertos_disponibles=ep.puerto
        ).select_related('gestor__user').prefetch_related('puertos_disponibles')
        
        # Organizar por tipo principal (Productos/Servicios), luego por subtipo
        recursos_organizados = {
            'productos': {},  # Aquí guardaremos {tipo_principal: {subtipo: [recursos]}}
            'servicios': {}
        }
        
        for recurso in recursos:
            # Determinar si es producto o servicio
            es_servicio = recurso.tipo.lower().startswith('servicio')
            categoria = 'servicios' if es_servicio else 'productos'
            
            # Obtener el tipo principal (eliminando 'Servicio ' si es necesario)
            tipo_principal = recurso.tipo.replace('Servicio ', '') if es_servicio else recurso.tipo
            
            # Si no hay subtipo, usar "General"
            subtipo = recurso.subtipo if recurso.subtipo else "General"
            
            # Inicializar estructura si no existe
            if tipo_principal not in recursos_organizados[categoria]:
                recursos_organizados[categoria][tipo_principal] = {}
            
            if subtipo not in recursos_organizados[categoria][tipo_principal]:
                recursos_organizados[categoria][tipo_principal][subtipo] = []
                
            recursos_organizados[categoria][tipo_principal][subtipo].append({
                'id': recurso.id,
                'nombre': recurso.nombre,
                'precio': recurso.precio,
                'descripcion': recurso.descripcion,
                'proveedor': recurso.gestor.user.get_full_name() or recurso.gestor.user.username,
                'gestor_id': recurso.gestor.id,
                'imagen_url': recurso.imagen.url if recurso.imagen else None
            })
        
        recursos_por_puerto[ep] = recursos_organizados
    
    context = {
        'escala': escala,
        'recursos_por_puerto': recursos_por_puerto,
        'navio': escala.navio
    }
    
    return render(request, 'gestionarRecursos.html', context)


@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect(reverse('login_general'))

@login_required
def escalas_sin_recursos(request, navio_id=None):
    # Obtener todas las escalas que no tienen asignaciones de recursos
    escalas_con_puertos = Escala.objects.annotate(
        num_puertos=Count('escalapuerto')
    ).filter(num_puertos__gt=0)
    # Si se proporciona un navio_id, filtrar por ese navío
    if navio_id:
        navio = get_object_or_404(Navio, id=navio_id)
        escalas_con_puertos = escalas_con_puertos.filter(navio=navio)
    
    # Filtrar escalas sin recursos
    escalas_sin_recursos = []
    for escala in escalas_con_puertos:
        tiene_recursos = AsignacionRecursos.objects.filter(
            escala_puerto__escala=escala
        ).exists()
        
        if not tiene_recursos:
            escalas_sin_recursos.append(escala)
    
    context = {
        'escalas': escalas_sin_recursos,
        'navio_filtrado': Navio.objects.get(id=navio_id) if navio_id else None
    }
    
    return render(request, 'escalasSinRecursos.html', context)


# Asignación de recursos a escalas
@login_required
def confirmar_asignacion(request, escala_id):
    escala = get_object_or_404(Escala, id=escala_id)
    
    # Validación adicional: Verificar si la escala ya tiene recursos asignados
    if AsignacionRecursos.objects.filter(escala_puerto__escala=escala).exists():
        messages.error(request, 'Esta escala ya tiene recursos asignados. No se pueden asignar más.')
        return redirect('escalas_sin_recursos')
    
    if request.method == 'POST':
        puertos_escala = EscalaPuerto.objects.filter(escala=escala)
        
        # Verificar que al menos se esté asignando un recurso
        recursos_asignados = False
        
        # Procesar productos
        for ep in puertos_escala:
            productos = request.POST.getlist(f'productos[{ep.id}][recurso]')
            cantidades = request.POST.getlist(f'productos[{ep.id}][cantidad]')
            for recurso_id, cantidad in zip(productos, cantidades):
                if cantidad.isdigit() and int(cantidad) > 0:
                    recursos_asignados = True
                    recurso = get_object_or_404(Recurso, id=recurso_id)
                    AsignacionRecursos.objects.create(
                        escala_puerto=ep,
                        recurso=recurso,
                        cantidad=int(cantidad)
                    )
        
        # Procesar servicios
        for ep in puertos_escala:
            servicio_id = request.POST.get(f'servicios[{ep.id}][recurso]')
            if servicio_id and servicio_id != "0":
                recursos_asignados = True
                recurso = get_object_or_404(Recurso, id=servicio_id)
                AsignacionRecursos.objects.create(
                    escala_puerto=ep,
                    recurso=recurso,
                    cantidad=1
                )
        
        if recursos_asignados:
            messages.success(request, 'Recursos asignados exitosamente.')
            if escala.navio:  # Verificar que la escala tenga un navío asociado
                escala.navio.estado = 'completo'
                escala.navio.save()
        else:
              # Usar el sistema de alertas para mostrar el error
            messages.warning(request, 'No se asignaron recursos. Por favor, seleccione al menos un recurso.')
            return redirect(reverse('gestionar_recursos', args=[escala_id]))
        
        return redirect('escalas_sin_recursos')
    
    return redirect('escalas_sin_recursos')


# creacion de escalas
def make_aware_if_naive(dt):
    if dt and timezone.is_naive(dt):
        return timezone.make_aware(dt, timezone.get_current_timezone())
    return dt

@login_required
def gestionar_escala(request, navio_id):
    navio = get_object_or_404(Navio, id=navio_id)
    puertos = Puerto.objects.all()
    escalas_existentes = Escala.objects.filter(navio=navio)


    if request.method == "POST":
        escala_nombre = request.POST.get("escala_nombre")
        puertos_ids = request.POST.getlist("puertos[]")
        fechas_arribo = request.POST.getlist("fechas_arribo[]")
        fechas_zarpe = request.POST.getlist("fechas_zarpe[]")
        errores = False

        # Validación de fecha global de la nueva escala respecto a escalas anteriores del mismo navío
        ultima_fecha_zarpe_existente = EscalaPuerto.objects.filter(
            escala__navio=navio
        ).aggregate(max_fecha_zarpe=Max('fecha_zarpe'))['max_fecha_zarpe']

        if ultima_fecha_zarpe_existente:
            fechas_arribo_dt = [make_aware_if_naive(parse_datetime(f)) for f in fechas_arribo if parse_datetime(f) is not None]
            if fechas_arribo_dt:
                fecha_min_arribo_nueva = min(fechas_arribo_dt)
                if fecha_min_arribo_nueva <= ultima_fecha_zarpe_existente:
                    messages.error(request, (
                        f"La nueva escala debe tener fechas de arribo posteriores al zarpe de la última escala existente "
                        f"({ultima_fecha_zarpe_existente.strftime('%d %b %Y %H:%M')})."
                    ))
                    errores = True


        puertos_usados = set()
        escala_puertos_validos = []
        ultima_fecha_zarpe = None

        for puerto_id, fecha_arribo, fecha_zarpe in zip(puertos_ids, fechas_arribo, fechas_zarpe):
            fecha_arribo_dt = make_aware_if_naive(parse_datetime(fecha_arribo))
            fecha_zarpe_dt = make_aware_if_naive(parse_datetime(fecha_zarpe))
            puerto = Puerto.objects.get(id=puerto_id)
            puerto_nombre = puerto.nombre

            if puerto_id in puertos_usados:
                messages.error(request, f"Error: El puerto {puerto_nombre} ya fue asignado dentro de esta escala.")
                errores = True
                continue
            puertos_usados.add(puerto_id)

            if not fecha_arribo_dt or not fecha_zarpe_dt or fecha_arribo_dt >= fecha_zarpe_dt:
                messages.error(request, f"Error: Fecha inválida para el puerto {puerto_nombre}. Arribo debe ser antes que zarpe.")
                errores = True
                continue

            if ultima_fecha_zarpe and fecha_arribo_dt < ultima_fecha_zarpe:
                messages.error(request, f"Error: El arribo a {puerto_nombre} debe ser posterior al zarpe del puerto anterior.")
                errores = True
                continue

            conflictos = EscalaPuerto.objects.filter(
                escala__navio=navio,
                puerto_id=puerto_id,
                fecha_arribo__lt=fecha_zarpe_dt,
                fecha_zarpe__gt=fecha_arribo_dt
            )

            if conflictos.exists():
                messages.error(request, f"Conflicto: El puerto {puerto_nombre} ya está ocupado en esas fechas.")
                errores = True
                continue

            escala_puertos_validos.append({
                "puerto": puerto,
                "fecha_arribo": fecha_arribo_dt,
                "fecha_zarpe": fecha_zarpe_dt
            })
            ultima_fecha_zarpe = fecha_zarpe_dt

        # Si no hubo errores, crear escala y asignaciones
        if not errores and escala_puertos_validos:
            escala = Escala.objects.create(nombre=escala_nombre, navio=navio)
            for datos in escala_puertos_validos:
                EscalaPuerto.objects.create(
                    escala=escala,
                    puerto=datos["puerto"],
                    fecha_arribo=datos["fecha_arribo"],
                    fecha_zarpe=datos["fecha_zarpe"]
                )
                messages.success(request, f"Puerto {datos['puerto'].nombre} asignado correctamente.")

            return redirect('/navios/EscalasSinRecursos/')
        elif not escala_puertos_validos:
            messages.error(request, "Error: No se pudo registrar ningún puerto porque todas las asignaciones fallaron.")
        else:
            messages.error(request, "La escala no se guardó porque una o más asignaciones son inválidas.")

    return render(request, "gestionar_escala.html", {
        "navio": navio,
        "puertos": puertos,
        "escalas_existentes": escalas_existentes
    })


def generar_presupuesto_pdf(request, escala_id):
    try:
        escala = Escala.objects.get(id=escala_id)
    except Escala.DoesNotExist:
        return HttpResponse("Escala no encontrada", status=404)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=presupuesto_escala_{escala_id}.pdf'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    y = height - inch

    p.setFont("Helvetica-Bold", 16)
    p.drawString(inch, y, f"Presupuesto de Escala: {escala.nombre}")
    y -= 0.4 * inch
    p.setFont("Helvetica", 12)
    p.drawString(inch, y, f"Navío: {escala.navio.nombre}")
    y -= 0.4 * inch

    total_general = Decimal("0.00")

    for escala_puerto in escala.escalapuerto_set.all():
        asignaciones = AsignacionRecursos.objects.filter(escala_puerto=escala_puerto)
        if not asignaciones.exists():
            continue

        p.setFont("Helvetica-Bold", 13)
        p.drawString(inch, y, f"Puerto: {escala_puerto.puerto.nombre}")
        y -= 0.3 * inch

        subtotal_puerto = Decimal("0.00")

        # Coordenadas X para las columnas
        x_recurso = inch
        x_proveedor = x_recurso + 75
        x_cantidad= x_proveedor + 115
        x_precio = x_cantidad + 70
        
        # Encabezados
        p.setFont("Helvetica-Bold", 11)
        p.drawString(x_recurso, y, "Recurso")
        p.drawString(x_proveedor, y, "Proveedor")
        p.drawString(x_cantidad, y, "Cantidad")
        p.drawString(x_precio, y, "Precio")
        y -= 0.2 * inch
        p.setFont("Helvetica", 11)
        
        # Filas de datos
        for asignacion in asignaciones:
            recurso = asignacion.recurso
            cantidad = asignacion.cantidad
            precio = recurso.precio
            proveedor = recurso.gestor.user.username
            subtotal = cantidad * precio
            subtotal_puerto += subtotal
        
            p.drawString(x_recurso, y, recurso.nombre[:20])
            p.drawString(x_proveedor, y, proveedor[:20])
            p.drawString(x_cantidad, y, str(cantidad))
            p.drawString(x_precio, y, f"${precio:.2f}")
            y -= 0.2 * inch
        
            if y < inch:  # Salto de página si nos quedamos sin espacio
                p.showPage()
                y = height - inch

        # Fuera del bucle de asignaciones - subtotal del puerto
        p.setFont("Helvetica-Bold", 11)
        p.drawString(inch, y, f"Subtotal del puerto: ${subtotal_puerto:.2f}")
        total_general += subtotal_puerto
        y -= 0.4 * inch

        if y < inch:  # Salto de página después del subtotal si es necesario
            p.showPage()
            y = height - inch

    # Total general (asegurando que haya espacio)
    if y < 0.5 * inch:  # Si queda poco espacio, nueva página
        p.showPage()
        y = height - inch
    
    p.setFont("Helvetica-Bold", 14)
    p.drawString(inch, y, f"TOTAL GENERAL: ${total_general:.2f}")
    p.showPage()
    p.save()

    return response


@login_required
def editar_escala(request, escala_id):

    escala = get_object_or_404(Escala, id=escala_id)
    puertos = Puerto.objects.all()

    if request.method == "POST":
        escala_nombre = request.POST.get("escala_nombre")
        puertos_ids = request.POST.getlist("puertos[]")
        fechas_arribo = request.POST.getlist("fechas_arribo[]")
        fechas_zarpe = request.POST.getlist("fechas_zarpe[]")

        errores = False
        puertos_usados = set()
        escala_puertos_validos = []
        ultima_fecha_zarpe = None

        min_fecha_arribo_escala_actual = EscalaPuerto.objects.filter(escala=escala).aggregate(min_fecha=Min('fecha_arribo'))['min_fecha']

        otras_escalas = Escala.objects.filter(navio=escala.navio).exclude(id=escala.id)
        escala_posterior = None
        escala_anterior = None

        for e in otras_escalas:
            e_fecha_arribo = EscalaPuerto.objects.filter(escala=e).aggregate(f=Min('fecha_arribo'))['f']
            if e_fecha_arribo and e_fecha_arribo > min_fecha_arribo_escala_actual:
                if not escala_posterior or e_fecha_arribo < EscalaPuerto.objects.filter(escala=escala_posterior).aggregate(f=Min('fecha_arribo'))['f']:
                    escala_posterior = e
            elif e_fecha_arribo and e_fecha_arribo < min_fecha_arribo_escala_actual:
                if not escala_anterior or e_fecha_arribo > EscalaPuerto.objects.filter(escala=escala_anterior).aggregate(f=Min('fecha_arribo'))['f']:
                    escala_anterior = e

        fecha_limite_superior = None
        if escala_posterior:
            fecha_limite_superior = EscalaPuerto.objects.filter(escala=escala_posterior).aggregate(f=Min('fecha_arribo'))['f']

        fecha_limite_inferior = None
        if escala_anterior:
            fecha_limite_inferior = EscalaPuerto.objects.filter(escala=escala_anterior).aggregate(f=Max('fecha_zarpe'))['f']

        for puerto_id, fecha_arribo, fecha_zarpe in zip(puertos_ids, fechas_arribo, fechas_zarpe):
            fecha_arribo_dt = parse_datetime(fecha_arribo)
            fecha_zarpe_dt = parse_datetime(fecha_zarpe)
            if fecha_arribo_dt and fecha_arribo_dt.tzinfo is None:
                fecha_arribo_dt = make_aware(fecha_arribo_dt)
            if fecha_zarpe_dt and fecha_zarpe_dt.tzinfo is None:
                fecha_zarpe_dt = make_aware(fecha_zarpe_dt)

            try:
                puerto = Puerto.objects.get(id=puerto_id)
            except Puerto.DoesNotExist:
                messages.error(request, f"Puerto no encontrado con ID {puerto_id}.")
                errores = True
                continue

            if puerto_id in puertos_usados:
                messages.error(request, f"Error: El puerto {puerto.nombre} ya fue asignado dentro de esta escala.")
                errores = True
                continue
            puertos_usados.add(puerto_id)

            if not fecha_arribo_dt or not fecha_zarpe_dt or fecha_arribo_dt >= fecha_zarpe_dt:
                messages.error(request, f"Error: Fecha inválida para el puerto {puerto.nombre}. Arribo debe ser antes que zarpe.")
                errores = True
                continue

            if ultima_fecha_zarpe and fecha_arribo_dt < ultima_fecha_zarpe:
                messages.error(request, f"Error: El arribo a {puerto.nombre} debe ser posterior al zarpe del puerto anterior.")
                errores = True
                continue

            mensajes_error = []
            if fecha_limite_superior and (fecha_arribo_dt >= fecha_limite_superior or fecha_zarpe_dt >= fecha_limite_superior):
                mensajes_error.append(f"anterior a la fecha de arribo de la siguiente escala ({fecha_limite_superior.strftime('%d %b %Y %H:%M')})")
            if fecha_limite_inferior and (fecha_arribo_dt <= fecha_limite_inferior or fecha_zarpe_dt <= fecha_limite_inferior):
                mensajes_error.append(f"mayor a la de zarpe de la última escala ({fecha_limite_inferior.strftime('%d %b %Y %H:%M')})")

            if mensajes_error:
                mensajes = " y ".join(mensajes_error)
                messages.error(request, f"La fecha {fecha_arribo_dt.strftime('%d %b %Y %H:%M')} - {fecha_zarpe_dt.strftime('%d %b %Y %H:%M')} debe ser {mensajes}.")
                errores = True
                continue

            conflictos = EscalaPuerto.objects.filter(
                escala__navio=escala.navio,
                puerto_id=puerto_id,
                fecha_arribo__lt=fecha_zarpe_dt,
                fecha_zarpe__gt=fecha_arribo_dt
            ).exclude(escala=escala)

            if conflictos.exists():
                messages.error(request, f"Conflicto: El puerto {puerto.nombre} ya está ocupado en esas fechas.")
                errores = True
                continue

            escala_puertos_validos.append({
                "puerto": puerto,
                "fecha_arribo": fecha_arribo_dt,
                "fecha_zarpe": fecha_zarpe_dt
            })
            ultima_fecha_zarpe = fecha_zarpe_dt

        if not errores and escala_puertos_validos:
            escala.nombre = escala_nombre
            escala.save()

            EscalaPuerto.objects.filter(escala=escala).delete()

            for datos in escala_puertos_validos:
                EscalaPuerto.objects.create(
                    escala=escala,
                    puerto=datos["puerto"],
                    fecha_arribo=datos["fecha_arribo"],
                    fecha_zarpe=datos["fecha_zarpe"]
                )
                messages.success(request, f"Puerto {datos['puerto'].nombre} asignado correctamente.")

            return redirect('/navios/EscalasSinRecursos/')
        elif not escala_puertos_validos:
            messages.error(request, "Error: No se pudo registrar ningún puerto porque todas las asignaciones fallaron.")
        else:
            messages.error(request, "La escala no se guardó porque una o más asignaciones son inválidas.")

    context = {
        'escala': escala,
        'escalapuertos': EscalaPuerto.objects.filter(escala=escala).order_by('fecha_arribo'),
        'puertos': puertos
    }
    return render(request, 'editarEscala.html', context)


@login_required
def eliminar_escala(request, escala_id):
    escala = get_object_or_404(Escala, id=escala_id)
    navio = escala.navio  # Guardamos el navío antes de borrar la escala
    
    if request.method == 'POST':
        escala.delete()

        # Verificar si el navío tiene más escalas
        tiene_escalas = Escala.objects.filter(navio=navio).exists()
        if not tiene_escalas:
            navio.estado = 'inactivo'
            navio.save()

        return redirect('escalas_con_recursos')
    
    return HttpResponseForbidden("Método no permitido")


@login_required
def escalas_con_recursos(request):
    # Obtener todos los navíos para el combo
    navios = Navio.objects.all()

    navio_id = request.GET.get('navio')  # Recibo navio por query param
    escalas = Escala.objects.all().prefetch_related(
        'escalapuerto_set__asignacionrecursos_set',
        'escalapuerto_set__puerto',
    ).select_related('navio')

    if navio_id and navio_id.isdigit():
        navio = get_object_or_404(Navio, id=navio_id)
        escalas = escalas.filter(navio=navio)
    else:
        navio = None


     # Calcular el total de cada recurso (cantidad * precio)
    for escala in escalas:
        for ep in escala.escalapuerto_set.all():
            for recurso in ep.asignacionrecursos_set.all():
                recurso.total = recurso.cantidad * recurso.recurso.precio

    # Filtrar solo las escalas con recursos
    escalas_filtradas = []
    for escala in escalas:
        for ep in escala.escalapuerto_set.all():
            if ep.asignacionrecursos_set.exists():
                escalas_filtradas.append(escala)
                break

    # Paginación, 9 escalas por página
    paginator = Paginator(escalas_filtradas, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'navios': navios,
        'escalas': page_obj,  # Aquí envío la página con las escalas
        'navio_filtrado': navio,
        'page_obj': page_obj,
    }
    return render(request, 'escalasConRecursos.html', context)