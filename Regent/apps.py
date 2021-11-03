from django.apps import AppConfig


class RegentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Regent'
    
    def ready(self):
        import Regent.signals
        
