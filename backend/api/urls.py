from django.urls import include, path

from rest_framework import routers

from . import views


app_name = 'api'

router = routers.DefaultRouter()
router.register(r'languages', views.LanguageViewSet)
router.register(r'topics', views.TopicViewSet)
router.register(r'lessons', views.LessonViewSet)
router.register(r'questions', views.QuestionViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
