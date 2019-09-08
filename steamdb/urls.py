from django.urls import path

from . import views

app_name = "steamdb"

urlpatterns = [
    path('summary/', views.app_summary, name="app_summary"),
    path('detail/<int:app_id>/', views.app_detail, name="app_detail"),
    path('edit/<int:app_id>/', views.app_edit, name="app_edit"),
    path('add/', views.app_add, name="app_add"),
    path('delete/<int:app_id>/', views.app_delete, name="app_delete"),
]
