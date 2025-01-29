"""
URL configuration for dgcart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', CustomerRegistrationAPIView.as_view(), name='customer-register'),
    path('customer/<str:phone>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('api/login/', CustomerLoginAPIView.as_view(), name='customer-login'),
    path('api/staff/login/', StaffLoginAPIView.as_view(), name='staff-login'),
    path('api/products/', ProductListAPIView.as_view(), name='product-list'),
    path('api/products/add/', ProductCreateAPIView.as_view(), name='product-create'),
    path('api/products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('api/products/<int:pk>/update/', ProductUpdateAPIView.as_view(), name='product-update'),
    path('api/products/<int:pk>/delete/', ProductDeleteAPIView.as_view(), name='product-delete'),
    path('api/products/<int:pk>/update-stock/', ProductStockUpdateAPIView.as_view(), name='product-stock-update'),
    path('api/complaints/submit/', SubmitComplaintAPI.as_view(), name='submit_complaint_api'),
    path('api/complaints/', ComplaintListAPI.as_view(), name='complaint_list_api'),
]
