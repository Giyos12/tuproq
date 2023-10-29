import json
import random
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from modul.models import Weather7Daily, Weather24Hourly, Prediction, Modul, Counter, B
from uath.models import Model
from modul.serializers import Weather3DailySerializer, Weather24HourlySerializer, PredictionSerializer, ModulSerializer, \
    CounterSerializer, BSerializer
import requests
from django.http import JsonResponse
from modul.utils import dl_predict, ml_predict
from uath.permissions import IsAdmin, IsPowerUser
from rest_framework import permissions
import ee
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

    # def get_queryset(self):
    #     # get last 2653 data
    #     return Counter.objects.all().order_by('-id')[:2653]

    def list(self, request, *args, **kwargs):
        params = request.query_params
        if params.get('name'):
            try:
                p1 = Prediction.objects.get(name=params.get('name'))
                query = Counter.objects.filter(massiv=p1)
                queryset2 = query.order_by('-id')[:2653]
            except Prediction.DoesNotExist:
                return Response(data={'message': 'massiv topilmadi'}, status=404)
            serializer = self.serializer_class(queryset2, many=True)
            return Response(serializer.data, status=200)
        serializer = self.serializer_class(Counter.objects.all().order_by('-id')[:2653], many=True)
        return Response(serializer.data, status=200)

    def create(self, request, *args, **kwargs):
        return Response(data={'message': 'method not allowed'}, status=405)

    def partial_update(self, request, *args, **kwargs):
        return Response(data={'message': 'method not allowed'}, status=405)

    def destroy(self, request, *args, **kwargs):
        return Response(data={'message': 'method not allowed'}, status=405)

    def update(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.groups.all()[0].name == 'admin_system' or request.user.groups.all()[0].name == 'power_user'):
            return super().update(request, *args, **kwargs)
        return Response(data={'message': 'user not authenticated'}, status=401)


class PredictionCounterViewSet(ViewSet):
    queryset = Counter.objects.all()
    serializer_class = CounterSerializer
    pagination_class = 100

    # def list(self, request):
    #     b1 = B.objects.filter(date__year='2022', date__month='09', date__day='01').first()
    #     file = b1.file
    #
    #     for i in file.read().decode('utf-8').splitlines()[1:2]:
    #
    #
    #         Counter.objects.create(
    #             counter_id=(i.split(',')[8]),
    #             b1=(i.split(',')[0]),
    #             b2=(i.split(',')[1]),
    #             b3=(i.split(',')[2]),
    #             b4=(i.split(',')[3]),
    #             b5=(i.split(',')[4]),
    #             b6=(i.split(',')[5]),
    #             b7=(i.split(',')[6]),
    #             b10=(i.split(',')[7]),
    #             gumus=bashorat((i.split(',')[0]), i.split(',')[1], i.split(',')[2], i.split(',')[3], i.split(',')[4],
    #                            i.split(',')[5], i.split(',')[6], i.split(',')[7]),
    #             fosfor=bashorat((i.split(',')[0]), i.split(',')[1], i.split(',')[2], i.split(',')[3], i.split(',')[4],
    #                             i.split(',')[5], i.split(',')[6], i.split(',')[7]),
    #             kaliy=bashorat((i.split(',')[0]), i.split(',')[1], i.split(',')[2], i.split(',')[3], i.split(',')[4],
    #                            i.split(',')[5], i.split(',')[6], i.split(',')[7]),
    #             shorlanish=bashorat((i.split(',')[0]), i.split(',')[1], i.split(',')[2], i.split(',')[3],
    #                                 i.split(',')[4], i.split(',')[5], i.split(',')[6], i.split(',')[7]),
    #             mex=bashorat((i.split(',')[0]), i.split(',')[1], i.split(',')[2], i.split(',')[3], i.split(',')[4],
    #                          i.split(',')[5], i.split(',')[6], i.split(',')[7]),
    #             namlik=1,
    #             date=b1.date,
    #             massiv=Counter.objects.filter(i.split(',')[8])
    #
    #         )
    #
    #         return Response(data="hjk", status=200)
    #

# update counter
# def list(self, request):
#     import json
#     geoJSON = json.load(open('Konturlar.json'))
#     # ee.Initialize()
#     count = 0
#     for i in Counter.objects.all():
#         #     # print(count)
#         #
#         #
#         #     l8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
#         #     coors = geoJSON['features'][count]['geometry']['coordinates']
#         #     aoi = ee.Geometry.Polygon(coors)
#         #     ffa_db = ee.Image(ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
#         #                       .filterBounds(aoi)
#         #                       .filterDate('2021-01-01', '2021-03-02')
#         #                       .first()
#         #                       .clip(aoi))
#         #     json = ffa_db.getInfo()
#         #     # print(float(geoJSON['features'][count]['properties']['Kontur_raq']))
#         #     # print(json['bands'][0]['crs_transform'][2])
#         #     # print(json['bands'][1]['crs_transform'][2])
#         #
#         Counter.objects.filter(id=count + 1).update(**{
#             'counter_id': geoJSON['features'][count]['properties']['Kontur_raq'],
#             #         'b1':(json['bands'][0]['crs_transform'][2])//30,
#             #         'b2':(json['bands'][1]['crs_transform'][2])//30,
#             #         'b3':json['bands'][2]['crs_transform'][2]//30,
#             #         'b4':json['bands'][3]['crs_transform'][2]//30,
#             #         'b5':json['bands'][4]['crs_transform'][2]//30,
#             #         'b6':json['bands'][5]['crs_transform'][2]//30,
#             #         'b7':json['bands'][6]['crs_transform'][2]//30,
#             #         'b10':json['bands'][7]['crs_transform'][2]//30,
#             #         'gumus':bashorat(
#             #             json['bands'][0]['crs_transform'][2]//30,
#             #             json['bands'][1]['crs_transform'][2]//30,
#             #             json['bands'][2]['crs_transform'][2]//30,
#             #             json['bands'][3]['crs_transform'][2]//30,
#             #             json['bands'][4]['crs_transform'][2]//30,
#             #             json['bands'][5]['crs_transform'][2]//30,
#             #             json['bands'][6]['crs_transform'][2]//30,
#             #             json['bands'][7]['crs_transform'][2]//30,
#             #         ),
#             'massiv': Prediction.objects.get(name=geoJSON['features'][count]['properties']['massiv'])}
#                                                     )
#         count += 1
#     serializer = self.serializer_class(self.queryset, many=True)
#     return Response(data=serializer.data, status=200)


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


def get_prediction(request):
    active_model = Model.objects.filter(order=0).first()
    if active_model.is_dl:
        dl_predict(active_model.model, request.data)
    else:
        ml_predict(active_model.model, request.data)
    return JsonResponse({'success': 'Success'}, status=200)


class BModelViewSet(ModelViewSet):
    queryset = B.objects.all()
    serializer_class = BSerializer
