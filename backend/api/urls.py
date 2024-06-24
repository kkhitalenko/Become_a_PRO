from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api import views


app_name = 'api'

v1_router = DefaultRouter()

v1_router.register(r'progress', views.ProgressViewSet, basename='progress')


urlpatterns = [
    path('languages/<slug:slug>/', views.LanguageDetail.as_view()),
    path('', include(v1_router.urls)),
]
