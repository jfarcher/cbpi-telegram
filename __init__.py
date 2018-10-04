from modules import app, cbpi
from thread import start_new_thread
import logging
import time
import requests

Telegram_token = None
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
    telegramChatID()
    telegramToken()
#    if telegram_token is None or not telegram_token:
#        cbpi.notify("Telegram Error","Check Telegram API Token is set", type="danger", timeout=None)
#    elif telegram_chatid is None or not telegram_chatid:
#        cbpi.notify("Telegram Error", "Check Telegram chat ID is set", type="danger", timeout=None)
#    else:
    telegram = "OK"

@cbpi.event("MESSAGE", async=True)
def messageEvent(message):
    requests.post("https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}".format(telegram_token,message,telegram_chatid))
    cbpi.app.logger.info("Sending Notification")
