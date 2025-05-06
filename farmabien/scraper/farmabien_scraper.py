# Dependencias de este Archivo
from datetime import datetime
from .Product import Product
from bs4 import BeautifulSoup
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

class FarmabienProductsPageScraper:
    
    # Obtener los productos del contenido HTML
    async def get_products(self, html_content: BeautifulSoup) -> list[Product]:
        products = []  # Lista para almacenar los productos

        if not html_content:  # Verificar si el contenido HTML es válido
            return products  # Retornar lista vacía

        # Buscar todos los contenedores de productos
        products_div_list = html_content.find_all("div", {"class": "product-item card"})
        if not products_div_list:
            print("No se encontraron productos en Farmabien.")
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
                        print(f"Error al convertir el precio: {raw_price}")
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
                    id=index + 1,
                    name=item_name,
                    price=item_price,
                    url=item_url,
                    date=await get_current_time()
                ))

            except Exception as e:
                print(f"Error procesando producto en índice {index}: {e}")
                continue  # Continuar con el siguiente producto en caso de error

        return products

    # Buscar productos en Farmabien
    async def search_product_farmabien(self, item: str) -> list[Product]:
        
        try:
            farmabien_url = f"https://www.farmabien.com/buscador/{item}"
            html_content = await get_html(farmabien_url)
            return await self.get_products(html_content)
        except Exception as e:
            print(f"Error durante la búsqueda en Farmabien: {e}")
            return []
