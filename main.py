import os
import time
import threading

import schedule
import telebot
from PIL import Image
import soundfile as sf

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
bot = telebot.TeleBot(TOKEN)

images = {"what_a_week_huh": "what_a_week_huh.jpg", "adam": "adam.jpeg"}

sounds = {"cry_baby": "cry_baby.wav"}

chat_ids = []


def get_photo(image):
  path = images[image]

  if path is None:
    return None

  photo = Image.open(path)
  return photo


def get_audio(audio):
  path = sounds[audio]

  if path is None:
    return None

  audio, _ = sf.read(path)
  return audio


def send_audio(chat_id, audio):
  audio = get_audio(audio)

  if audio is None:
    return

  bot.send_audio(chat_id, audio)


def send_photo(chat_id, image):
  photo = get_photo(image)

  if photo is None:
    return

  bot.send_photo(chat_id, photo)


# Function to send a photo message to all chats
def send_photo_message_to_all():
  print("It's wednesday my dudes! Sending the photo...")
  photo = get_photo("what_a_week_huh")
  for chat_id in chat_ids:
    print(f"Sending photo to chat ID: {chat_id}")
    send_photo(chat_id, photo)


# Function to handle the testing command and send the photo
@bot.message_handler(commands=['sendphoto'])
def send_photo_message_test(message):
  chat_id = message.chat.id
  send_photo(chat_id, "what_a_week_huh")


# Function to manually trigger loading all joined chats ids
@bot.message_handler(commands=['addchat'])
def add_chat(message):
  chat_id = message.chat.id
  if chat_id not in chat_ids:
    bot.send_message(chat_id, "Adding chat to schedule")
    chat_ids.append(message.chat.id)
  else:
    bot.send_message(chat_id, "Chat is already known. Skipping.")


# Function to get all scheduled chat ids
@bot.message_handler(commands=['getchats'])
def get_chats(message):
  chat_id = message.chat.id
  bot.send_message(chat_id, f"Chat ids: {chat_ids}")


# When you need to show Adam their place
@bot.message_handler(commands=["adamejdidoprdele"])
def adam(message):
  chat_id = message.chat.id
  bot.send_message(chat_id, f"Adam!!!")
  send_photo(chat_id, "adam")


def update_listener(messages):
  for message in messages:
    chat_id = message.chat.id
    if chat_id not in chat_ids:
      print(f"Discovered new chat! Adding chat {chat_id} to schedule.")
      chat_ids.append(chat_id)


# Do not cry sweet little child
@bot.message_handler(commands=["crybaby"])
def cry_baby(message):
  chat_id = message.chat.id
  bot.send_message(chat_id, "👶")
  send_audio(chat_id, "cry_baby")


schedule.every().wednesday.at("10:00",
                              "Europe/Berlin").do(send_photo_message_to_all)


def polling_thread():
  try:
    bot.set_update_listener(update_listener)
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
  except Exception as e:
    print(f"Whoops, there has been an error: {e}")
    time.sleep(5)


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
