from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('login', views.login),
    path('register', views.register),
    path('dashboard', views.dashboard),
    path('projects/new/', views.newProject),
    path('projects/<int:id>/', views.projectDashboard),
    # path('projects/<int:id>/', views.projectDashboard),
    path('projects/<int:projectID>/portfolios/<int:portfolioID>/', views.portfolioView),
    path('projects/<int:projectID>/portfolios/<int:portfolioID>/accounts/<int:accountID>/', views.accountView),
    path('projects/<int:projectID>/portfolios/<int:portfolioID>/accounts/<int:accountID>/proposals/new/', views.newProposal),
    path('projects/<int:projectID>/portfolios/<int:portfolioID>/accounts/<int:accountID>/proposals/<int:proposalID>/', views.proposals),
    path('portfolios/add/', views.addPortfolio),
    path('accounts/add/', views.addAccount),
    path('security/add/', views.addSecurity),
    path('productType/add/', views.addProductType),
    path('holdings/add/', views.addHolding),
    path('lots/add/', views.addLot),
    path('admin', views.admin),
]

