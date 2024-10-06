import email_parser as ep
import creds
import bot
import time
import shutil
import threading
import bot_logger
import telebot
import html

TIMEOUT: int = 5

logger = bot_logger.get_console_logger()
err_logger = bot_logger.get_dual_logger()

email_handler = ep.EmailHandler(creds.EMAIL, creds.PASSWD, logger)

def main_loop():
  if (len(bot.IDs) == 0):
    return
  global logger
  mails = email_handler.check()
  logger.info(f"Emails check complete, new emails count: {len(mails)}")

  if (len(mails) == 0):
    return
  
  for mail in mails:
    message = "Вы получили новое сообщение!\n\n"
    message += f"- <b>От кого:</b> {html.escape(mail.from_)}\n"
    message += f"- <b>Тема:</b> {html.escape(mail.subject)}\n"
    if (len(mail.body) > 2):
      message += f"- <b>Текст</b>: \n<blockquote expandable>{html.escape(mail.body)}</blockquote>\n\n"
    if (len(mail.filenames) > 0):
      message += f"<b>Найдено вложений:</b> {len(mail.filenames)}\n"
    
    for chat in bot.IDs:
      msg_sent: bool = False
      while (not msg_sent):
        try:
          bot.bot.send_message(chat_id=chat[0], message_thread_id=chat[1], text=message, parse_mode="HTML")
          msg_sent = True
        except telebot.apihelper.ApiTelegramException as err:
          raise err
      for filename in mail.filenames:
        while True:
          try:
            bot.bot.send_document(chat_id=chat[0], message_thread_id=chat[1], document=open(filename, "rb"), timeout=60)
          except telebot.apihelper.ApiTelegramException as err:
            logger.info(f"Telegram API error: \"{err.description}\", retrying...")
            continue
          except Exception:
            err_logger.error("\nDEVELOPER, LOOK HERE")
          break
          
    if (len(mail.filenames) > 0):
      shutil.rmtree(mail.filenames[0].split('/')[0])
      logger.info("Removed attachments folder")
    email_handler.mark_read(mail.id)
  email_handler.remove_seen()
  logger.info("Removed all seen emails")
      
logger.info("Initializing bot")
bot.logger = logger
bot_thread = threading.Thread(target=bot.bot.infinity_polling)
bot_thread.start()
logger.info("Entering main loop")

while (1):
  try:
    time.sleep(TIMEOUT)
    main_loop()
  except Exception as err:
    err_logger.error("Main loop encountered error!", exc_info=err)
