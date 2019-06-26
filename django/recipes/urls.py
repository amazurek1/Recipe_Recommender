from django.urls import path
from . import views

urlpatterns = [
    path('vis', views.vis, name='recipes-vis'),
    path('', views.home, name='recipes-home'),
]
