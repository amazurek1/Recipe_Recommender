from django.urls import path
from . import views

urlpatterns = [
    path('visuals', views.visuals, name='recipes-visuals'),
    path('', views.home, name='recipes-home'),
]
