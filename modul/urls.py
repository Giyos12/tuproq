from tuproq.routers import CustomRouter
from modul import views

router = CustomRouter(root_view_name='modul-root')
router.register(r'weather3-daily', views.Weather3DailyModelViewSet, basename='weather3-daily')
router.register(r'weather24-hourly', views.Weather24HourlyModelViewSet, basename='weather24-hourly')
router.register(r'prediction', views.PredictionModulViewSet, basename='prediction')
router.register(r'module', views.ModulModelViewSet, basename='module')

urlpatterns = router.urls