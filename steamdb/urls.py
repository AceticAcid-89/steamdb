from django.urls import path

from . import views

app_name = "steamdb"

urlpatterns = [
    path('summary/', views.game_summary, name="game_summary"),
    path('detail/<int:game_id>/', views.game_detail, name="game_detail"),
]
