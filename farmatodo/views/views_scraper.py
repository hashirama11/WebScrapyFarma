from asgiref.sync import async_to_sync
from rest_framework.views import APIView
from rest_framework.response import Response
from typing import List
from ..scraper.farmatodo_scraper import FarmatodoProductsPageScraper
from rest_framework import status
from ..loggin_config import logger
from ..models import ScrapyWebFarmatodo



# Obtener todos los productos resultantes de la busqueda
def fetch_products_all_farmatodo(item: str) -> list[dict]:

# Esta lógica de negocio puede ser reutilizada por diferentes métodos HTTP
    scraper_farmatodo : FarmatodoProductsPageScraper = FarmatodoProductsPageScraper()

    products : List[dict] = async_to_sync(scraper_farmatodo.search_product_farmatodo)(item)
        
    # Retorna la lista de productos filtrados
    return products

# Funcion para almacenar los resultados del scraper en la base de datos
def save_products_to_db(products: list[dict]) -> None:
    for product in products:
        try:
            # Verifica si el producto ya existe en la base de datos
            existing_product = ScrapyWebFarmatodo.objects.filter(nombre=product.name).first()
            if not existing_product:
                # Si no existe, crea un nuevo registro
                ScrapyWebFarmatodo.objects.create(
                    nombre=product.name,
                    precio=product.price,
                    url=product.url,
                    fecha=product.date,
                )
            else:
                # Si existe pero el precio ha cambiado o la fecha es diferente, crea nuevo registro
                if existing_product.precio != product.price or existing_product.fecha != product.date:
                    ScrapyWebFarmatodo.objects.create(
                        nombre=product.name,
                        precio=product.price,
                        url=product.url,
                        fecha=product.date,
                    )
        except Exception as e:
            logger.error(f"Error al guardar el producto: {e}")
   
    

# Vista que permite realizar una búsqueda de productos en Farmatodo y obtener los resultados en memoria de ejecucion
class FarmatodoGETSearchViewAll(APIView):

    # Vista para obtener todos los productos de Farmatodo
    

    def get(self, request, item: str):
        try:
            # Verifica si el parámetro 'item' está vacío
            if not item:
                raise Response({"error": "El parámetro 'item' no puede estar vacío"}, status=status.HTTP_400_BAD_REQUEST)
            # Llama al método fetch_products

            # para obtener todos los productos de la búsqueda
            products: List[dict] = fetch_products_all_farmatodo(item)

            # Guardar los datos en la base de datos
            save_products_to_db(products)

            # Retorna código 200 (OK)
            return Response(status=status.HTTP_200_OK)

        except ValueError:  # Error en la entrada de datos
            return Response({"error": "Entrada inválida"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Error interno del servidor: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



