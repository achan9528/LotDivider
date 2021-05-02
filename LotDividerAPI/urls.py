from django.urls import path, include
from LotDividerAPI import views

urlpatterns = [
    path('api/welcome/', views.TestView.as_view()),
    path('api/rest-auth/', include('rest_auth.urls')),
    path('api/rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api/projects/', views.ProjectView.as_view()),
    path('api/product-types/', views.ListProductTypesView.as_view()),
    path('api/product-types/<int:id>/', views.ProductTypeView.as_view()),
    path('api/securities/', views.ListSecurityTypesView.as_view()),
    path('api/securities/<int:id>/', views.SecurityView.as_view()),
    path('api/clients/', views.ListClientView.as_view()),
    path('api/clients/<int:id>/', views.ClientView.as_view()),
    # path('api/portfolios/', views.ListPortfolioView.as_view()),
    # path('api/portfolios/<int:id>', views.PortfolioView_asView()),

]