from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls', namespace='api')),
]

admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'Изучение программирования'
