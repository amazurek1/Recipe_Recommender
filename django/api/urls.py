from django.urls import path
from .views import recipes, recommendations

urlpatterns = [
    path('recipes', recipes, name='recipes'),
    path('recs', recommendations, name='recommendations'),
]