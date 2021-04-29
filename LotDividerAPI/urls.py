from django.urls import path
from LotDividerAPI.views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view())
]