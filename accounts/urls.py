from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "accounts"

urlpatterns = [
    path('register/', views.register_page, name="register-page"),
    path('login/', views.login_page, name="login-page"),
    path('logout/', views.logout_user, name="logout"),

    path('', views.user_page, name="user-page"),
]
