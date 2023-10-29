from django.db import models
from django.utils import timezone
from uath.models import Model


def custom_time():
    return timezone.now()


class Weather7Daily(models.Model):
    weather = models.JSONField()
    created_at = models.DateTimeField(default=custom_time)

    class Meta:
        db_table = 'weather7_daily'
        verbose_name = 'Weather7Daily'
        verbose_name_plural = 'Weather7Dailys'


class Weather24Hourly(models.Model):
    weather = models.JSONField()
    created_at = models.DateTimeField(default=custom_time)

    class Meta:
        db_table = 'weather24_hourly'
        verbose_name = 'Weather24Hourly'
        verbose_name_plural = 'Weather24Hourlys'


class Prediction(models.Model):
    name = models.CharField(max_length=255, default='region')
    b1 = models.FloatField()
    b2 = models.FloatField()
    b3 = models.FloatField()
    b4 = models.FloatField()
    b5 = models.FloatField()
    b6 = models.FloatField()
    b7 = models.FloatField()
    b10 = models.FloatField()
    gumus = models.FloatField()
    fosfor = models.FloatField()
    kaliy = models.FloatField()
    shorlanish = models.FloatField()
    namlik = models.FloatField()
    mex = models.FloatField(default=1)
    model = models.ForeignKey(Model, on_delete=models.DO_NOTHING, related_name='prediction')
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'prediction'
        verbose_name = 'Prediction'
        verbose_name_plural = 'Predictions'

    def __str__(self):
        return self.name


class Counter(models.Model):
    counter_id = models.CharField(max_length=255, unique_for_year='date', unique_for_month='date')
    b1 = models.FloatField()
    b2 = models.FloatField()
    b3 = models.FloatField()
    b4 = models.FloatField()
    b5 = models.FloatField()
    b6 = models.FloatField()
    b7 = models.FloatField()
    b10 = models.FloatField()
    gumus = models.FloatField()
    fosfor = models.FloatField()
    kaliy = models.FloatField()
    shorlanish = models.FloatField()
    namlik = models.FloatField()
    mex = models.FloatField(default=1)
    model = models.ForeignKey(Model, on_delete=models.DO_NOTHING, related_name='counter')
    created_at = models.DateTimeField(auto_now_add=True)
    massiv = models.ForeignKey(Prediction, on_delete=models.DO_NOTHING, related_name='counter')
    date = models.DateTimeField(default=custom_time)

    class Meta:
        db_table = 'counter'
        verbose_name = 'Counter'
        verbose_name_plural = 'Counters'


class Modul(models.Model):
    name = models.CharField(max_length=255, unique=True)
    status = models.BooleanField(default=False)


class B(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='csv')
    date = models.DateTimeField(default=custom_time)
