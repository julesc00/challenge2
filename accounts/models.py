from django.db import models

from django.contrib.auth.models import User


class Usuario(models.Model):
    """Create custom user model."""
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True, unique=True)
    saved_password = models.CharField(max_length=100, null=True, blank=True, default="")
    date_created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Capitalize name"""
        self.name = self.name.title()

    def __str__(self):
        return self.name


class LoginLog(models.Model):
    """Record user login logs."""
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    login_log = models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.login_log
