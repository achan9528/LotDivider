from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('login', views.login),
    path('register', views.register),
    path('dashboard', views.dashboard),
    path('projects/new', views.newProject),
    path('portfolios/add', views.addPortfolio),
    path('accounts/add', views.addAccount),
    path('security/add', views.addSecurity),
    path('productType/add', views.addProductType),
    path('holdings/add', views.addHolding),
    path('lots/add', views.addLot),
    path('portfolios/lots', views.viewLots),
    path('portfolios/holdings', views.viewAccountHoldings),
    path('portfolios/holdings/select', views.viewSelectPage),
    path('portfolios/test', views.split),
]
