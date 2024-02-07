from apscheduler.schedulers.background import BackgroundScheduler
from modul.views import WeatherViewSet
from .utils import CounterTasks


def start():
    scheduler = BackgroundScheduler()
    weather = WeatherViewSet()
    scheduler.add_job(weather.get_weekly_weather, 'cron', hour=0, minute=0, second=0, timezone='UTC',
                      id='weatherweakly_001', replace_existing=True)

    scheduler.start()


def start2():
    scheduler = BackgroundScheduler()
    weather = WeatherViewSet()
    scheduler.add_job(weather.get_hourly_weather, 'cron', hour=0, minute=0, second=0, timezone='UTC',
                      id='weatherhourly_001', replace_existing=True)

    scheduler.start()


def counter_year():
    scheduler = BackgroundScheduler()
    counter_year = CounterTasks()
    scheduler.add_job(counter_year.avg_year_counter, 'cron', month='1', day='1', hour='5', minute=3,
                      timezone='Asia/Tashkent',
                      id='counteryear_001', replace_existing=True)

    scheduler.start()


def counter_season():
    scheduler = BackgroundScheduler()
    counter_season = CounterTasks()
    scheduler.add_job(counter_season.avg_season_counter, 'cron', month='3,6,9,12', day='1', hour='5', minute=3,
                      timezone='Asia/Tashkent',
                      id='counterseason_001', replace_existing=True)

    scheduler.start()


def counter_month():
    scheduler = BackgroundScheduler()
    counter_month = CounterTasks()
    scheduler.add_job(counter_month.avg_monthly_counter, 'cron', day='7', hour='10', minute="53",
                      timezone='Asia/Tashkent',
                      id='countermonth_001', replace_existing=True)

    scheduler.start()
