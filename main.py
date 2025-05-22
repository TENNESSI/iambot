from telethon import TelegramClient, events
from config import api_id, api_hash, api_key
import asyncio

client = TelegramClient('test_session', api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def message_handler(event):
	sender = await event.get_sender()
	
	#Проверка является ли сообщение личным сообщением от пользователя
	# if event.is_private and sender.id == 1020139714:
	if event.is_private:
		#присвоение переменным айди, имя, текст сообщения их значений
		user_id = sender.id
		name = sender.first_name
		message_text = event.text

		#Вывод в консоль всех личных сообщений
		print(f'[Сообщение] от {name}: {message_text}')
		
		time_to_read = len(message_text) / 15 #Вычисление времени чтения сообщения
		time_to_typing = len(answer_message) / 4 #Вычисление времени печатаня ответа
		
		await asyncio.sleep(time_to_read) #афк время, имитация чтения сообщения

		#статус "печатает..."
		async with client.action(user_id, 'typing'):
			await asyncio.sleep(time_to_typing)

		#отправка ответа
		await event.reply(f'Бот:\n{event.text}\nна её трупе растёт сад')


async def main():
	await client.start()
	print('Бот запущен.')
	await client.run_until_disconnected()

if __name__ == '__main__':
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print('\nБот остановлен!!')