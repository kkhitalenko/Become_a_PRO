from django.urls import path

from rest_framework.generics import RetrieveAPIView

from api import views
from api.serializers import LanguageSerializer
from lessons.models import Language


app_name = 'api'


urlpatterns = [
    path(
        'languages/<slug:slug>/',
        RetrieveAPIView.as_view(
            queryset=Language.objects.all(),
            serializer_class=LanguageSerializer,
            lookup_field='slug'
        ),
        name='language description'
    ),
    path('create_user/', views.create_user),
]
