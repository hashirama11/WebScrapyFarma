from django.urls import path
from .views.views_farmahorro import FarmahorroGETSearchViewAll

urlpatterns = [
    # URL para obtener todos los productos de Farmatodo
    path('api/farmahorro/search/<str:item>/', FarmahorroGETSearchViewAll.as_view(), name='farmahorro_search_all'),
]