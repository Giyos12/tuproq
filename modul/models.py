from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError

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
    model = models.ForeignKey(Model, on_delete=models.SET_NULL, null=True, related_name='prediction')
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'prediction'
        verbose_name = 'Prediction'
        verbose_name_plural = 'Predictions'

    def __str__(self):
        return self.name


class Counter(models.Model):
    counter_id = models.CharField(max_length=255)
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
    model = models.ForeignKey(Model, on_delete=models.SET_NULL, null=True, related_name='counter')
    created_at = models.DateTimeField(auto_now_add=True)
    massiv = models.ForeignKey(Prediction, on_delete=models.DO_NOTHING, related_name='counter')
    date = models.DateTimeField(default=custom_time)

    class Meta:
        db_table = 'counter'
        verbose_name = 'Counter'
        verbose_name_plural = 'Counters'

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        counters = Counter.objects.filter(counter_id=self.counter_id)
        for counter in counters:
            if self.id != counter.id and self.date.year == counter.date.year and self.date.month == counter.date.month:
                raise ValidationError("You can't save this model")
        super().save(force_insert, force_update, using, update_fields)


class CounterSeasons(models.Model):
    CHOICES = (
        ('winter', 'winter'),
        ('spring', 'spring'),
        ('summer', 'summer'),
        ('autumn', 'autumn'),
    )
    season = models.CharField(max_length=128, choices=CHOICES)
    counter_id = models.CharField(max_length=255)
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
    model = models.ForeignKey(Model, on_delete=models.SET_NULL, null=True, related_name='counter_seasons')
    created_at = models.DateTimeField(auto_now_add=True)
    massiv = models.ForeignKey(Prediction, on_delete=models.DO_NOTHING, related_name='counter_seasons')
    date = models.DateTimeField(default=custom_time)

    class Meta:
        db_table = 'counter_seasons'
        verbose_name = 'CounterSeasons'
        verbose_name_plural = 'CounterSeasonss'

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        counters = CounterSeasons.objects.filter(counter_id=self.counter_id)
        for counter in counters:
            if self.id != counter.id and self.date.year == counter.date.year and self.date.month == counter.date.month:
                raise ValidationError("You can't save this model")
            # if self.season
        super().save(force_insert, force_update, using, update_fields)


class CounterYears(models.Model):
    counter_id = models.CharField(max_length=255)
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
    created_at = models.DateTimeField(auto_now_add=True)
    massiv = models.ForeignKey(Prediction, on_delete=models.DO_NOTHING, related_name='counter_years')
    date = models.DateTimeField(default=custom_time)

    class Meta:
        db_table = 'counter_years'
        verbose_name = 'CounterYears'
        verbose_name_plural = 'CounterYearss'

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        counters = CounterYears.objects.filter(counter_id=self.counter_id)
        for counter in counters:
            if self.id != counter.id and self.date.year == counter.date.year:
                raise ValidationError("You can't save this model")
        super().save(force_insert, force_update, using, update_fields)


class Modul(models.Model):
    name = models.CharField(max_length=255, unique=True)
    status = models.BooleanField(default=False)
    is_information = models.BooleanField(default=False)
    is_recommendation = models.BooleanField(default=False)
    is_feature = models.BooleanField(default=False)


class B(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='csv')
    date = models.DateTimeField(default=custom_time)
