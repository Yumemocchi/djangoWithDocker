from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.db.utils import OperationalError, ProgrammingError


# For the initial migrate issue
try:
    urlpatterns = [
        path('brotherhood/', admin.site.urls),
        path('', include('myblog.urls')),
        path('members/', include('django.contrib.auth.urls')),
        path('members/', include('members.urls')),
    ]
except (OperationalError, ProgrammingError):
    urlpatterns = []

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

