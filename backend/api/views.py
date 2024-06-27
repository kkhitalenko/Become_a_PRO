from django.shortcuts import get_object_or_404

from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import (LanguageSerializer, LessonSerializer,
                             ProgressSerializer)
from lessons.models import Language, Lesson, Progress


class LanguageDetail(generics.RetrieveAPIView):
    """View for getting language description."""

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    lookup_field = 'slug'


class ProgressViewSet(viewsets.ModelViewSet):
    """ViewSet for user progress CRUD operations."""

    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer

    def create(self, request):

        tg_user_id = request.data.get('tg_user_id')
        language = request.data.get('language')
        last_completed_lesson = request.data.get('last_completed_lesson')

        language = Language.objects.get(slug=language)
        lesson = Lesson.objects.get(language=language,
                                    serial_number=last_completed_lesson)

        progress = Progress.objects.create(tg_user_id=tg_user_id,
                                           language=language,
                                           last_completed_lesson=lesson)
        serializer = ProgressSerializer(progress)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view()
def lesson_detail(request, language, serial_number):
    """Retrieve a lesson instance."""

    language = Language.objects.get(title=language)
    lesson = get_object_or_404(Lesson, language=language,
                               serial_number=serial_number)
    serializer = LessonSerializer(lesson)
    return Response(serializer.data, status=status.HTTP_200_OK)
