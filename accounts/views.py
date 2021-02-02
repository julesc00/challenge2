import os

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import BadHeaderError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import send_mail
import emails


from .models import Usuario, LoginLog
from .forms import CreateUserForm
from .decorators import unauthenticated_user, allowed_users
from .filters import LogFilter


@unauthenticated_user
def register_page(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user_email = form.cleaned_data.get("email")
            user_email = str(user_email)
            print(user_email)
            saved_password = form.cleaned_data.get("password1")
            saved_password = str(saved_password)
            print(saved_password)

            user.save()
            #Prepare email
            message = emails.html(
                html=f"<h4>Contraseña: <strong>{saved_password}</strong></p></h4>",
                subject="Enviado desde Challenge App",
                mail_from="julesc003@gmail.com"
            )
            try:
                # Send the email
                r = message.send(
                    to="julesc003@gmail.com",
                    smtp={
                        "host": "smtp.gmail.com",
                        "port": 587,
                        "timeout": 5,
                        "user": "julesc003@gmail.com",
                        "password": "gbxisrodikjuihxa",
                        "tls": True,
                    },
                )
            except BadHeaderError:
                return HttpResponse(f"response: {r.status_code == 250}")

            return redirect("accounts:login-page")

    context = {
        "title": "Página de Registro",
        "form": form
    }

    return render(request, "accounts/register.html", context)


@unauthenticated_user
def login_page(request):
    """Log in a user"""
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if next in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect("accounts:user-page")
    else:
        form = AuthenticationForm()

    context = {
        "title": "Página de Login",
        "form": form
    }

    return render(request, "accounts/login.html", context)


@login_required(login_url="accounts:login-page")
@allowed_users(allowed_roles=["usuarios"])
def user_page(request):
    usuario = Usuario.objects.all()
    logs = LoginLog.objects.filter(owner=request.user)

    my_filter = LogFilter(request.GET, queryset=logs)
    logs = my_filter.qs

    context = {
        "title": "Página de Usuario",
        "usuario": usuario,
        "logs": logs,
        "my_filter": my_filter
    }

    return render(request, "accounts/user.html", context)


def logout_user(request):
    logout(request)
    return redirect("accounts:login-page")
