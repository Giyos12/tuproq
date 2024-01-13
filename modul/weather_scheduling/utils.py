from django.http import JsonResponse

from modul.models import CounterYears, CounterSeasons, Counter
from django.db.models import Avg, aggregates
from django.utils import timezone


class Counter:
    def __init__(self):
        pass

    @staticmethod
    def avg_year_counter():
        year = timezone.now().year
        counters = Counter.objects.filter(date__year=year, date__month=1)
        queryset = Counter.objects.filter(date__year=year)
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
        time = timezone.now()



