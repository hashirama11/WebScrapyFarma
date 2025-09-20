# Dependencias de Archivo
from bs4 import BeautifulSoup

from utils.Product import Product
from utils.get_html import get_html
from utils.product_dinamic import product_dinamic
from ..loggin_config import logger


class FarmahorroProductsPageScraper:
    @staticmethod
    async def get_products(html_content: BeautifulSoup) -> list[Product]:
        products = []
        if not html_content:
            return products

        # Encuentra todos los divs con productos
        products_div_list = html_content.find_all("li", {"class": "product type-product post-6817 status-publish first instock product_cat-analgesicos-antipireticos product_tag-calox has-post-thumbnail product-type-simple __web-inspector-hide-shortcut__"})
        for index, item in enumerate(products_div_list):
            try:
                item_name_tag = item.find("h2", {"class": "woocommerce-loop-product__title"})
                item_price_tag = item.find("span", {"class": "woocommerce-Price-currencySymbol"})
                item_url_tag = item.find("a", {"url": "woocommerce-LoopProduct-link woocommerce-loop-product__link"})

                if item_name_tag and item_price_tag and item_url_tag:
                    item_name = item_name_tag.text.strip()
                    
                    # Limpiar y convertir precio
                    item_price_cleaned = item_price_tag.text.strip().replace("Bs.", "").replace("Bs", "").replace(".", "").replace(",", "").strip()

                    # Procesar URL
                    item_url = item_url_tag.attrs["href"]
                    if not item_url.startswith("http"):
                        item_url = "https://www.farmatodo.com.ve" + item_url


                    await product_dinamic(item_price_cleaned, item_url, index, item_name)
            except Exception as e:
                logger.error(f"Error procesando item: {e}")
                pass
        return products

    async def search_product_farmahorro(self, item: str) -> list:
        farmatodo_url = f"https://farmahorro.com.ve/?s={item}"
        html_content = await get_html(farmatodo_url)
        return await self.get_products(html_content)