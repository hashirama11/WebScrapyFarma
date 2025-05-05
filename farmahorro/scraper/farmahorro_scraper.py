# Dependencias de Archivo
from bs4 import BeautifulSoup
from .Product import Product
from playwright.async_api import async_playwright

async def get_html(url: str) -> BeautifulSoup:
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Iniciar el navegador en modo headless
        page = await browser.new_page()
        try:
            await page.goto(url)
            content = await page.content()  # Capturar el contenido HTML
            await browser.close()
            return BeautifulSoup(content, "html.parser")  # Retornar el HTML parseado
        
        except Exception as e:
            print(f"Error esperando la carga de la página: {e}")
            await browser.close()
            return None

class FarmahorroProductsPageScraper:
    
    async def get_products(self, html_content: BeautifulSoup) -> list[Product]:
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
                    item_price_cleaned = item_price_tag.text.strip().replace("Bs.", "").replace("Bs", "").replace(",", "").strip()
                    item_price = float(item_price_cleaned)

                    # Procesar URL
                    item_url = item_url_tag.attrs["href"]
                    if not item_url.startswith("http"):
                        item_url = "https://www.farmatodo.com.ve" + item_url

                    # Añadir el producto a la lista
                    products.append(Product(
                        id=index + 1,
                        name=item_name,
                        price=item_price,
                        url=item_url
                    ))
            except Exception as e:
                print(f"Error procesando item: {e}")
                pass
        return products

    async def search_product_farmahorro(self, item: str) -> list:
        farmatodo_url = f"https://farmahorro.com.ve/?s={item}"
        html_content = await get_html(farmatodo_url)
        return await self.get_products(html_content)