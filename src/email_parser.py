import imaplib
import email
import os
import random
import logging
import bot_logger
import time

class EmailInstance:
  def __init__(self, id, subject, body, from_, filenames):
    self.id = id
    self.subject = subject
    self.body = body
    self.from_ = from_
    self.filenames = filenames

class EmailHandler:
  def __init__(self, email: str, passwd: str, logger) -> None:
    self.email = email
    self.passwd = passwd
    self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
    self.mail.login(email, passwd)
    self.mail.list()
    self.mail.select("inbox")
    self.logger: logging.Logger = logger
    self.err_logger: logging.Logger = bot_logger.get_dual_logger()
  
  def remove_all(self):
    self.logger.info("Mailbox cleanup")
    for i in self.messages[0].decode("utf-8").split(' '):
      self.mail.store(i, "+FLAGS", "\\Deleted")
    self.mail.expunge()

  def parse_header(self, msg):
    subject, encoding = email.header.decode_header(msg["Subject"])[0]
    if (isinstance(subject, bytes)):
      subject = subject.decode(encoding)
    
    from_, encoding = email.header.decode_header(msg.get("From"))[0]
    if (isinstance(from_, bytes)):
      from_ = from_.decode(encoding)
    
    return subject, from_

  def clean(self, text):
    return "".join(c if c.isalnum() else "_" for c in text)

  def decode_filename(self, part):
    tmp_filename = email.header.decode_header(part.get_filename())
    if (tmp_filename[0][1] is None):
      return tmp_filename[0][0]
    return ''.join(
      str(part, encoding if isinstance(part, bytes) else None) 
      for part, encoding in tmp_filename)
  
  def get_mail_count(self) -> int:
    status, messages = self.mail.search(None, "UNSEEN")
    return len(messages[0].decode("utf-8").split(' '))
  
  def mark_read(self, msg_id):
    self.mail.store(msg_id, "+FLAGS", "\\Seen")

  def remove_seen(self):
    status, messages = self.mail.search(None, "SEEN")
    if (status != "OK"):
      return
    for i in messages[0].decode("utf-8").split(' '):
      while True:
        try:
          self.mail.store(i, "+FLAGS", "\\Deleted")
        except imaplib.IMAP4.error as err:
          raise err
          self.logger.info("imaplib.IMAP4.error! Retrying...")
          time.sleep(2)
          continue
        break
      self.logger.info("Removed message")
    self.mail.expunge()

  def download_attachment(self, part, subject, prev_dir_name):
    filename = self.decode_filename(part)
    filepath = ""
    
    if (filename):
      folder_name = self.clean(subject)
      if (len(folder_name) <= 1):
        folder_name = "data"
      if (not os.path.isdir(folder_name)):
        os.mkdir(folder_name)
      elif (prev_dir_name == ""):
        folder_name += str(random.randint(0, 99999999999999999999999))
        os.mkdir(folder_name)
      if (prev_dir_name == ""):
        filepath = os.path.join(folder_name, filename)
      else:
        filepath = os.path.join(prev_dir_name, filename)
      self.logger.info(f"Downloading attachment to {filepath}")
      open(filepath, "wb+").write(part.get_payload(decode=True))
    
    return filepath


  def check(self):
    self.mail.check()
    status, messages = self.mail.search(None, "UNSEEN")
    if (status != "OK"):
      self.err_logger.error(f"imaplib returned code \"{status}\"")
      return []
    elif (messages[0] is None or len(messages[0]) == 0):
      return []

    result: list[EmailInstance] = []

    for i in messages[0].decode("utf-8").split(' '):
      res, msg = self.mail.fetch(str(i), '(RFC822)')
      for response in msg:
        email_inst = EmailInstance(i, None, None, None, [])
        if (not isinstance(response, tuple)):
          continue

        msg = email.message_from_bytes(response[1])
        subject, from_ = self.parse_header(msg)
        email_inst.subject = subject
        email_inst.from_ = from_
        if (msg.is_multipart()):
          self.logger.info("Multipart message detected")
          for part in msg.walk():
            content_type = part.get_content_type()
            self.logger.info(f"Part content type: {content_type}")
            content_disposition = str(part.get("Content-Disposition"))

            try:
              data = part.get_payload(decode=True).decode()
            except:
              self.logger.info("Failed to get payload: continuing")
              
            if (content_type == "text/plain" and "attachment" not in content_disposition):
              email_inst.body = data
            elif ("attachment" in content_disposition):
              prev_dir_name = ""
              if (len(email_inst.filenames) > 0):
                prev_dir_name = email_inst.filenames[-1].split('/')[0]
              email_inst.filenames.append(self.download_attachment(part, subject, prev_dir_name))
        else:
          content_type = msg.get_content_type()
          email_inst.body = msg.get_payload(decode=True).decode()

        result.append(email_inst)
    
    self.messages = messages
    return result
