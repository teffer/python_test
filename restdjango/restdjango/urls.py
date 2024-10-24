"""
URL configuration for restdjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from simpleorg.views import UserRegisterView, UserProfileView, UserListView, OrganizationCreateView, OrganizationListView, OrganizationDetailView, CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('organizations/', OrganizationListView.as_view(), name='organization-list'),
    path('organizations/create/', OrganizationCreateView.as_view(), name='organization-create'),
    path('organizations/<int:pk>/', OrganizationDetailView.as_view(), name='organization-detail'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
