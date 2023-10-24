from django.db import models
from django.utils import timezone
from uath.models import Model


class Weather7Daily(models.Model):
    weather = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'weather7_daily'
        verbose_name = 'Weather7Daily'
        verbose_name_plural = 'Weather7Dailys'


class Weather24Hourly(models.Model):
    weather = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

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
    model = models.ForeignKey(Model, on_delete=models.DO_NOTHING, related_name='prediction')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'prediction'
        verbose_name = 'Prediction'
        verbose_name_plural = 'Predictions'


class Modul(models.Model):
    name = models.CharField(max_length=255, unique=True)
    status = models.BooleanField(default=False)

