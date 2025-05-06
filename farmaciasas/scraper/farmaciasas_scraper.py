# Dependencias de este Archivo
from datetime import datetime
from bs4 import BeautifulSoup
from .Product import Product
from playwright.async_api import async_playwright


# Funcion para obtener la hora actual por cada consulta exitosa
async def get_current_time() -> str:
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

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

class Farmacia_sasProductsPageScraper:
    
    async def get_products(self, html_content: BeautifulSoup) -> list[Product]:
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
                        id=index + 1,
                        name=item_name,
                        price=item_price,
                        url=item_url,
                        date=await get_current_time()
                    ))
            except Exception as e:
                print(f"Error procesando producto: {e}")
        return products
    async def search_product_farmacias_sas(self, item: str) -> list:
        farmaciassas_url = f"https://tienda.farmaciasaas.com/buscar/{item}/0"
        html_content = await get_html(farmaciassas_url)
        return await self.get_products(html_content)