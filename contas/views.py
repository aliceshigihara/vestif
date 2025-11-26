from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

def home_view(request):
    return render(request, "contas/index.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("principal")
    else:
        form = RegisterForm()

    return render(request, "contas/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("principal")
        else:
            return render(request, "contas/login.html", {"error": "Usuário ou senha incorretos"})

    return render(request, "contas/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

def principal_view(request):
    return render(request, 'contas/principal-page.html')

def notas_view(request):
    return render(request, 'contas/notas-page.html')

def conteudos_view(request):
    return render(request, 'contas/content-page.html')

def exercicios_view(request):
    return render(request, 'contas/simulador-page.html')