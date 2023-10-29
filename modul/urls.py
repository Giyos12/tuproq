from tuproq.routers import CustomRouter
from modul import views

router = CustomRouter(root_view_name='modul-root')
router.register(r'weather7-daily', views.Weather3DailyModelViewSet, basename='weather7-daily')
router.register(r'weather24-hourly', views.Weather24HourlyModelViewSet, basename='weather24-hourly')
# router.register(r'prediction-massive', views.PredictionMassiveViewSet, basename='prediction-massive')
router.register(r'counter', views.PredictionCounterViewSet, basename='counter')
router.register(r'counter-db', views.CounterModelViewSet, basename='counter-db')

urlpatterns = router.urls