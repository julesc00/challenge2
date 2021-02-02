import os

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import BadHeaderError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from decouple import config
import emails

from .models import Usuario, LoginLog
from .forms import CreateUserForm
from .decorators import unauthenticated_user, allowed_users
from .filters import LogFilter


@unauthenticated_user
def register_page(request):
    """Register a new user and send them a confirmation email with password."""
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
                mail_from=config("EMAIL_HOST_USER")
            )
            try:
                # Send the email
                r = message.send(
                    to=user_email,
                    smtp={
                        "host": config("EMAIL_HOST"),
                        "port": 587,
                        "timeout": 5,
                        "user": config("EMAIL_HOST_USER"),
                        "password": config("EMAIL_HOST_PASSWORD"),
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
    """Show user dashboard and his/her login logs."""
    usuario = Usuario.objects.all()
    logs = LoginLog.objects.filter(owner__usuario=request.user.usuario)

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
    """log out a user."""
    logout(request)
    return redirect("accounts:login-page")
