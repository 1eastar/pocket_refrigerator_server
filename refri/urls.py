from django.contrib import admin
from django.urls import path, include

from rest_framework  import routers

from . import views

router = routers.DefaultRouter()
router.register('item', views.ItemViewSet)
router.register('basicitem', views.BasicItemViewSet)
router.register('memo', views.MemoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('refrigerator/', views.RefrigeratorDetailView.as_view()),
]
