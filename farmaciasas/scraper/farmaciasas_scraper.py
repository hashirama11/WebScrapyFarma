# Dependencias de este Archivo
from bs4 import BeautifulSoup
from utils.Product import Product
from utils.get_current_time import get_current_time
from utils.get_html import get_html
from ..loggin_config import logger


class FarmaciasasProductsPageScraper:
    @staticmethod
    async def get_products(html_content: BeautifulSoup) -> list[Product]:
        products = []
        if not html_content:
            return products

        # Encuentra todos los divs de productos
        product_divs = html_content.find_all("div", {"class": "card-grid ng-star-inserted"})
        for index, item in enumerate(product_divs):
            try:
                # Extraer datos del producto
                name_tag = item.find("a", {"class": "mat-body"})
                price_tag = item.find("span", {"class": "precio"})

                item_name = name_tag.text.strip() if name_tag else None
                item_url = name_tag.get("href") if name_tag else None

                if item_url and not item_url.startswith("http"):
                    item_url = "https://tienda.farmaciasaas.com" + item_url

                raw_price = price_tag.text.strip().replace("Bs.", "").replace(",", "").replace(".", "").strip() if price_tag else None
                item_price = float(raw_price)/100 if raw_price else None

            

                # Validar y añadir producto
                if item_name and item_price and item_url:
                    products.append(Product(
                        id_product=index + 1,
                        name=item_name,
                        price=item_price,
                        url=item_url,
                        date=await get_current_time()
                    ))
            except Exception as e:
                logger.error(f"Error procesando producto: {e}")
        return products
    async def search_product_farmacias_sas(self, item: str) -> list:
        farmaciassas_url = f"https://tienda.farmaciasaas.com/buscar/{item}/0"
        html_content = await get_html(farmaciassas_url)
        return await self.get_products(html_content)