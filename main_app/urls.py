from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('finches/', views.finch_index, name='index'),
  path('finches/<int:finch_id>/', views.finch_detail, name='detail'),
  path('finches/create/', views.FinchCreate.as_view(), name='finch_create'),
  path('finches/<int:pk>/update/', views.FinchUpdate.as_view(), name='finch_update'),
  path('finches/<int:pk>/delete/', views.FinchDelete.as_view(), name='finch_delete'),
]
