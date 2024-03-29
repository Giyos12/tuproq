import os
import pickle
from keras.models import load_model
from django.db import transaction
from django.utils import timezone
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from modul.models import Weather7Daily, Weather24Hourly, Prediction, Modul, Counter, B, CounterSeasons, CounterYears
from uath.models import Model
from modul.serializers import Weather3DailySerializer, Weather24HourlySerializer, ModulSerializer, \
    CounterSerializer, BSerializer, CounterSeasonsSerializer
import requests
from django.http import JsonResponse
from modul.utils import namlik_predict
from modul.service import bashorat
from tuproq.settings import BASE_DIR
from uath.permissions import IsAdmin


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
                if timezone.now().month > 1:
                    serializer = self.serializer_class(
                        Counter.objects.filter(date__year=timezone.now().year,
                                               date__month=int(timezone.now().month) - 1).filter(massiv=p1),
                        many=True)
                else:
                    serializer = self.serializer_class(
                        Counter.objects.filter(date__year=int(timezone.now().year) - 1, date__month=12).filter(
                            massiv=p1),
                        many=True)

            except Prediction.DoesNotExist:
                return Response(data={'message': 'bu massivda kontrlar mavjud emas'}, status=404)
            return Response(serializer.data, status=200)

        if params.get('year'):
            if params.get('year'):
                query = CounterYears.objects.filter(date__year=str(int(params.get('year')) + 1))

                serializer = self.serializer_class(query, many=True)
                return Response(serializer.data, status=200)

        if params.get('quarter'):
            if params.get('quarter'):
                current_month = int(timezone.now().month)
                month = int(params.get('quarter'))
                if month == 3:
                    if current_month - month > 0:
                        query = CounterSeasons.objects.filter(date__year=timezone.now().year,
                                                              date__month=params.get('quarter'))
                        serializer = CounterSeasonsSerializer(query, many=True)
                        return Response(serializer.data, status=200)
                    else:
                        query = CounterSeasons.objects.filter(date__year=str(int(timezone.now().year) - 1),
                                                              date__month=params.get('quarter'))
                        serializer = CounterSeasonsSerializer(query, many=True)
                        return Response(serializer.data, status=200)
                if month == 6:
                    if current_month - month > 0:
                        query = CounterSeasons.objects.filter(date__year=timezone.now().year,
                                                              date__month=params.get('quarter'))
                    else:
                        query = CounterSeasons.objects.filter(date__year=str(int(timezone.now().year) - 1),
                                                              date__month=params.get('quarter'))
                    serializer = CounterSeasonsSerializer(query, many=True)
                    return Response(serializer.data, status=200)
                if month == 9:
                    if current_month - month > 0:
                        query = CounterSeasons.objects.filter(date__year=timezone.now().year,
                                                              date__month=params.get('quarter'))
                    else:
                        query = CounterSeasons.objects.filter(date__year=str(int(timezone.now().year) - 1),
                                                              date__month=params.get('quarter'))
                    serializer = CounterSeasonsSerializer(query, many=True)
                    return Response(serializer.data, status=200)
                if month == 12:
                    if current_month - month > 0:
                        query = CounterSeasons.objects.filter(date__year=timezone.now().year,
                                                              date__month=params.get('quarter'))

                    else:
                        query = CounterSeasons.objects.filter(date__year=str(int(timezone.now().year) - 1),
                                                              date__month=params.get('quarter'))
                    serializer = CounterSeasonsSerializer(query, many=True)
                    return Response(serializer.data, status=200)

        if params.get('month'):
            if params.get('month'):
                current_month = int(timezone.now().month)
                if current_month - int(params.get('month')) > 0:
                    query = Counter.objects.filter(date__year=timezone.now().year, date__month=params.get('month'))
                else:
                    query = Counter.objects.filter(date__year=str(int(timezone.now().year) - 1),
                                                   date__month=params.get('month'))
                serializer = self.serializer_class(query, many=True)
                return Response(serializer.data, status=200)
        if timezone.now().month > 1:
            serializer = self.serializer_class(
                Counter.objects.filter(date__year=timezone.now().year, date__month=int(timezone.now().month) - 1),
                many=True)
        else:
            serializer = self.serializer_class(
                Counter.objects.filter(date__year=int(timezone.now().year) - 1, date__month=12),
                many=True)
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
        print(len(geoJSON['features']))
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


