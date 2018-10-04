from modules import app, cbpi
from thread import start_new_thread
import logging
import time
import telegram

Telegram_token = None
telegram_user = None
telegram = None
def telegramToken():
    global Telegram_token
    telegram_token = cbpi.get_config_parameter("telegram_token",None)
    if Telegram_token is None:
        print "INIT Telegram Token"
        try:
            cbpi.add_config_parameter("telegram_token", "", "text", "Telegram API Token")
        except:
            cbpi.notify("Telegram Error", "Unable to update database. Update CraftBeerPi and Reboot.", type="danger", timeout=None)

def telegramUser():
    global telegram_user
    telegram_user = cbpi.get_config_parameter("telegram_user", None)
    if telegram_user is None:
        print "INIT Telegram User Key"
        try:
            cbpi.add_config_parameter("telegram_user", "", "text", "Telegram User Key")
        except:
            cbpi.notify("Telegram Error", "Unable to update database. Update CraftBeerPi and reboot.", type="danger", timeout=None)

@cbpi.initalizer(order=9000)
def init(cbpi):
    global telegram
    cbpi.app.logger.info("INITIALIZE Telegram PLUGIN")
    telegramUser()
    telegramToken()
    if telegram_token is None or not telegram_token:
        cbpi.notify("Telegram Error", "Check Telegram API Token is set", type="danger", timeout=None)
    elif telegram_user is None or not telegram_user:
        cbpi.notify("Telegram Error", "Check Telegram User Key is set", type="danger", timeout=None)
    else:
        telegram = "OK"

@cbpi.event("MESSAGE", async=True)
def messageEvent(message):
  bot = telegram.Bot(token=telegram_token)
  bot.sendMessage(chat_id=telegram_user, text=message)
