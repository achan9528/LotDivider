from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('portfolios/add', views.addPortfolio),
    path('portfolios/lots', views.viewLots),
]
