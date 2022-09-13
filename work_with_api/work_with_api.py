from datetime import datetime
import requests
from users_info_storage.users_info_storage import users_info_dict
from telebot.types import Message
from dbworker.dbworker import set_history


url = "https://hotels4.p.rapidapi.com/"
headers = {
	"X-RapidAPI-Key": "dfdcae03ffmsh6500f2709b7b791p162bf0jsn593c1397f57a",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"}


def request_to_api(endpoint: str, querystring: dict):
	try:
		response = requests.get(url + endpoint, headers=headers, params=querystring, timeout=10)
		if response.status_code == requests.codes.ok:
			return response
		else:
			print('Ошибка', response.status_code)
	except Exception:
		print('Ошибка', Exception)


def get_city_districts(city: str) -> dict:
	endpoint_city_id = 'locations/v2/search'
	querystring = {"query": city}
	response = request_to_api(endpoint=endpoint_city_id, querystring=querystring)
	districts = {}
	for district in response.json().get('suggestions', {})[0].get('entities'):
		districts[district['name']] = district['destinationId']
	return districts


def get_hotels(message: Message) -> dict:
	endpoint_hotels = 'properties/list'
	destination_id = users_info_dict.get(message.from_user.id)[2]['destination_id']
	check_in = users_info_dict.get(message.from_user.id)[3]['check_in']
	check_out = users_info_dict.get(message.from_user.id)[4]['check_out']
	sort_order = users_info_dict.get(message.from_user.id)[0]['hotels_price']
	hotels_num = users_info_dict.get(message.from_user.id)[5]['hotels_num']
	try:
		min_price = users_info_dict.get(message.from_user.id)[6]['min_price']
		max_price = users_info_dict.get(message.from_user.id)[7]['max_price']
		min_dist = float(users_info_dict[message.from_user.id][8]['min_dist'])
		max_dist = float(users_info_dict[message.from_user.id][9]['max_dist'])
	except IndexError:
		min_price = None
		max_price = None
		min_dist = 0
		max_dist = 1000000000000
	querystring = {
		"destinationId": destination_id,
		"pageNumber": "1",
		"pageSize": 15,
		"checkIn": check_in,
		"checkOut": check_out,
		"priceMin": min_price,
		"priceMax": max_price,
		"adults1": "1", "sortOrder": sort_order,
		"locale": "ru_RU", "currency": "USD"
	}
	response = request_to_api(endpoint=endpoint_hotels, querystring=querystring)
	hotels = response.json().get('data', {}).get('body', {}).get("searchResults", {}).get('results')

	hotels_info = {}
	hotels_count = 0

	for hotel in hotels:
		hotel_name = hotel.get("name", {})
		address = hotel.get("address", {}).get("streetAddress", {})
		dist = hotel.get("landmarks", {})[0].get("distance", {})
		rating = hotel.get("guestReviews", {}).get("rating", {})
		star_rating = hotel.get("starRating", {})
		site = hotel.get("id", {})
		price = hotel.get("ratePlan", {}).get("price", {}).get("current", {}).replace(',', '')

		float_dist = float(dist.replace(',', '.')[:3])
		if hotels_count == hotels_num:
			break
		if (hotel_name or address or dist or rating or star_rating or price) is not None and\
				min_dist <= float_dist <= max_dist:
			total_price = str(
				(datetime.strptime(check_out, '%Y-%m-%d') - datetime.strptime(check_in, '%Y-%m-%d')).days *
				int(price[1:]))
			hotels_info[hotel.get("id", {})] = (f'🏨 Название отеля: {hotel_name}\n'
												f'🌎 Адрес: {address}\n'
												f'🌇 Расстояние до центра: {dist}\n'
												f'⭐ Рейтинг от пользователей: {rating}\n'
												f'✨ Рейтинг по звёздам: {star_rating}\n'
												f'🌐 Сайт: https://www.hotels.com/ho{site}\n'
												f'1️⃣ Цена за ночь: {price}\n'
												f'💳 Цена за весь период: ${total_price}')
			hotels_count += 1
			if sort_order == 'PRICE_LOWEST_FIRST':
				command = 'Low price'
			elif sort_order == 'PRICE_HIGHEST_FIRST':
				command = 'High price'
			else:
				command = 'Best deal'

			info = (
				message.from_user.id, message.chat.id, str(datetime.today())[:19],
				users_info_dict.get(message.from_user.id)[1]['city'], hotel_name, check_in, check_out, hotels_num, command,
				min_price, max_price, dist, 'https://www.hotels.com/ho' + str(site), price, total_price)
			set_history(info)
	return hotels_info


def get_photos(hotel_id: str, photos_num: int) -> list:
	endpoint_photos = 'properties/get-hotel-photos'
	querystring = {"id": hotel_id}
	final_photos = []
	while True:
		response = request_to_api(endpoint=endpoint_photos, querystring=querystring)
		try:
			photos = response.json().get("hotelImages", {})
			break
		except AttributeError:
			photos = 'Ошибка с базой фотографий'
	for num, photo in enumerate(photos, 1):
		final_photos.append(str(photo.get('baseUrl', {})).replace('{size}', 'y'))
		if num == photos_num:
			break
	return final_photos

