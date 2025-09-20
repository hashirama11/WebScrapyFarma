from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from utils.loggin_config import logger


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
            logger.error(f"Error esperando la carga de la página: {e}")
            await browser.close()
            return None
