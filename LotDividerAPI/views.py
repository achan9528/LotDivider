from LotDividerAPI.models import User
from LotDividerAPI.serializers import UserSerializer
from django.http import HttpResponseBadRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import bcrypt

# view to register and create a new client
class RegisterView(generics.CreateAPIView):
    # these variables below to the generic API view are
    # overwritten here for customization
    queryset = User.objects.all()
    serializer_class = UserSerializer

# view to login 
class LoginView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TestView(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, format=None):
        content = {
            'welcome': 'hello!'
        }
        return Response(content)



