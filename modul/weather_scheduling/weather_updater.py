from apscheduler.schedulers.background import BackgroundScheduler
from modul.views import WeatherViewSet
from .utils import Counter


def start():
    scheduler = BackgroundScheduler()
    weather = WeatherViewSet()
    scheduler.add_job(weather.get_weekly_weather, 'cron', hour=0, minute=0, second=0, timezone='UTC',
                      id='weatherweakly_001', replace_existing=True)

    scheduler.start()


def start2():
    scheduler = BackgroundScheduler()
    weather = WeatherViewSet()
    scheduler.add_job(weather.get_hourly_weather, 'cron', month=1, hour=0, minute=0, second=0, timezone='UTC',
                      id='weatherhourly_001', replace_existing=True)

    scheduler.start()


def counter_year():
    scheduler = BackgroundScheduler()
    counter_year = Counter()
    scheduler.add_job(counter_year.avg_year_counter, 'interval', timezone='UTC',
                      id='counteryear_001', replace_existing=True)

    scheduler.start()

def counter_season():
    scheduler = BackgroundScheduler()
    counter_season = Counter()
    scheduler.add_job(counter_season.avg_season_counter, 'interval', timezone='UTC',
                      id='counterseason_001', replace_existing=True)

    scheduler.start()
