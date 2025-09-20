from bs4 import BeautifulSoup

from utils.Product import Product
from utils.get_current_time import get_current_time

async def product_dinamic(monto: str, item_url: str, index: int, item_name: str):
    products = []

    item_price = float(monto) / 100

    # Añadir el producto a la lista
    products.append(Product(
        id_product=index + 1,
        name=item_name,
        price=item_price,
        url=item_url,
        date=await get_current_time()
    ))