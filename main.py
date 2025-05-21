from telethon import TelegramClient, events
from config import api_id, api_hash
import asyncio

client = TelegramClient('test_session', api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def message_handler(event):
	sender = await event.get_sender()
	print(f'[Сообщение] от {sender.first_name}: {event.text}')

	if event.is_private and sender.id == 1020139714:
		await asyncio.sleep(3)
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