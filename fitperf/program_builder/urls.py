from django.urls import path
from . import views

app_name = "program_builder"
urlpatterns = [
    path('dashboard/', views.homepage, name="homepage"),
    path('movements/', views.movements_list, name="movements_list"),
    path('delete-movement/<movement_pk>', views.delete_movement, name="delete_movement"),
    path('exercices/', views.exercises_list, name="exercises_list"),
    path('exercise/<exercise_pk>', views.exercise_page, name="exercise_page")
]