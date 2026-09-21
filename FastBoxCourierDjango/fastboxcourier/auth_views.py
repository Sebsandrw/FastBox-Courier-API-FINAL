
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def login_usuario(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    mensaje = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        usuario = authenticate(request, username=username, password=password)

        if usuario:
            login(request, usuario)
            return redirect("dashboard")
        else:
            mensaje = "Usuario o contraseña incorrectos"

    return render(request, "login.html", {"mensaje": mensaje})


def logout_usuario(request):
    logout(request)
    return redirect("login")
