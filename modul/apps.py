from django.apps import AppConfig


class ModulConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modul'

    def ready(self):
        print('Modul is ready')

        # 1 marta ishlashi uchun shart qo'shing
        if not hasattr(ModulConfig, '_is_ready_called'):
            ModulConfig._is_ready_called = True

            from modul.weather_scheduling import weather_updater
            weather_updater.start()
            weather_updater.start2()
            weather_updater.counter_year()
            weather_updater.counter_season()
            weather_updater.counter_month()
