import telebot.async_telebot
import creds
import logging

bot = telebot.TeleBot(creds.TOKEN)
IDs = []
logger: logging.Logger = None

@bot.message_handler(commands=['start'])
def welcome(message):
  bot.send_message(message.chat.id, "Hello! I'm email forwarding bot, developed for... someone. Happy using!\nType \"/help\" to get more info about usage.")

@bot.message_handler(commands=['help'])
def help(message):
  bot.send_message(message.chat.id, "/register - register new chat for sending emails\nThat's all i can do rn:)")

@bot.message_handler(commands=['register'])
def register_group(message: telebot.types.Message):
  IDs.append((message.chat.id, message.message_thread_id))
  logger.info("Registered new ID")
  bot.send_message(chat_id=IDs[-1][0], message_thread_id=IDs[-1][1], text="I noticed new chat! Now i'm going to send everything here.")
