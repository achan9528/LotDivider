from django.urls import path, include
from LotDividerAPI.views import TestView

urlpatterns = [
    path('api/welcome/', TestView.as_view()),
    path('api/rest-auth/', include('rest_auth.urls')),
    path('api/rest-auth/registration/', include('rest_auth.registration.urls'))
]