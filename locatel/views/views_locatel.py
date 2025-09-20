from typing import List
from asgiref.sync import async_to_sync
from rest_framework.views import APIView
from rest_framework.response import Response
from ..scraper.locatel_scraper import LocatelProductsPageScraper
from ..models import ScrapyWebLocatel
from rest_framework import status
from utils.loggin_config import logger

# Obtener todos los productos resultantes de la busqueda
def fetch_products_all_locatel(item: str) -> list[dict]:

    # Esta lógica de negocio puede ser reutilizada por ambos métodos
    scraper_locatel: LocatelProductsPageScraper = LocatelProductsPageScraper()

    products : list[dict] = async_to_sync(scraper_locatel.search_product_locatel)(item)
        
    # Retorna la lista de productos filtrados
    return products  

# Funcion para almacenar los resultados del scraper en la base de datos
def save_products_to_db(products: list[dict]) -> None:
    for product in products:
        try:
            # Verifica si el producto ya existe en la base de datos
            existing_product = ScrapyWebLocatel.objects.filter(nombre=product.name).first()
            if not existing_product:
                # Si no existe, crea un nuevo registro
                ScrapyWebLocatel.objects.create(
                    nombre=product.name,
                    precio=product.price,
                    url=product.url,
                    fecha=product.date,
                )
            else:
                # Si existe, pero el precio ha cambiado o la fecha es diferente, crea nuevo registro
                if existing_product.precio != product.price or existing_product.fecha != product.date:
                    ScrapyWebLocatel.objects.create(
                        nombre=product.name,
                        precio=product.price,
                        url=product.url,
                        fecha=product.date,
                    )
        except Exception as e:
            logger.error(f"Error al guardar el producto: {e}")
        
# Vista que ejecuta el scraper de locatel
class LocatelGETSearchViewAll(APIView):
 
    # Vista para obtener todos los productos de Locatel
    @staticmethod
    def get(request, item: str):
        try:
            # Verifica si el parámetro 'item' está vacío
            if not item:
                raise Response({"error": "El parámetro 'item' no puede estar vacío"}, status=status.HTTP_400_BAD_REQUEST)
            # Llama al método fetch_products

            # para obtener todos los productos de la búsqueda
            products: List[dict] = fetch_products_all_locatel(item)

            # Guardar los datos en la base de datos
            save_products_to_db(products)

            # Retorna código 200 (OK)
            return Response(status=status.HTTP_200_OK)

        except ValueError:  # Error en la entrada de datos
            return Response({"error": "Entrada inválida"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Error interno del servidor: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
