from LotDividerAPI.models import User
from LotDividerAPI.serializers import CreateProjectSerializer
from django.http import HttpResponseBadRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_auth.registration import views as restAuthViews
from rest_framework.generics import CreateAPIView

# Login and Registration views are through the django-rest-auth
# library (see github)

class TestView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'welcome': 'hello!'
        }
        return Response(content)

class CreateProjectView(CreateAPIView):
    serializer_class = CreateProjectSerializer



