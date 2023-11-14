from django.apps import AppConfig


class ModulConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modul'

    def ready(self):
        print('Modul is ready')
        from modul.weather_scheduling import weather_updater
        weather_updater.start()
        weather_updater.start2()
