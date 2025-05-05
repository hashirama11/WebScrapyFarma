from bs4 import BeautifulSoup
from .Product import Product
from playwright.async_api import async_playwright
from datetime import datetime

# Funcion para obtener la hora actual por cada consulta exitosa
async def get_current_time() -> str:
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# Funcion para obtener el HTML de una página web y devolver el contenido parseado
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


# Clase para realizar el scraping de productos de Farmatodo cada vez que se realize un request
class FarmatodoProductsPageScraper:
    
    async def get_products(self, html_content: BeautifulSoup) -> list[Product]:
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
                    item_price = float(item_price_cleaned)/100

                    # Procesar URL
                    item_url = item_url_tag.attrs["href"]
                    if not item_url.startswith("http"):
                        item_url = "https://www.farmatodo.com.ve" + item_url


                    # Añadir el producto a la lista
                    products.append(Product(
                        id=index + 1,
                        name=item_name,
                        price=item_price,
                        url=item_url,
                        # Obtener la fecha actual
                        date= await get_current_time()
                    ))
            except Exception as e:
                print(f"Error procesando item: {e}")
                pass
        return products

    async def search_product_farmatodo(self, item: str) -> list:
        farmatodo_url = f"https://www.farmatodo.com.ve/buscar?product={item}"
        html_content = await get_html(farmatodo_url)

        # Crear una instancia de la clase FarmatodoProductsPageScraper
        # y llamar al método get_products
        # para obtener los productos
        products_scraper : FarmatodoProductsPageScraper = FarmatodoProductsPageScraper()
        return await products_scraper.get_products(html_content)