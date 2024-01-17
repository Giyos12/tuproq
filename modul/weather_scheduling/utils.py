from django.http import JsonResponse
from modul.models import CounterYears, CounterSeasons, Counter
from django.db.models import Avg, Q
from django.utils import timezone
import calendar
from datetime import datetime
import requests
import json
import ee
import csv

service_account = 'tuproq@tuproq.iam.gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, 'tuproq-bb60103973b6.json')
ee.Initialize(credentials)

data = json.load(open('Konturlar.json'))
data = data['features']


def ret_bands(polygon, boshlanish_data, tugash_data):
    imagelist = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').filterBounds(polygon).filterDate(boshlanish_data,
                                                                                              tugash_data) \
        .select("SR_B1", "SR_B2", "SR_B3", "SR_B4", "SR_B5", "SR_B6", "SR_B7", "ST_B10")
    rasmlar_soni = imagelist.size().getInfo()
    image_list = imagelist.toList(imagelist.size())
    bands = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(rasmlar_soni):
        image = ee.Image(image_list.get(i))
        means = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=polygon,
            scale=30)
        means = means.getInfo()
        bands[0] += means["SR_B1"] * 0.9
        bands[1] += means["SR_B2"] * 0.9
        bands[2] += means["SR_B3"] * 0.85
        bands[3] += means["SR_B4"] * 0.85
        bands[4] += means["SR_B5"] * 0.9
        bands[5] += means["SR_B6"] * 0.9
        bands[6] += means["SR_B7"] * 0.9
        bands[7] += means["ST_B10"] * 1.1
    for i in range(len(bands)):
        bands[i] = int(bands[i] / rasmlar_soni)
    return bands


def write_csv_file(boshlanish_data, tugash_data):
    with open(f'media_root/csv/{boshlanish_data}.csv', 'w', newline='') as file1:
        writer = csv.writer(file1)
        writer.writerow(["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B10", "Kontur_raq"])

        for i in range(len(data)):
            coors = data[i]['geometry']['coordinates']
            aoi = ee.Geometry.Polygon(coors)
            bands = ret_bands(aoi, boshlanish_data, tugash_data)
            writer.writerow([bands[0], bands[1], bands[2], bands[3], bands[4], bands[5], bands[6], bands[7],
                             data[i]['properties']['Kontur_raq']])
            print(i)
    return f'media_root/csv/{boshlanish_data}.csv'


