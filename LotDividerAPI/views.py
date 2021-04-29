from LotDividerAPI.models import User
from LotDividerAPI.serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

class RegisterView(generics.CreateAPIView):
    # these variables below to the generic API view are
    # overwritten here for customization
    queryset = User.objects.all()
    serializer_class = UserSerializer



