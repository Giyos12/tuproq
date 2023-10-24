from rest_framework import serializers
from .models import Weather24Hourly, Weather7Daily


class Weather24HourlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather24Hourly
        fields = '__all__'


class Weather3DailySerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather7Daily
        fields = '__all__'
