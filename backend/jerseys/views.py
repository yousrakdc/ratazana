from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Jersey
from .serializers import JerseySerializer

class PromotedJerseysView(APIView):
    def get(self, request, *args, **kwargs):
        jerseys = Jersey.objects.filter(is_promoted=True)
        serializer = JerseySerializer(jerseys, many=True)
        return Response({'promoted_jerseys': serializer.data}, status=status.HTTP_200_OK)
