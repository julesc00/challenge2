from django.contrib import admin

from .models import Usuario, LoginLog

admin.site.register(Usuario)
admin.site.register(LoginLog)
