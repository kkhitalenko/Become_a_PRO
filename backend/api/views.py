from rest_framework.generics import RetrieveAPIView

from api.serializers import LanguageSerializer
from lessons.models import Language


class LanguageDetail(RetrieveAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    lookup_field = 'slug'
