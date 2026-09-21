from .models import Bitacora

def registrar_bitacora(request, accion, descripcion, modulo):
    usuario = "Sistema"

    if request.user.is_authenticated:
        usuario= request.user.username

    Bitacora.objects.create(
        usuario=usuario,
        accion=accion,
        descripcion=descripcion,
        modulo=modulo,
    )
