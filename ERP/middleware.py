# middleware.py

import time
# middleware.py

# from django.shortcuts import redirect

# class SessionTimeoutMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             last_activity = request.session.get('last_activity')
#             if last_activity and (time.time() - last_activity > request.session.get_expiry_age()):
#                 # Redirigir a la vista de cierre de sesión con un parámetro de consulta
#                 print("Middleware ejecutado")
#                 return redirect('usuarios:logout' + '?inactive=true')  # Usa un parámetro de consulta

#         # Actualizar el tiempo de la última actividad
#         request.session['last_activity'] = time.time()
#         return self.get_response(request)