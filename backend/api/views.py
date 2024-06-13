from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from api.serializers import LanguageSerializer
from lessons.models import Language
from tg_user.models import TelegramUser


class LanguageDetail(RetrieveAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    lookup_field = 'slug'


@api_view(['POST'])
def create_user(request):
    user_id = request.data.get('user_id')
    username = request.data.get('username')
    if not TelegramUser.objects.filter(tg_user_id=user_id).exists():
        TelegramUser.objects.create(tg_user_id=user_id, username=username)
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_200_OK)
