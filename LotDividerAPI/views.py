from LotDividerAPI.models import User
from LotDividerAPI import serializers
from django.http import HttpResponseBadRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions, mixins
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_auth.registration import views as restAuthViews
from .models import Project, ProductType

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

class ProjectView(generics.GenericAPIView, 
                mixins.CreateModelMixin, 
                mixins.ListModelMixin):
    queryset = Project.objects.all()
    serializer_class = serializers.CreateProjectSerializer

    def get_queryset(self):
        user = self.request.user
        return user.projects.all()

    def get(self, request, format=None):
        return self.list(request)

    def post(self, request, format=None):
        return self.create(request)

class ListProductTypesView(generics.GenericAPIView,
                mixins.CreateModelMixin,
                mixins.ListModelMixin):
    queryset = ProductType.objects.all()
    serializer_class = serializers.ProductTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        return self.list(request)

    def post(self, request, format=None):
        return self.create(request)
        
class ProductTypeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductType.objects.all()
    lookup_field = 'id'
    serializer_class = serializers.ProductTypeSerializer
    
    def get_queryset(self):
        return ProductType.objects.filter(id=self.kwargs['id'])
    
    

