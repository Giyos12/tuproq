from tuproq.routers import CustomRouter
from uath import views

router = CustomRouter(root_view_name='account-wallet-root')
router.register(r'auth', views.AuthModelViewSet, basename='auth')
router.register(r'admin-system', views.ModelAdminViewSet, basename='admin-system')
router.register(r'update-order', views.ModelOrderUpdateViewSet, basename='update-order')
router.register(r'add-power-user', views.AddPowerUserViewSet, basename='user-add-role')
router.register(r'export', views.ExportCounterDBToExel, basename='export')
urlpatterns = router.urls
