from django.shortcuts import get_object_or_404

from rest_framework import generics, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from api.serializers import (LanguageSerializer, LessonSerializer,
                             ProgressCreateSerializer,
                             ProgressGetUpdateDeleteSerializer,
                             WrongAnsweredQuestionsSerializer)
from lessons.models import Language, Lesson, Progress, Question


class LanguageDetail(generics.RetrieveAPIView):
    """View for getting language description."""

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    lookup_field = 'slug'


class ProgressViewSet(viewsets.ModelViewSet):
    """ViewSet for user progress CRUD operations."""

    queryset = Progress.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'create':
            return ProgressCreateSerializer
        return ProgressGetUpdateDeleteSerializer

    @action(detail=True, methods=['get', 'patch'])
    def wrong_answered_questions(self, request, slug):
        language, tg_user_id = slug.split('_')
        language = Language.objects.get(title=language)
        progress = Progress.objects.get(language=language,
                                        tg_user_id=tg_user_id)

        if request.method == 'GET':
            serializer = WrongAnsweredQuestionsSerializer(progress)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PATCH':
            wrong_answered_questions = request.data.get('wrong_answers')

            progress.wrong_answers.clear()
            if wrong_answered_questions:
                new_questions = [Question.objects.get(id=question)
                                 for question in wrong_answered_questions]
                progress.wrong_answers.set(new_questions)
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def lesson_detail(request, language, serial_number):
    """Retrieve a lesson instance."""

    language = Language.objects.get(title=language)
    lesson = get_object_or_404(Lesson, language=language,
                               serial_number=serial_number)
    serializer = LessonSerializer(lesson)
    return Response(serializer.data, status=status.HTTP_200_OK)
