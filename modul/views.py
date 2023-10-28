import json
import random
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from modul.models import Weather7Daily, Weather24Hourly, Prediction, Modul, Counter
from uath.models import Model
from modul.serializers import Weather3DailySerializer, Weather24HourlySerializer, PredictionSerializer, ModulSerializer, \
    CounterSerializer
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


class PredictionModulViewSet(ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsPowerUser]


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


class PredictionMassiveViewSet(ViewSet):
    serializer_class = PredictionSerializer
    queryset = Prediction.objects.all()
    pagination_class = 100

    def list(self, request):
        # massive = ['A.Kulbekov', 'G’.Yunusov', 'Y.Oxunboboyev', 'Chinobod', 'Guliston', 'Barlos',
        #            'Shifokor Yangi-hayot', 'M.Ulug’bek', 'Beruniy', 'Mustaqillik 5 yilligi', 'Mirzacho’l', 'Yangiobod',
        #            'Toshkent', 'Dehqonobod', 'T.Axmedov', 'Bahor', 'Oqoltin']
        # for i in massive:
        #     Prediction.objects.create(
        #         name=i,
        #         b1=31113.0,
        #         b2=31113.0,
        #         b3=31113.0,
        #         b4=31113.0,
        #         b5=31113.0,
        #         b6=31113.0,
        #         b7=31113.0,
        #         b10=31113.0,
        #         gumus=random.randint(1, 5),
        #         fosfor=random.randint(1, 5),
        #         kaliy=random.randint(1, 5),
        #         shorlanish=random.randint(1, 5),
        #         namlik=random.randint(1, 5),
        #         model=Model.objects.all().first(),
        #     )
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(data=serializer.data, status=200)


class PredictionCounterViewSet(ViewSet):
    queryset = Counter.objects.all()
    serializer_class = CounterSerializer
    pagination_class = 100
    #

    def list(self, request):
        import json
        geoJSON = json.load(open('konturlar.json'))
        ee.Initialize()
        count = 0
        for i in Counter.objects.all():
            print(count)


            l8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
            coors = geoJSON['features'][count]['geometry']['coordinates']
            aoi = ee.Geometry.Polygon(coors)
            ffa_db = ee.Image(ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
                              .filterBounds(aoi)
                              .filterDate('2021-01-01', '2021-03-02')
                              .first()
                              .clip(aoi))
            json = ffa_db.getInfo()
            print(float(geoJSON['features'][count]['properties']['Kontur_raq']))
            print(json['bands'][0]['crs_transform'][2])
            print(json['bands'][1]['crs_transform'][2])
            count = count + 1
            Counter.objects.filter(counter_id=count).update(**{
                'counter_id':geoJSON['features'][count]['properties']['Kontur_raq'],
                'b1':(json['bands'][0]['crs_transform'][2])//30,
                'b2':(json['bands'][1]['crs_transform'][2])//30,
                'b3':json['bands'][2]['crs_transform'][2]//30,
                'b4':json['bands'][3]['crs_transform'][2]//30,
                'b5':json['bands'][4]['crs_transform'][2]//30,
                'b6':json['bands'][5]['crs_transform'][2]//30,
                'b7':json['bands'][6]['crs_transform'][2]//30,
                'b10':json['bands'][7]['crs_transform'][2]//30,
                'gumus':bashorat(
                    json['bands'][0]['crs_transform'][2]//30,
                    json['bands'][1]['crs_transform'][2]//30,
                    json['bands'][2]['crs_transform'][2]//30,
                    json['bands'][3]['crs_transform'][2]//30,
                    json['bands'][4]['crs_transform'][2]//30,
                    json['bands'][5]['crs_transform'][2]//30,
                    json['bands'][6]['crs_transform'][2]//30,
                    json['bands'][7]['crs_transform'][2]//30,
                ),
                'massiv':Prediction.objects.get(name=geoJSON['features'][count]['properties']['massiv'])}
            )

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


def get_prediction(request):
    active_model = Model.objects.filter(order=0).first()
    if active_model.is_dl:
        dl_predict(active_model.model, request.data)
    else:
        ml_predict(active_model.model, request.data)
    return JsonResponse({'success': 'Success'}, status=200)
