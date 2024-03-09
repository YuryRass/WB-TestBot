"""Различные выражения для Tg бота"""
from enum import Enum

class WBLexicon(str, Enum):
    GetInfo = 'get_info'
    GetInfoFromBD = 'get_info_from_bd'
    StopNotifications = 'stop_notifications'


LEXICON: dict[str, str] = {
    '/start': 'Это бот, который поможет узнать информацию о товаре по его артикулу '
              'на сайте WildBerries\n\nЧтобы посмотреть список доступных '
              'команд - наберите /help',
    '/help': 'Это <b>бот-информатор.</b> С его помощью можно узнать информацию '
             'о товаре с WildBerries: название, артикул, цена, рейтинг товара, '
             'количество товара на всех складах',
    WBLexicon.GetInfo: 'Получить информацию по товару',
    WBLexicon.GetInfoFromBD: 'Получить информацию из БД',
    WBLexicon.StopNotifications: 'Остановить уведомления'

}
