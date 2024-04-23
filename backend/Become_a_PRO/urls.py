from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls', namespace='api')),
    path('__debug__/', include('debug_toolbar.urls')),
]

admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'Изучение программирования'
