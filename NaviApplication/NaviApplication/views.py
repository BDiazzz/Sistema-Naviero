from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout

from django.http import Http404

def login_general(request):
    if request.path != '/login/':
        raise Http404("Ruta no válida")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if hasattr(user, 'gestorrecursos'):
                return redirect('dashboard')
            elif user.is_superuser:
                return redirect('gestionar_navios')

            return redirect('login_general')

        return render(request, "login.html", {"error": "Credenciales inválidas"})
    
    return render(request, "login.html")

def handdling_404(request, exception):
    return render(request, '404.html', status=404)