from django.contrib import admin
from django.urls import path, include

from rest_framework  import routers

from . import views

router = routers.DefaultRouter()
router.register('notice', views.NoticeViewSet)
router.register('barcode', views.BarcodeViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('checkUserAuth/', views.check_user_auth),
    path('verify/', views.verify),
    path('signup/', views.signup),
    path('signin/', views.signin),
    path('userDetail/', views.UserDetailView.as_view()),
    path('getbarcode/', views.get_barcode_data),
    # path('setbarcode/', views.set_barcode_data),
    path('report/', views.report),
    path('icons/', views.getIconList),
]
