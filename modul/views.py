from django.utils import timezone
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from modul.models import Weather7Daily, Weather24Hourly
from modul.serializers import Weather3DailySerializer, Weather24HourlySerializer
import requests
from django.http import JsonResponse


class Weather3DailyModelViewSet(ViewSet):
    serializer_class = Weather3DailySerializer
    queryset = Weather7Daily.objects.filter(created_at__date=timezone.now().date())

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(data=serializer.data, status=200)


class Weather24HourlyModelViewSet(ViewSet):
    serializer_class = Weather24HourlySerializer
    queryset = Weather24Hourly.objects.filter(created_at__date=timezone.now().date())

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=200)


def get_weekly_weather(request):
    lat = 40.5  # Yarim atrofda joylashgan geografik enlem
    lon = 68.75  # Yarim atrofda joylashgan geografik boylam
    api_key = "f5acb50ac7e17eac9343767377447ac4"
    base_url = f"https://api.openweathermap.org/data/2.5/onecall"
    params = {
        'lat': lat,
        'lon': lon,
        'units': 'metric',
        'exclude': 'current,minutely',
        'appid': api_key,
    }

    response = requests.get(base_url, params=params)
    weather_data = response.json()
    if response.status_code == 200:
        daily_forecast = weather_data.get('daily')[:7]
        Weather7Daily.objects.create(weather=daily_forecast)
        return JsonResponse({'success': 'Success'}, status=200)
    else:
        return JsonResponse({'error': 'weather error'}, status=400)


def get_hourly_weather(request):
    lat = 40.5  # Yarim atrofda joylashgan geografik enlem
    lon = 68.75  # Yarim atrofda joylashgan geografik boylam
    api_key = "f5acb50ac7e17eac9343767377447ac4"
    base_url = f"https://api.openweathermap.org/data/2.5/onecall"
    params = {
        'lat': lat,
        'lon': lon,
        'units': 'metric',
        'exclude': 'current,minutely,daily',
        'appid': api_key,
    }

    response = requests.get(base_url, params=params)
    weather_data = response.json()
    if response.status_code == 200:
        hourly_forecast = weather_data.get('hourly')[:24]
        Weather24Hourly.objects.create(weather=hourly_forecast)
        return JsonResponse({'success': 'Success'}, status=200)
    else:
        return JsonResponse({'error': 'weather error'}, status=400)
