import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .choices import TIPO_SUBTIPO_MAP
from .models import GestorRecursos, Recurso
from .forms import PerfilForm, RecursoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.db.models import Q

#Registro de usuario Recursos
def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono', 'Sin telefono')
        direccion = request.POST.get('direccion', 'Sin direccion')
        descripcion = request.POST.get('descripcion', 'Sin descripcion')

        if not username or not password or not correo:
            return render(request, 'registro.html', {'error': 'campos username, password y correo son obligatorios'})    
        
        if User.objects.filter(username=username).exists():
            return render(request, 'registro.html', {'error': 'El nombre de usuario ya existe'})

        user = User.objects.create_user(username=username, password=password)
        GestorRecursos.objects.create(user=user,correo=correo,telefono=telefono,direccion=direccion,descripcion=descripcion)
        return redirect('login_general')  # Redirige al login general después del registro
    return render(request, 'registro.html')

#ya no sirve pero dejalo ahi por si acaso es mejor el actual
"""""
#Login de usuario Recursos
def login_recurso(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')
"""

@login_required
def dashboard(request):
    if request.user.is_authenticated:
        gestor = request.user.gestorrecursos
        recursos_list = gestor.recurso_set.all()

        search_query = request.GET.get('search', '').strip()
        if search_query:
            # Intentar convertir a entero para filtrar por id
            try:
                search_id = int(search_query)
            except ValueError:
                search_id = None
            
            filtros = Q(nombre__icontains=search_query) | Q(tipo__icontains=search_query)
            if search_id is not None:
                filtros |= Q(id=search_id)

            recursos_list = recursos_list.filter(filtros)
        
        paginator = Paginator(recursos_list, 9)
        page_number = request.GET.get('page')
        recursos = paginator.get_page(page_number)

        return render(request, 'dashboard.html', {'recursos': recursos, 'gestor': gestor, 'search_query': search_query})
    else:
        return redirect('login_general')



#Crear un Recurso nuevo
@login_required
def registrar_recurso(request):
    if request.method == 'POST':
        form = RecursoForm(request.POST, request.FILES)
        if form.is_valid():
            recurso = form.save(commit=False)
            recurso.gestor = request.user.gestorrecursos
            recurso.save()
            form.save_m2m()
            return redirect('dashboard')
    else:
        form = RecursoForm()

    # Pasar el mapa al template
    contexto = {
        'form': form,
        'gestor': request.user.gestorrecursos,
        'tipo_subtipo_map': json.dumps(TIPO_SUBTIPO_MAP)
    }
    return render(request, 'crear-recurso.html', contexto)
    

@login_required
def editar_recurso(request, recurso_id):
    recurso = get_object_or_404(Recurso, id=recurso_id, gestor=request.user.gestorrecursos)

    if request.method == 'POST':
        form = RecursoForm(request.POST, request.FILES, instance=recurso)
        if form.is_valid():
            recurso = form.save(commit=False)
            recurso.gestor = request.user.gestorrecursos
            recurso.save()
            form.save_m2m()
            return redirect('dashboard')
    else:
        form = RecursoForm(instance=recurso)

    contexto = {
        'form': form,
        'gestor': request.user.gestorrecursos,
        'tipo_subtipo_map': json.dumps(TIPO_SUBTIPO_MAP),
        'modo_edicion': True  # útil para cambiar el título del formulario si deseas
    }
    return render(request, 'crear-recurso.html', contexto)

    
#Deslogearse
@login_required
def logout_GestorRecursos(request):
    logout(request)
    return redirect('login_general')


#Editar Perfil
@login_required
def editar_perfil(request):
    gestor = request.user.gestorrecursos
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=gestor)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PerfilForm(instance=gestor)

    return render(request, 'editar_perfil.html', {'form': form})


#test bryan esto te trae todo alemnos en json para que proves trae el provedor su recursos con su categorias y los puertos en los que oferta
#si ves algun subtipo vacio o recurso si puertos es porque estaba probando antes de crearlos por eso estan asi no te preocupes por eso
def lista_gestores_recursos_json(request):
    gestores = GestorRecursos.objects.all().prefetch_related('recurso_set__puertos_disponibles')
    data = []

    for gestor in gestores:
        recursos = []
        for recurso in gestor.recurso_set.all():
            recursos.append({
                'nombre': recurso.nombre,
                'precio': str(recurso.precio),
                'descripcion': recurso.descripcion,
                'puertos_disponibles': [p.nombre for p in recurso.puertos_disponibles.all()],
                'tipo': recurso.tipo,
                'subtipo': recurso.subtipo,
            })

        data.append({
            'gestor': gestor.user.username,
            'telefono': gestor.telefono,
            'recursos': recursos,
        })

    return JsonResponse(data, safe=False)


from django.http import JsonResponse

def lista_gestores_recursos_separados_json(request):
    gestores = GestorRecursos.objects.all().prefetch_related('recurso_set__puertos_disponibles')

    servicios = []
    no_servicios = []

    for gestor in gestores:
        recursos_servicios = []
        recursos_no_servicios = []

        for recurso in gestor.recurso_set.all():
            recurso_data = {
                'nombre': recurso.nombre,
                'precio': str(recurso.precio),
                'descripcion': recurso.descripcion,
                'puertos_disponibles': [p.nombre for p in recurso.puertos_disponibles.all()],
                'tipo': recurso.tipo,
                'subtipo': recurso.subtipo,
            }

            # Validación de None antes de startswith
            if (recurso.tipo and recurso.tipo.startswith("Servicio")) or (recurso.subtipo and recurso.subtipo.startswith("Servicio")):
                recursos_servicios.append(recurso_data)
            else:
                recursos_no_servicios.append(recurso_data)

        if recursos_servicios:
            servicios.append({
                'gestor': gestor.user.username,
                'telefono': gestor.telefono,
                'recursos': recursos_servicios,
            })

        if recursos_no_servicios:
            no_servicios.append({
                'gestor': gestor.user.username,
                'telefono': gestor.telefono,
                'recursos': recursos_no_servicios,
            })

    return JsonResponse({
        'servicios': servicios,
        'no_servicios': no_servicios,
    }, safe=False)


# Eliminar recurso
@login_required
def eliminar_recurso(request, recurso_id):
    recurso = get_object_or_404(Recurso, id=recurso_id, gestor=request.user.gestorrecursos)

    if request.method == 'POST':
        recurso.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@login_required
def detalles_recurso(request, recurso_id):
    recurso = get_object_or_404(Recurso, id=recurso_id, gestor=request.user.gestorrecursos)
    puertos = recurso.puertos_disponibles.all()
    data = {
        'nombre': recurso.nombre,
        'descripcion': recurso.descripcion,
        'precio': str(recurso.precio),
        'tipo': recurso.tipo,
        'subtipo': recurso.subtipo,
        'puertos': [puerto.nombre for puerto in puertos],
    }
    return JsonResponse(data)