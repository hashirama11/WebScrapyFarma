
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('farmatodo/', include('farmatodo.urls')),
    path('farmaciasas/', include('farmaciasas.urls')),
    path('locatel/', include('locatel.urls')),
    path('farmabien/', include('farmabien.urls')),
    path('farmahorro/', include('farmahorro.urls')),
    
]
