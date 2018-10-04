from modules import app, cbpi
from thread import start_new_thread
import logging
import time
import requests

telegram_token = None
telegram_user = None
telegram = None

def telegramToken():
    global Telegram_token
    telegram_token = cbpi.get_config_parameter("telegram_token", None)
    if telegram_token is None:
        print "INIT Telegram Token"
        try:
            cbpi.add_config_parameter("telegram_token", "", "text", "Telegram API Token")
        except:
            cbpi.notify("Telegram Error", "Unable to update database. Update CraftBeerPi and Reboot.", type="danger", timeout=None)

def telegramChatID():
    global telegram_chatid
    telegram_chatid = cbpi.get_config_parameter("telegram_chatid", None)
    cbpi.app.logger.info(telegram_chatid)
    if telegram_chatid is None:
        print "INIT Telegram Chat ID"
        try:
            cbpi.add_config_parameter("telegram_chatid", "", "text", "Telegram Chat ID")
        except:
            cbpi.notify("Telegram Error", "Unable to update database. Update CraftBeerPi and reboot.", type="danger", timeout=None)

@cbpi.initalizer(order=9000)
def init(cbpi):
    global telegram
    cbpi.app.logger.info("INITIALIZE Telegram PLUGIN")
    telegramToken()
    telegramChatID()
    if telegram_token is None or not telegram_token:
            cbpi.notify("Telegram Error", "Check Telegram API Token is set", type="danger", timeout=None)
    elif telegram_chatid is None or not telegram_chatid:
            cbpi.notify("Telegram Error", "Check Telegram Chat ID is set", type="danger", timeout=None)
    else:
            telegram = "OK"
@cbpi.event("MESSAGE", async=True)
def messageEvent(message):
    telegramData = {}
    telegramData["chat_id"] = telegram_chatid
    telegramData["message"] = message["message"]
    cbpi.app.logger.info("Sending Notification" + telegram_token + telegram_chatid + message)
    requests.post("https://api.telegram.org/bot{}/sendMessage/", json=telegramData)
