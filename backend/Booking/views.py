from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class GetCSRFToken(APIView):
    def get(self, request):
        token = get_token(request)
        response = Response({'detail': 'CSRF cookie set'}, status=status.HTTP_200_OK)
        return response