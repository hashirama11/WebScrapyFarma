from django.urls import path
from .views.views_scraper import FarmatodoGETSearchViewAll

urlpatterns = [
    # URL para obtener todos los productos de Farmatodo
    path('api/farmatodo/search/<str:item>/', FarmatodoGETSearchViewAll.as_view(), name='farmatodo_search_all'),
]