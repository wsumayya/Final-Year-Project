from django.apps import AppConfig



class NutriConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Nutri'


class NutriConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Nutri'

    def ready(self):
        import Nutri.signals  # This will ensure the signals are loaded when the app starts