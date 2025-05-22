from telethon import TelegramClient, events
from config import api_id, api_hash, api_key
import asyncio
from openai import OpenAI
import os
import json

#инициализация телеграма и нейронки
tg_client = TelegramClient('test_session', api_id, api_hash)
ai_client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

@tg_client.on(events.NewMessage(incoming=True))
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

		if os.path.exists(f'data/{user_id}.json') == False:
			with open(f'data/{user_id}.json', 'w') as f:
				with open('data/system.txt', 'r') as file:
					content = file.read()
					messages = [{"role": "system", "content": content}]
				json.dump(messages, f, indent=4)

		with open(f'data/{user_id}.json', 'r') as f:
			messages = json.load(f)
		messages.append({'role': 'user', 'content': f'{name}: {message_text}'})
		response = ai_client.chat.completions.create(
		    model="deepseek-chat",
		    messages=messages,
		    stream=False
		)
		answer_message = response.choices[0].message.content
		messages.append({'role': 'assistant', 'content': answer_message})

		#Вывод в консоль ответа бота
		print(f'[Ответ бота]: {answer_message}')

		with open(f'data/{user_id}.json', 'w') as f:
			json.dump(messages, f, indent=4)
		
		time_to_read = len(message_text) / 15 #Вычисление времени чтения сообщения
		time_to_typing = len(answer_message) / 4 #Вычисление времени печатаня ответа
		
		await asyncio.sleep(time_to_read) #афк время, имитация чтения сообщения

		#статус "печатает..."
		async with tg_client.action(user_id, 'typing'):
			await asyncio.sleep(time_to_typing)

		#отправка ответа
		await tg_client.send_message(user_id, answer_message)
	else:
		print('event is not private')


async def main():
	await tg_client.start()
	print('Бот запущен.')
	await tg_client.run_until_disconnected()

if __name__ == '__main__':
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print('\nБот остановлен!!')