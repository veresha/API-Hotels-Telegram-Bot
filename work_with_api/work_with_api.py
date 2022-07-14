import requests
from users_info_storage.users_info_storage import users_info_dict
from telebot.types import Message
import json
import re
from loguru import logger

url = "https://hotels4.p.rapidapi.com/"
headers = {
	"X-RapidAPI-Key": "79b22035d4msh81e225cd5d7c59dp106dccjsn38e17a5d4d9b",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"}


def request_to_api(endpoint, querystring):
	try:
		logger.debug('Запрос к апи')
		response = requests.get(url + endpoint, headers=headers, params=querystring, timeout=10)
		logger.debug('Ответ получен')
		if response.status_code == requests.codes.ok:
			logger.debug('Проверка статус кода и возврат ответа')
			return response
		else:
			print('Ошибка ', response.status_code)
	except Exception:
		print('Ошибка.', Exception)


def get_city_districts(city: str) -> dict:
	endpoint_city_id = 'locations/v2/search'
	querystring = {"query": city}
	response = request_to_api(endpoint=endpoint_city_id, querystring=querystring)
	districts = {}
	for district in response.json()['suggestions'][0]['entities']:
		districts[district['name']] = district['destinationId']
	return districts


def get_hotels(message: Message, hotels_num: int) -> dict:
	endpoint_hotels = 'properties/list'
	check_in = users_info_dict[message.from_user.id][3]['check_in']
	check_out = users_info_dict[message.from_user.id][4]['check_out']
	price = users_info_dict[message.from_user.id][0]['hotels_price']
	querystring = {
		"destinationId": users_info_dict[message.from_user.id][2]['destination_id'], "pageNumber": "1",
		"pageSize": hotels_num, "checkIn": check_in, "checkOut": check_out, "adults1": "1", "sortOrder": price,
		"locale": "ru_RU", "currency": "USD"
	}
	logger.debug('Запрос к апи')
	response = request_to_api(endpoint=endpoint_hotels, querystring=querystring)
	logger.debug('Получение ответа от апи')
	hotels = response.json()['data']['body']["searchResults"]['results']
	hotels_info = {}
	for hotel in hotels:
		try:
			hotels_info[hotel['id']] = f'Название отеля: {hotel["name"]}\n'\
									f'Адрес: {hotel["address"]["streetAddress"]}\n'\
									f'Расстояние до центра: {hotel["landmarks"][0]["distance"]}\n'\
									f'Рейтинг от пользователей: {hotel["guestReviews"]["rating"]}\n'\
									f'Рейтинг по звёздам: {hotel["starRating"]}\n'\
									f'Цена за ночь: {hotel["ratePlan"]["price"]["current"]}'
		except KeyError:
			print('Отсутствует ключ')
			########################
	return hotels_info


def get_photos(hotel_id, photos_num) -> list:
	endpoint_photos = 'get-hotel-photos'
	querystring = {"id": hotel_id}
	response = request_to_api(endpoint=endpoint_photos, querystring=querystring)
	photos = []
	for photo in response.json()["hotelImages"]:
		photos.append(str(photo['baseUrl']).replace('{size}', 'y'))
	return photos

