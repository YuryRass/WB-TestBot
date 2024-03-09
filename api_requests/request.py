"""Запрос к публичному API для получения информации о товаре по его артикулу."""

from aiohttp import ClientSession
from config import settings


class WBProduct:
    """Информация о товаре."""

    def __init__(self) -> None:
        self.product_info = {}

    async def get_info(self, item_number: int) -> dict:
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
                    return {}
                stocks = product.get("sizes")[0].get("stocks")

                self.product_info.update(
                    name=product.get("name"),
                    article_number=item_number,
                    price=product.get("salePriceU"),
                    rating=product["rating"],
                    quantity=stocks[0].get("qty") if stocks else 0,
                )
                return self.product_info
