from django.contrib import admin
from django.urls import path, include
from web.models import Image, Participant, Block, Trial, Login, Delete, Flag
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin', admin.site.urls),
    path('', include('web.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)