class CounterSeasonsViewSet(ModelViewSet):
    queryset = CounterSeasons.objects.all()
    serializer_class = CounterSerializer

    def list(self, request, *args, **kwargs):
        params = request.query_params
        if params.get('q'):
            n = int(params.get('q'))
            current_month = int(timezone.now().month)
            if n == 12 and current_month - n >= 0:
                counter = Counter.objects.filter(date__year=timezone.now().year, date__month__in=[11, 10, 9])


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
            if m1.is_dl:
                preprocessing1 = pickle.load(open(m1.file1norm.path, 'rb'))
                model1 = load_model(m1.file1.path)
                preprocessing2 = pickle.load(open(m1.file2norm.path, 'rb'))
                model2 = load_model(m1.file2.path)
                preprocessing3 = pickle.load(open(m1.file3norm.path, 'rb'))
                model3 = load_model(m1.file3.path)
                preprocessing4 = pickle.load(open(m1.file4norm.path, 'rb'))
                model4 = load_model(m1.file4.path)
                preprocessing5 = pickle.load(open(m1.file5norm.path, 'rb'))
                model5 = load_model(m1.file5.path)
            else:
                preprocessing1 = pickle.load(open(m1.file1norm.path, 'rb'))
                model1 = pickle.load(open(m1.file1.path, 'rb'))
                preprocessing2 = pickle.load(open(m1.file2norm.path, 'rb'))
                model2 = pickle.load(open(m1.file2.path, 'rb'))
                preprocessing3 = pickle.load(open(m1.file3norm.path, 'rb'))
                model3 = pickle.load(open(m1.file3.path, 'rb'))
                preprocessing4 = pickle.load(open(m1.file4norm.path, 'rb'))
                model4 = pickle.load(open(m1.file4.path, 'rb'))
                preprocessing5 = pickle.load(open(m1.file5norm.path, 'rb'))
                model5 = pickle.load(open(m1.file5.path, 'rb'))

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
                                   i.split(',')[5], i.split(',')[6], i.split(',')[7], preprocessing1, model1, m1.is_dl),
                    fosfor=bashorat((i.split(',')[0]), i.split(',')[1], i.split(',')[2], i.split(',')[3],
                                    i.split(',')[4],
                                    i.split(',')[5], i.split(',')[6], i.split(',')[7], preprocessing2, model2,
                                    m1.is_dl),
                    kaliy=bashorat((i.split(',')[0]), i.split(',')[1], i.split(',')[2], i.split(',')[3],
                                   i.split(',')[4],
                                   i.split(',')[5], i.split(',')[6], i.split(',')[7], preprocessing3, model3, m1.is_dl),
                    shorlanish=bashorat((i.split(',')[0]), i.split(',')[1], i.split(',')[2], i.split(',')[3],
                                        i.split(',')[4], i.split(',')[5], i.split(',')[6], i.split(',')[7],
                                        preprocessing4, model4, m1.is_dl),

                    mex=bashorat((i.split(',')[0]), i.split(',')[1], i.split(',')[2], i.split(',')[3], i.split(',')[4],
                                 i.split(',')[5], i.split(',')[6], i.split(',')[7], preprocessing5, model5, m1.is_dl),
                    namlik=namlik_predict(i.split(',')[4], i.split(',')[5]),
                    date=s1.date,
                    massiv=c1.massiv,
                    model=m1,

                )

        return Response(data=serializer.data, status=200)


class ExampleView(APIView):
    def get(self, request):
        print(request.user)
        return Response(data={'message': 'success'}, status=200)
