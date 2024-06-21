from rest_framework import generics, viewsets

from api.serializers import LanguageSerializer, ProgressSerializer
from lessons.models import Language, Progress


class LanguageDetail(generics.RetrieveAPIView):
    """View for getting language description."""

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    lookup_field = 'slug'


class ProgressViewSet(viewsets.ModelViewSet):
    """ViewSet for user progress CRUD operations."""

    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
