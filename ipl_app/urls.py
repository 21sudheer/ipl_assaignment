from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/matches-per-year/', views.matches_per_year),
    path('api/matches-won/', views.matches_won_per_team),
    path('api/extra-runs/<int:year>/', views.extra_runs),
    path('api/economical-bowlers/<int:year>/', views.economical_bowlers),
    path('api/matches-played-won/<int:year>/', views.matches_played_vs_won),
]

