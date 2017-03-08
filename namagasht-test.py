import requests, telebot
#import test
import API.request
import API.CoreData
from telebot import types

myReqHandler = API.request.RequestHandler()

bot = telebot.TeleBot("321627717:AAHftufVKQWrZzVG_IlcucVPt0AkJGarsH4")

@bot.message_handler(commands=['packages'])
def getPackages(message):
    messagesToSend = myReqHandler.getFinalPackages(myReqHandler.getToken(API.CoreData.sampleData))
    for messageToSend in messagesToSend:
        bot.send_message(message.chat.id, messageToSend)

@bot.message_handler(commands=['treaties', '/قراردادها'])
def getTreaties(message):
    messagesToSend = myReqHandler.getFinalTreaties(myReqHandler.getToken(API.CoreData.sampleData))
    for messageToSend in messagesToSend:
        bot.send_message(message.chat.id, messageToSend)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width = 2, selective= False)
    itembtn1 = types.KeyboardButton(API.CoreData.treatyText)
    itembtn2 = types.KeyboardButton(API.CoreData.packageText)
    markup.add(itembtn1, itembtn2)
    markup.resize_keyboard = True
    bot.send_message(message.chat.id, "سرویس خود را انتخاب کنید", reply_markup= markup)

@bot.message_handler(content_types= ['text'])
def handleCommand(message):
    if(message.text == API.CoreData.treatyText):
        getTreaties(message)
    elif(message.text == API.CoreData.packageText):
        getPackages(message)

bot.polling()