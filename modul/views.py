from django.db import transaction
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from modul.models import Weather7Daily, Weather24Hourly, Prediction, Modul, Counter, B
from uath.models import Model
from modul.serializers import Weather3DailySerializer, Weather24HourlySerializer, ModulSerializer, \
    CounterSerializer, BSerializer
import requests
from django.http import JsonResponse
from modul.utils import namlik_predict
from modul.service import bashorat


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


class ModulModelViewSet(ModelViewSet):
    queryset = Modul.objects.all()
    serializer_class = ModulSerializer

    def create(self, request, *args, **kwargs):
        return Response(data={'message': 'method not allowed'}, status=405)

    def update(self, request, *args, **kwargs):
        # IsAuthenticated and IsAdmin working
        if request.user.is_authenticated and request.user.groups.all()[0].name == 'admin_system':
            return super().update(request, *args, **kwargs)
        return Response(data={'message': 'user not authenticated'}, status=401)

    def partial_update(self, request, *args, **kwargs):
        return Response(data={'message': 'method not allowed'}, status=405)

    def destroy(self, request, *args, **kwargs):
        return Response(data={'message': 'method not allowed'}, status=405)


class CounterModelViewSet(ModelViewSet):
    queryset = Counter.objects.all()
    serializer_class = CounterSerializer

    def list(self, request, *args, **kwargs):
        params = request.query_params
        if params.get('name'):
            try:
                p1 = Prediction.objects.get(name=params.get('name'))
                query = Counter.objects.filter(date__year=timezone.now().year, date__month=timezone.now().month).filter(
                    massiv=p1)

            except Prediction.DoesNotExist:
                return Response(data={'message': 'bu massivda kontrlar mavjud emas'}, status=404)
            serializer = self.serializer_class(query, many=True)
            return Response(serializer.data, status=200)

        if params.get('year'):
            if params.get('year'):
                query = Counter.objects.filter(date__year=str(int(params.get('year')) - 1),
                                               date__month=12)

                serializer = self.serializer_class(query, many=True)
                return Response(serializer.data, status=200)

        if params.get('quarter'):
            if params.get('quarter'):
                query = Counter.objects.filter(date__year=timezone.now().year, date__month=params.get('quarter'))
                serializer = self.serializer_class(query, many=True)
                return Response(serializer.data, status=200)

        if params.get('month'):
            if params.get('month'):
                query = Counter.objects.filter(date__year=timezone.now().year, date__month=params.get('month'))
                serializer = self.serializer_class(query, many=True)
                return Response(serializer.data, status=200)

        serializer = self.serializer_class(
            Counter.objects.filter(date__year=timezone.now().year, date__month=timezone.now().month), many=True)
        return Response(serializer.data, status=200)

    def create(self, request, *args, **kwargs):
        return Response(data={'message': 'method not allowed'}, status=405)

    def partial_update(self, request, *args, **kwargs):
        return Response(data={'message': 'method not allowed'}, status=405)

    def destroy(self, request, *args, **kwargs):
        return Response(data={'message': 'method not allowed'}, status=405)

    def update(self, request, *args, **kwargs):
        if request.user.is_authenticated and (
                request.user.groups.all()[0].name == 'admin_system' or request.user.groups.all()[
            0].name == 'power_user'):
            return super().update(request, *args, **kwargs)
        return Response(data={'message': 'user not authenticated'}, status=401)


class PredictionCounterViewSet(ViewSet):
    queryset = Counter.objects.all()
    serializer_class = CounterSerializer
    pagination_class = 100

    def list(self, request):
        import json
        geoJSON = json.load(open('Konturlar.json'))
        # ee.Initialize()
        for i in geoJSON['features']:
            Counter.objects.create(counter_id=i['properties']['Kontur_raq'], b1=2, b2=3, b3=4, b4=5, b5=6, b6=7, b7=8,
                                   b10=9,
                                   gumus=9, fosfor=10, kaliy=11, shorlanish=12, mex=13, namlik=14,
                                   date=timezone.now() - timezone.timedelta(days=800),
                                   massiv=Prediction.objects.get(name=i['properties']['massiv']),
                                   model=Model.objects.get(order=0))

        serializer = self.serializer_class(self.queryset, many=True)
        return Response(data=serializer.data, status=200)


class WeatherViewSet():
    def get_weekly_weather(self):
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

    def get_hourly_weather(self):
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


class BModelViewSet(ModelViewSet):
    queryset = B.objects.all()
    serializer_class = BSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            s1 = serializer.save()
            file = s1.file
            m1 = Model.objects.filter(order='0').first()
            for i in file.read().decode('utf-8').splitlines()[1:]:
                c1 = Counter.objects.filter(counter_id=i.split(',')[8]).first()

                Counter.objects.create(
                    counter_id=(i.split(',')[8]),
                    b1=(i.split(',')[0]),
                    b2=(i.split(',')[1]),
                    b3=(i.split(',')[2]),
                    b4=(i.split(',')[3]),
                    b5=(i.split(',')[4]),
                    b6=(i.split(',')[5]),
                    b7=(i.split(',')[6]),
                    b10=(i.split(',')[7]),
                    gumus=bashorat((i.split(',')[0]), i.split(',')[1], i.split(',')[2], i.split(',')[3],
                                   i.split(',')[4],
                                   i.split(',')[5], i.split(',')[6], i.split(',')[7], m1.file1, m1.file1norm, m1.is_dl),
                    fosfor=bashorat((i.split(',')[0]), i.split(',')[1], i.split(',')[2], i.split(',')[3],
                                    i.split(',')[4],
                                    i.split(',')[5], i.split(',')[6], i.split(',')[7], m1.file2, m1.file2norm,
                                    m1.is_dl),
                    kaliy=bashorat((i.split(',')[0]), i.split(',')[1], i.split(',')[2], i.split(',')[3],
                                   i.split(',')[4],
                                   i.split(',')[5], i.split(',')[6], i.split(',')[7], m1.file3, m1.file3norm, m1.is_dl),
                    shorlanish=bashorat((i.split(',')[0]), i.split(',')[1], i.split(',')[2], i.split(',')[3],
                                        i.split(',')[4], i.split(',')[5], i.split(',')[6], i.split(',')[7], m1.file5,
                                        m1.file5norm, m1.is_dl),
                    mex=bashorat((i.split(',')[0]), i.split(',')[1], i.split(',')[2], i.split(',')[3], i.split(',')[4],
                                 i.split(',')[5], i.split(',')[6], i.split(',')[7], m1.file4, m1.file4norm, m1.is_dl),
                    namlik=namlik_predict(i.split(',')[4], i.split(',')[5]),
                    date=s1.date,
                    massiv=c1.massiv,
                    model=m1,

                )

        return Response(data=serializer.data, status=200)
