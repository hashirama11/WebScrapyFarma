from bs4 import BeautifulSoup
from utils.Product import Product
from utils.get_html import get_html
from utils.product_dinamic import product_dinamic
from ..loggin_config import logger



# Clase para realizar el scraping de productos de Farmatodo cada vez que se realize un request
class FarmatodoProductsPageScraper:
    @staticmethod
    async def get_products(html_content: BeautifulSoup) -> list[Product]:

        products = []
        if not html_content:
            return products

        # Encuentra todos los divs con productos
        products_div_list = html_content.find_all("div", {"class": "card-ftd"})
        for index, item in enumerate(products_div_list):
            try:
                item_name_tag = item.find("p", {"class": "text-title"})
                item_price_tag = item.find("span", {"class": "price__text-price"})
                item_url_tag = item.find("a", {"class": "product-image__link"})

                if item_name_tag and item_price_tag and item_url_tag:
                    item_name = item_name_tag.text.strip()
                    
                    # Limpiar y convertir precio
                    item_price_cleaned = item_price_tag.text.strip().replace("Bs.", "").replace("Bs", "").replace(",", "").replace(".","").strip()

                    item_url = item_url_tag.attrs["href"]
                    if not item_url.startswith("http"):
                        item_url = "https://www.farmatodo.com.ve" + item_url

                    await product_dinamic(item_price_cleaned, item_url, index, item_name)

            except Exception as e:
                logger.error(f"Error procesando item: {e}")
                pass
        return products

    @staticmethod
    async def search_product_farmatodo(item: str) -> list:
        farmatodo_url = f"https://www.farmatodo.com.ve/buscar?product={item}"
        html_content = await get_html(farmatodo_url)

        # Crear una instancia de la clase FarmatodoProductsPageScraper
        # y llamar al método get_products
        # para obtener los productos
        products_scraper : FarmatodoProductsPageScraper = FarmatodoProductsPageScraper()
        return await products_scraper.get_products(html_content)