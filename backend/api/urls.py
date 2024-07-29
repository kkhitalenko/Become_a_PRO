from django.urls import path

from api.views import LanguageDetail, ProgressViewSet, lesson_detail


app_name = 'api'


urlpatterns = [
    path('languages/<slug:slug>/', LanguageDetail.as_view()),
    path('lessons/<slug:language>/<int:serial_number>/', lesson_detail),
    path('progress/<slug:slug>/wrong_answered_questions/',
         ProgressViewSet.as_view({'get': 'wrong_answered_questions',
                                  'patch': 'wrong_answered_questions'})),
    path('progress/<slug:slug>/',
         ProgressViewSet.as_view({'get': 'retrieve',
                                  'patch': 'partial_update',
                                  'delete': 'destroy'})),
    path('progress/', ProgressViewSet.as_view({'post': 'create'})),
]
