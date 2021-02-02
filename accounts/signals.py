from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.dispatch import receiver

from .models import Usuario, LoginLog


def user_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name="usuarios")
        instance.groups.add(group)

        Usuario.objects.create(
            user=instance,
            name=instance.username
        )
        print("Profile created")


post_save.connect(user_profile, sender=User)


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    print(f"User {user.username} logged in on {user.last_login}")

    log = user.last_login

    LoginLog.objects.create(
        login_log=log
    )


