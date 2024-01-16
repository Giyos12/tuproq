from django.contrib import admin
from modul.models import Weather7Daily, Weather24Hourly, Prediction, Modul, Counter, B, CounterSeasons, \
    CounterYears

admin.site.register(Weather7Daily)
admin.site.register(Weather24Hourly)
admin.site.register(Prediction)
admin.site.register(Modul)
admin.site.register(Counter)
admin.site.register(B)
# admin.site.register(CounterSeasons)
# admin.site.register(CounterYears)
