"""Запрос к публичному API для получения информации о товаре по его артикулу."""

from aiohttp import ClientSession
from config import settings
from lexicon import WBInfo


class WBProduct:
    """Информация о товаре."""

    def __init__(self) -> None:
        self.product_info = {}

    async def get_info(self, item_number: int) -> str:
        """Получение информации о товаре в JSON формате."""
        payload: dict[str, str] = {
            "appType": 1,
            "curr": "rub",
            "dest": -1257786,
            "spp": 30,
            "nm": item_number,
        }
        async with ClientSession() as session:
            async with session.get(
                url=str(settings.URL),
                params=payload,
            ) as response:
                # Название, артикул, цена, рейтинг товара, количество товара
                res = await response.json()
                product = res.get("data").get("products")
                if product:
                    product = product[0]
                else:
                    return ""
                stocks = product.get("sizes")[0].get("stocks")
                try:
                    price = int(product.get("salePriceU") / 100)
                except:
                    price = 0

                self.product_info = {
                    WBInfo.name: product.get("name"),
                    WBInfo.article_number: item_number,
                    WBInfo.price: price,
                    WBInfo.rating: product["rating"],
                    WBInfo.quantity: stocks[0].get("qty") if stocks else 0,
                }
                res_info = "\n".join(f"{k}{val}" for k, val in self.product_info.items())
                return res_info