class CounterTasks:
    def __init__(self):
        pass

    @staticmethod
    def avg_year_counter():
        year = timezone.now().year
        counters = Counter.objects.filter(date__year=year - 1, date__month=1)
        queryset = Counter.objects.filter(date__year=year - 1)
        print(len(queryset))
        if counters:
            for i in counters:
                aggregate_qs = queryset.filter(counter_id=i.counter_id).aggregate(
                    b1=Avg('b1'),
                    b2=Avg('b2'),
                    b3=Avg('b3'),
                    b4=Avg('b4'),
                    b5=Avg('b5'),
                    b6=Avg('b6'),
                    b7=Avg('b7'),
                    b10=Avg('b10'),
                    gumus=Avg('gumus'),
                    fosfor=Avg('fosfor'),
                    kaliy=Avg('kaliy'),
                    shorlanish=Avg('shorlanish'),
                    namlik=Avg('namlik'),
                    mex=Avg('mex'))
                CounterYears.objects.create(
                    counter_id=i.counter_id,
                    b1=aggregate_qs['b1'],
                    b2=aggregate_qs['b2'],
                    b3=aggregate_qs['b3'],
                    b4=aggregate_qs['b4'],
                    b5=aggregate_qs['b5'],
                    b6=aggregate_qs['b6'],
                    b7=aggregate_qs['b7'],
                    b10=aggregate_qs['b10'],
                    gumus=aggregate_qs['gumus'],
                    fosfor=aggregate_qs['fosfor'],
                    kaliy=aggregate_qs['kaliy'],
                    shorlanish=aggregate_qs['shorlanish'],
                    namlik=aggregate_qs['namlik'],
                    mex=aggregate_qs['mex'],
                    massiv=i.massiv,
                    date=timezone.now()
                )
        else:
            print('No data')

        return JsonResponse({'success': 'Success'}, status=200)

    @staticmethod
    def avg_season_counter():
        season_dict = {
            3: 'winter',
            6: 'spring',
            9: 'summer',
            12: 'autumn'
        }
        time = timezone.now()
        year = time.year - 1
        month = time.month + 5
        date = datetime.strptime(f'{year}-{month}-01', '%Y-%m-%d')
        counters = Counter.objects.filter(date__year=year, date__month=1)
        if month == 3:
            queryset = Counter.objects.filter(
                Q(date__year=year - 1, date__month=12) |
                Q(date__year=year, date__month__in=[1, 2])
            )
            print(len(queryset))
        elif month == 6:
            queryset = Counter.objects.filter(
                Q(date__year=year, date__month__in=[3, 4, 5])
            )
            print(len(queryset))
        elif month == 9:
            queryset = Counter.objects.filter(
                Q(date__year=year, date__month__in=[6, 7, 8])
            )
        elif month == 12:
            queryset = Counter.objects.filter(
                Q(date__year=year, date__month__in=[9, 10, 11])
            )
        else:
            queryset = []

        if counters:
            for i in counters:
                aggregate_qs = queryset.filter(counter_id=i.counter_id).aggregate(
                    b1=Avg('b1'),
                    b2=Avg('b2'),
                    b3=Avg('b3'),
                    b4=Avg('b4'),
                    b5=Avg('b5'),
                    b6=Avg('b6'),
                    b7=Avg('b7'),
                    b10=Avg('b10'),
                    gumus=Avg('gumus'),
                    fosfor=Avg('fosfor'),
                    kaliy=Avg('kaliy'),
                    shorlanish=Avg('shorlanish'),
                    namlik=Avg('namlik'),
                    mex=Avg('mex'))

                CounterSeasons.objects.create(
                    counter_id=i.counter_id,
                    b1=aggregate_qs['b1'],
                    b2=aggregate_qs['b2'],
                    b3=aggregate_qs['b3'],
                    b4=aggregate_qs['b4'],
                    b5=aggregate_qs['b5'],
                    b6=aggregate_qs['b6'],
                    b7=aggregate_qs['b7'],
                    b10=aggregate_qs['b10'],
                    gumus=aggregate_qs['gumus'],
                    fosfor=aggregate_qs['fosfor'],
                    kaliy=aggregate_qs['kaliy'],
                    shorlanish=aggregate_qs['shorlanish'],
                    namlik=aggregate_qs['namlik'],
                    mex=aggregate_qs['mex'],
                    massiv=i.massiv,
                    date=timezone.now()
                )
            CounterSeasons.objects.create(
                season=season_dict[month],
                counter_id=i.counter_id,
                b1=aggregate_qs['b1'],
                b2=aggregate_qs['b2'],
                b3=aggregate_qs['b3'],
                b4=aggregate_qs['b4'],
                b5=aggregate_qs['b5'],
                b6=aggregate_qs['b6'],
                b7=aggregate_qs['b7'],
                b10=aggregate_qs['b10'],
                gumus=aggregate_qs['gumus'],
                fosfor=aggregate_qs['fosfor'],
                kaliy=aggregate_qs['kaliy'],
                shorlanish=aggregate_qs['shorlanish'],
                namlik=aggregate_qs['namlik'],
                mex=aggregate_qs['mex'],
                massiv=i.massiv,
                model=i.model,
                date=date
            )
        else:
            print('No data')

        return JsonResponse({'success': 'Success'}, status=200)

    @staticmethod
    def avg_monthly_counter():
        time = datetime.now()

        if time.month == 1:
            year = time.year - 1
            month = 12
        else:
            year = time.year
            month = time.month - 1

        last_day_of_month = calendar.monthrange(year, month)[1]
        boshlanish_data = f'{year}-{month}-01'
        formatted_date = datetime.strptime(boshlanish_data, '%Y-%m-%d')
        file_path = write_csv_file(boshlanish_data=f'{year}-{month}-01',
                                   tugash_data=f'{year}-{month}-{last_day_of_month}')
        name = str(time)
        files = {'file': open(file_path, 'rb')}
        data = {'name': name, 'date': formatted_date}

        response = requests.post(url='http://127.0.0.1:8000/api/modul/b/', files=files, data=data)

        print(response.status_code)
        print(response.text)
        return JsonResponse({'success': 'Success'}, status=200)
