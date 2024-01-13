from rest_framework import serializers
from .models import Weather24Hourly, Weather7Daily, Prediction, Modul, Counter, B, CounterSeasons, CounterYears


class CounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counter
        fields = '__all__'


class Weather24HourlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather24Hourly
        fields = '__all__'


class Weather3DailySerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather7Daily
        fields = '__all__'


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'


class ModulSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modul
        fields = '__all__'


class BSerializer(serializers.ModelSerializer):
    class Meta:
        model = B
        fields = '__all__'


class CounterSeasonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounterSeasons
        fields = '__all__'


class CounterYearsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounterYears
        fields = '__all__'
