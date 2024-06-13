from django.urls import path

from api import views


app_name = 'api'


urlpatterns = [
    path('languages/<slug:slug>/', views.LanguageDetail.as_view()),
    path('users/', views.create_user),
]