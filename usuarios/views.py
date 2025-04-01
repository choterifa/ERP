from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_view(request):
    # Verifica si el usuario ya está autenticado
    if request.user.is_authenticated:
        return redirect('resumen_finanzas')  # Redirige a la página de resumen de finanzas o a donde desees
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('resumen_finanzas') # Redirigir después del login
        else:
            return render(request, 'usuarios/login.html', {'error': 'Usuario o contraseña incorrectos'})

    return render(request, 'usuarios/login.html')

@login_required
def logout_view(request):
    # inactive = request.GET.get('inactive', False)  # Obtén el parámetro de consulta
    logout(request)
    
    # if inactive:
    #     messages.info(request, 'Tu sesión ha expirado por inactividad. Por favor, inicia sesión nuevamente.')
    return redirect('usuarios:login')




