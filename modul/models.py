from django.db import models
from django.utils import timezone


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
