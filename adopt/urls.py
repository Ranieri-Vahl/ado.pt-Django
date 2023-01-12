from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('publish/', include('publish.urls')),
    path('adoption/', include('adoption.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
