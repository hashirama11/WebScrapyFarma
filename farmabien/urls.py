from django.urls import path
from .views.views_farmabien import FarmabienGETSearchViewAll

urlpatterns = [
    # URL para obtener todos los productos de Farmatodo
    path('api/farmabien/search/<str:item>/', FarmabienGETSearchViewAll.as_view(), name='farmabien_search_all'),
]