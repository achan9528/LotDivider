from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.login),
    path('login', views.login),
    path('register', views.register),
    path('dashboard/', views.dashboard),
    path('projects/new/', views.newProject),
    path('projects/<int:id>/', views.projectDashboard),
    path('proposals/new/', views.newProposal2),
    path('projects/<int:projectID>/portfolios/', views.selectPortfolio),
    path('projects/<int:projectID>/portfolios/<int:portfolioID>/', views.portfolioView),
    path('projects/<int:projectID>/portfolios/<int:portfolioID>/accounts/<int:accountID>/', views.accountView),
    path('projects/<int:projectID>/portfolios/<int:portfolioID>/accounts/<int:accountID>/proposals/new/', views.newProposal),
    path('proposals/<int:proposalID>/', views.viewProposal),
    path('proposals/<int:proposalID>/edit/', views.editProposal),
    path('proposals/<int:proposalID>/delete/', views.deleteProposal),
    path('portfolios/new/', views.newPortfolio),
    path('portfolios/add/', views.addPortfolio),
    path('accounts/add/', views.addAccount),
    path('security/add/', views.addSecurity),
    path('productType/add/', views.addProductType),
    path('holdings/add/', views.addHolding),
    path('lots/add/', views.addLot),
    path('admin', views.admin),
    path('logout/', views.logout),
    path('test', views.test),
]

