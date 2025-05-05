from django.urls import path
from .views.views_locatel import LocatelGETSearchViewAll

urlpatterns = [
    # URL para obtener todos los productos de Farmatodo
    path('api/locatel/search/<str:item>/', LocatelGETSearchViewAll.as_view(), name='locatel_search_all'),
]