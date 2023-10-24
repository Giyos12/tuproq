from django.conf.urls.static import static
from django.contrib import admin
from collections import OrderedDict

from django.urls import re_path, path, include

from rest_framework.routers import APIRootView

from tuproq import settings

api_root_dict = OrderedDict()
api_root_dict['audio'] = 'audio-root'
root_view = APIRootView.as_view(api_root_dict=api_root_dict)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/', include([
                      re_path(r'^$', root_view, name='api-root'),
                      path('accounts/', include('uath.urls')),
                      path('modul/', include('modul.urls')),

                  ])),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
