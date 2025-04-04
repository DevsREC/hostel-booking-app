from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
    icon = 'fa-solid fa-users'
    verbose_name = 'Users'
    divider_title = 'Manage Users'
