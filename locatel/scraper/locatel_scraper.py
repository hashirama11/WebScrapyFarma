# Dependencias del Archivo
from rest_framework.views import APIView

from utils.get_current_time import get_current_time
from utils.get_html import get_html
from utils.Product import Product
from typing import List, Optional
from bs4 import BeautifulSoup
from utils.loggin_config import logger

class LocatelProductsPageScraper(APIView):
    @staticmethod
    async def get_products(html_content: Optional[BeautifulSoup]) -> List[Product]:
        products: List[Product] = []  # Lista para almacenar los productos

        if not html_content:  # Validar si el contenido HTML es válido
            return products  # Retornar lista vacía

        # Buscar todos los contenedores de productos
        products_div_list = html_content.find_all(
            "div", {"class": "vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryItem--normal pa4"}
        )
        if not products_div_list:
            logger.info("No se encontraron productos en Locatel.")
            return products

        # Iterar sobre cada producto encontrado
        for index, item in enumerate(products_div_list):
            try:
                # Obtener el nombre del producto
                item_name_tag = item.find(
                    "span",
                    {
                        "class": "vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-productBrand--NombreProducto vtex-product-summary-2-x-brandName vtex-product-summary-2-x-brandName--NombreProducto t-body"},
                )
                item_name: str = item_name_tag.text.strip() if item_name_tag else "Nombre desconocido"

                # Obtener el precio del producto
                item_price_tag = item.find(
                    "span",
                    {
                        "class": "vtex-product-price-1-x-currencyInteger vtex-product-price-1-x-currencyInteger--VitrinaProductoPrecioVenta"},
                )
                item_price: Optional[float] = None
                if item_price_tag:
                    raw_price: str = item_price_tag.text.strip().replace(",", "").replace("BS", "").replace(".",
                                                                                                            "").strip()
                    try:
                        item_price = float(raw_price) / 100
                    except ValueError:
                        print(f"Error al convertir el precio: {raw_price}")

                # Obtener la URL del producto
                item_url_tag = item.find("a", {
                    "class": "vtex-product-summary-2-x-clearLink vtex-product-summary-2-x-clearLink--VitrinaPrincipal h-100 flex flex-column"})
                item_url: str = "No disponible"
                if item_url_tag and "href" in item_url_tag.attrs:
                    item_url = item_url_tag.attrs["href"]
                    if not item_url.startswith("http"):  # Comprobar si es un enlace relativo
                        item_url = "https://www.locatel.com.ve" + item_url

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

    async def search_product_locatel(self, item: str) -> List[Product]:
        try:
            locatel_url: str = f"https://www.locatel.com.ve/{item}?_q={item}&map=ft"
            html_content: Optional[BeautifulSoup] = await get_html(locatel_url)
            return await self.get_products(html_content)
        except Exception as e:
            logger.error(f"Error durante la búsqueda en Locatel: {e}")
            return []


