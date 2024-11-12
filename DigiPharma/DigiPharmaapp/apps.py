from django.apps import AppConfig


class DigipharmaappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DigiPharmaapp'
    
    def ready(self):
        import DigiPharmaapp.signals