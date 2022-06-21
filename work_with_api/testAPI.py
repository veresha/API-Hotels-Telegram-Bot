import requests
# from users_info_storage.users_info_storage import users_info_dict
# from telebot.types import Message
# from load_bot import bot
# from states.user_state import UserState


def main():
# @bot.message_handler(state=UserState.work_with_api)
# def getting_hotels(message: Message):
	url = "https://hotels4.p.rapidapi.com/"
	endpoint_city_id = 'locations/v2/search'
	city = 'boston' #users_info_dict[message.from_user.id]['city']

	querystring = {"query": city}
	headers = {
		"X-RapidAPI-Key": "27c3b873d3msh5961c422d735f01p1d55e2jsne5957d6966a4",
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
	}
	response = requests.request("GET", url + endpoint_city_id, headers=headers, params=querystring)
	destinationid = response.json()['suggestions'][0]['entities'][0]['destinationId']

	###################

	endpoint_hotels = 'properties/list'
	check_in = '2022-12-10' #users_info_dict[message.from_user.id]['check_in']
	check_out = '2022-12-15' #users_info_dict[message.from_user.id]['check_out']
	price = 'PRICE_LOWEST_FIRST' #users_info_dict[message.from_user.id]['hotels_price']
	hotels_num = '3' #users_info_dict[message.from_user.id]['hotels_num']
	querystring = {
		"destinationId": destinationid, "pageNumber": "1", "pageSize": hotels_num, "checkIn": check_in,
		"checkOut": check_out, "adults1": "1", "sortOrder": price, "locale": "en_US", "currency": "USD"
	}
	response = requests.request("GET", url + endpoint_hotels, headers=headers, params=querystring)

	hotels = response.json()['data']['body']["searchResults"]['results']

	for i in hotels:
		print(i['name'])
		print(i['guestReviews']['rating'])
		print(i['ratePlan']['price']['current'])
		print('***********')


if __name__ == '__main__':
	main()
