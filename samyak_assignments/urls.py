from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header  = "Samyak Computer Classes — Admin"
admin.site.site_title   = "Samyak Admin"
admin.site.index_title  = "Ram Sir Classes — Administration Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('assignments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'assignments.views.handler404'
handler500 = 'assignments.views.handler500'
