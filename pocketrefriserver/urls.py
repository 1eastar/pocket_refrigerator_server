"""pocketrefriserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import permissions
from rest_framework.authtoken import views

schema_view = get_schema_view(
   openapi.Info(
      title="pocket_refrigerator",
      default_version='v1',
      description="REST API for pocket refri",
      terms_of_service="https://www.google.com/",
      contact=openapi.Contact(email="ehdwls6703@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.IsAdminUser,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth', views.obtain_auth_token),
    path('common/', include('common.urls')),
    path('recipe/', include('recipe.urls')),
    path('refri/', include('refri.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('users/', include('rest_auth.urls')),  # rest auth 'REST_AUTH_JWT=True' 설정 안 하면 기본 Token 모델 사용 / 모듈 내부에서 기본 토큰 자동 생성해줌(receiver 필요x)
    path('users/registration/', include('rest_auth.registration.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
