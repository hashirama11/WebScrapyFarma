from django.urls import path
from .views.views_farmacia_sas import Farmacia_sasGETSearchViewAll

urlpatterns = [
    # URL para obtener todos los productos de Farmatodo
    path('api/farmaciasas/search/<str:item>/', Farmacia_sasGETSearchViewAll.as_view(), name='farmaciasas_search_all'),
]