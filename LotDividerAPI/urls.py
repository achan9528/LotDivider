from django.urls import path, include
from LotDividerAPI import views

urlpatterns = [
    path('api/welcome/', views.TestView.as_view()),
    path('api/rest-auth/', include('rest_auth.urls')),
    path('api/rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api/projects/', views.ProjectView.as_view()),
    path('api/product-types/', views.ListProductTypesView.as_view()),
    path('api/product-types/<int:id>/', views.ProductTypeView.as_view()),
]