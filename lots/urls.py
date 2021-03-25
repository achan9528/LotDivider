from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('portfolios/add', views.addPortfolio),
    path('accounts/add', views.addAccount),
    path('security/add', views.addSecurity),
    path('productType/add', views.addProductType),
    path('holding/add', views.addHolding),
    path('lots/add', views.addLot),
    path('portfolios/lots', views.viewLots),
    path('portfolios/holdings', views.viewAccountHoldings),
    path('portfolios/holdings/select', views.viewSelectPage),
    path('portfolios/test', views.split),
]
