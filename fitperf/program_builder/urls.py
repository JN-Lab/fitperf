from django.urls import path
from . import views

app_name = "program_builder"
urlpatterns = [
    path('dashboard/', views.homepage, name="homepage"),
]