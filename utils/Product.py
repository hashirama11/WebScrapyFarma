
class Product:
    def __init__(self, id_product: int, name: str, price: float, url: str, date : str) -> None:
        self.id : int = id_product
        self.name : str = name
        self.price : float= price
        self.url : str = url
        self.date : str = date
        
        
        
    def __str__(self):
        return f"Producto: {self.name} - Precio: {self.price} - URL: {self.url} - Fecha: {self.date}"
   