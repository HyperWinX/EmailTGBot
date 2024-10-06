import stats
import telebot
import creds
import logging
import psutil
import html
import os

def __save_ids() -> None:
  with open("ids.dat", "w") as file:
    for id in IDs:
      file.write(f"{id[0]} - {id[1]}\n")

def __read_ids() -> list[str]:
  file = None
  try:
    file = open("ids.dat", "r")
  except OSError:
    return []
  
  result = []
  lines = file.readlines()
  breakpoint()
  for line in lines:
    if (len(line) < 4):
      continue
    splitted = line.split(" - ")
    result.append((int(splitted[0]), int(splitted[1][:-1])))
  return result

def __check_root_user(id: int) -> bool:
  return ROOT_USER_ID == id


bot: telebot.TeleBot = telebot.TeleBot(creds.TOKEN)
IDs: list[str] = []
ROOT_USER_ID: int = str(creds.ROOT_ID)
logger: logging.Logger = None
IDs = __read_ids()


@bot.message_handler(commands=['start'])
def welcome(message: telebot.types.Message):
  bot.send_message(message.chat.id, "Hello! I'm email forwarding bot, developed for... someone. Happy using!\nType \"/help\" to get more info about usage.")

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
  bot.send_message(message.chat.id, "/register - register new chat for sending emails\nThat's all i can do rn:)")

@bot.message_handler(commands=['register'])
def register_group(message: telebot.types.Message):
  IDs.append((message.chat.id, message.message_thread_id))
  logger.info("Registered new ID")
  bot.send_message(chat_id=IDs[-1][0], message_thread_id=IDs[-1][1], text="I noticed new chat! Now i'm going to send everything here.")

@bot.message_handler(commands=['stop'])
def stop(message: telebot.types.Message):
  if (message.from_user is not None and __check_root_user(message.from_user.id)):
    logger.warning(f"User \"{message.from_user.full_name}\" tried to use root command. Request blocked")
    return
  bot.send_message(message.chat.id, message_thread_id=message.message_thread_id, text="Terminating bot...")
  logger.warning("Stopping bot...")
  __save_ids()
  bot.stop_bot()
  psutil.Process(os.getpid()).terminate()

@bot.message_handler(commands=["status"])
def status(message: telebot.types.Message):
  bot.send_message(message.chat.id, f"```\n{html.escape(stats.get_stats())}\n```", parse_mode="MarkdownV2")