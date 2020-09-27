from django.contrib import admin
from django.urls import path, include

from rest_framework  import routers

from . import views

router = routers.DefaultRouter()
router.register('memo', views.MemoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('refrigerator/', views.RefrigeratorDetailView.as_view()),
    path('item/', views.ItemListView.as_view()),
    path('item/<int:pk>/',views.ItemDetailView.as_view()),
    path('basicitem/', views.BasicItemListView.as_view()),
    path('basicitem/<int:pk>/',views.BasicItemDetailView.as_view()),
]
