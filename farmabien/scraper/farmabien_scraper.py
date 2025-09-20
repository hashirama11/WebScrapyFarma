# Dependencias de este Archivo
from utils.Product import Product
from utils.get_current_time import get_current_time
from utils.get_html import get_html
from bs4 import BeautifulSoup
from ..loggin_config import logger


# Configuracion de logger para mensajes de debug
# Funcion para obtener la hora actual por cada consulta exitosa


class FarmabienProductsPageScraper:
    
    # Obtener los productos del contenido HTML
    @staticmethod
    async def get_products(html_content: BeautifulSoup | None) -> list[Product]:
        products = []  # Lista para almacenar los productos

        if not html_content:  # Verificar si el contenido HTML es válido
            return products  # Retornar lista vacía

        # Buscar todos los contenedores de productos
        products_div_list = html_content.find_all("div", {"class": "product-item card"})
        if not products_div_list:
            logger.info("No se encontraron productos en Farmabien.")
            return products

        # Iterar sobre cada producto encontrado
        for index, item in enumerate(products_div_list):
            try:
                # Obtener el nombre del producto
                item_name_tag = item.find("div", {"class": "card-title h5"})
                item_name = item_name_tag.text.strip() if item_name_tag else "Nombre desconocido"

                # Obtener el precio del producto
                item_price_tag = None
                card_text_tags = item.find_all("p", {"class": "card-text"})
                for tag in card_text_tags:
                    if "Bs." in tag.text:  # Identificar el precio por su contenido
                        item_price_tag = tag
                        break

                if item_price_tag:
                    # Limpiar y convertir el precio a flotante
                    raw_price = item_price_tag.text.strip().replace("Bs.", "").replace(",", "").replace(".", "").strip()
                    try:
                        item_price = float(raw_price)/100
                    except ValueError:
                        logger.error(f"Error al convertir el precio: {raw_price}")
                        item_price = None
                else:
                    item_price = None

                # Obtener la URL del producto
                item_url_tag = item.find("a")
                if item_url_tag and "href" in item_url_tag.attrs:
                    item_url = item_url_tag.attrs["href"]
                    if not item_url.startswith("http"):  # Verificar si es un enlace relativo
                        item_url = "https://www.farmabien.com" + item_url
                else:
                    item_url = "No disponible"

                # Agregar producto a la lista
                products.append(Product(
                    id_product=index + 1,
                    name=item_name,
                    price=item_price,
                    url=item_url,
                    date=await get_current_time()
                ))

            except Exception as e:
                logger.error(f"Error procesando producto en índice {index}: {e}")
                continue  # Continuar con el siguiente producto en caso de error

        return products

    # Buscar productos en Farmabien
    async def search_product_farmabien(self, item: str) -> list[Product]:
        
        try:
            farmabien_url = f"https://www.farmabien.com/buscador/{item}"
            html_content = await get_html(farmabien_url)
            return await self.get_products(html_content)
        except Exception as e:
            logger.error(f"Error durante la búsqueda en Farmabien: {e}")
            return []
