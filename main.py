import os
import time
import threading

import schedule
import telebot
from PIL import Image

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
IMAGE = "what_a_week_huh.jpg"
bot = telebot.TeleBot(TOKEN)

chat_ids = []


def get_photo():
  photo = Image.open(IMAGE)
  return photo


# Function to send a photo message to all chats
def send_photo_message_to_all():
  print("It's wednesday my dudes! Sending the photo...")
  photo = get_photo()
  for chat_id in chat_ids:
    print(f"Sending photo to chat ID: {chat_id}")
    bot.send_photo(chat_id, photo)


# Function to handle the testing command and send the photo
@bot.message_handler(commands=['sendphoto'])
def send_photo_message_test(message):
  chat_id = message.chat.id
  photo = get_photo()
  bot.send_photo(chat_id, photo)


# Function to manually trigger loading all joined chats ids
@bot.message_handler(commands=['addchat'])
def add_chat(message):
  chat_id = message.chat.id
  bot.send_message(chat_id, "Adding chat to schedule")
  chat_ids.append(message.chat.id)


# Function to get all scheduled chat ids
@bot.message_handler(commands=['getchats'])
def get_chats(message):
  chat_id = message.chat.id
  bot.send_message(chat_id, f"Chat ids: {chat_ids}")


def update_listener(messages):
  for message in messages:
    chat_id = message.chat.id
    if chat_id not in chat_ids:
      print(f"Discovered new chat! Adding chat {chat_id} to schedule.")
      chat_ids.append(chat_id)


schedule.every().wednesday.at("10:00",
                              "Europe/Berlin").do(send_photo_message_to_all)


def polling_thread():
  bot.set_update_listener(update_listener)
  bot.polling(non_stop=True)


def schedule_thread():
  while True:
    schedule.run_pending()
    time.sleep(30)


bot_thread = threading.Thread(target=polling_thread)
schedule_thread = threading.Thread(target=schedule_thread)

bot_thread.start()
schedule_thread.start()

bot_thread.join()
schedule_thread.join()
