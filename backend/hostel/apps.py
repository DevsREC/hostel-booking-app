from django.apps import AppConfig


class HostelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hostel'
    icon = "fa-solid fa-hotel"
    divider_title = 'Manage Hostels'    