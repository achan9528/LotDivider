from django.urls import path
from LotDividerAPI.views import RegisterView, TestView

urlpatterns = [
    path('api/welcome/', TestView.as_view()),
    path('api/registration/', RegisterView.as_view())
]