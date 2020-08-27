
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:player_id>/', views.detail_one_player, name='detail_one_player'),
    path('<int:player1_id>/<int:player2_id>/', views.detail_two_players, name='detail_two_players'),
]