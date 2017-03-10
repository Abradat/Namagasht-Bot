import requests, telebot
#import test
import API.request
import API.CoreData
import API.CoreDataHandler
import API.CoreDataHandler2
from telebot import types

myReqHandler = API.request.RequestHandler()
myDataHandler = API.CoreDataHandler.DataHandler()

bot = telebot.TeleBot("355663026:AAHqFh4FznycH8V5fE9zP3bVdM_Aeiqf9pA")

@bot.message_handler(commands=['packages'])
def getPackages(message):
    token = myDataHandler.getToken(message.from_user.id)
    messagesToSend = myReqHandler.getFinalPackages(token)
    for messageToSend in messagesToSend:
        bot.send_message(message.chat.id, messageToSend)

@bot.message_handler(commands=['treaties'])
def getTreaties(message):
    token = myDataHandler.getToken(message.from_user.id)
    messagesToSend = myReqHandler.getFinalTreaties(token)
    for messageToSend in messagesToSend:
        bot.send_message(message.chat.id, messageToSend)

@bot.message_handler(commands=['start'])
def start(message):
    if(myDataHandler.getToken(message.from_user.id) != -1):
        bot.send_message(message.from_user.id, "خوش آمدید")
        markup = types.ReplyKeyboardMarkup(row_width=2, selective=False)
        itembtn1 = types.KeyboardButton(API.CoreData.treatyText)
        itembtn2 = types.KeyboardButton(API.CoreData.packageText)
        markup.add(itembtn1, itembtn2)
        markup.resize_keyboard = True
        bot.send_message(message.chat.id, "سرویس خود را انتخاب کنید", reply_markup=markup)
    else:
        myDataHandler.setStateforUser(message.from_user.id, 0)
        #API.CoreDataHandler2.setStateforUser(message.from_user.id, 0)
        messageText = myReqHandler.messageCreator.signIn(0)
        bot.send_message(message.chat.id, messageText)

@bot.message_handler(commands=['logout'])
def logout(message):
    print("hello")
    myDataHandler.removeFromUsers(message.from_user.id)
    start(message)

@bot.message_handler(content_types= ['text'])
def handleCommand(message):
    if(myDataHandler.getUserState(message.from_user.id) != -1 and myDataHandler.getToken(message.from_user.id) == -1):
        userState = myDataHandler.getUserState(message.from_user.id)

        if (message.text == API.CoreData.treatyText):
            bot.reply_to(message, "ابتدا باید وارد شوید")
            if(userState == 0):
                bot.send_message(message.chat.id, "لطفا نام کاربری خود را وارد کنید")
            elif(userState == 1):
                bot.send_message(message.chat.id, "لطفا رمز خود را وارد نمایید")

        elif (message.text == API.CoreData.packageText):
            bot.reply_to(message, "ابتدا باید وارد شوید")
            if (userState == 0):
                bot.send_message(message.chat.id, "لطفا نام کاربری خود را وارد کنید")
            elif (userState == 1):
                bot.send_message(message.chat.id, "لطفا رمز خود را وارد نمایید")

        elif(userState == 0):
            myDataHandler.setStateforUser(message.from_user.id, 1, message.text)
            messageText = myReqHandler.messageCreator.signIn(1)
            bot.send_message(message.chat.id, messageText)

        elif(userState == 1):
            myDataHandler.setStateforUser(message.from_user.id, 2, "", message.text)
            bot.send_message(message.chat.id, "لطفا صبر کنید")
            userPass = myDataHandler.getUserUsernamePass(message.from_user.id)
            #print (userPass)
            logState = myReqHandler.signIn(userPass[0], userPass[1])
            if(not logState):
                messageText = "نام کاربری یا رمز اشتباه است دوباره تلاش کنید" + '\n\n'
                bot.send_message(message.chat.id, messageText)
                messageText = myReqHandler.messageCreator.signIn(0)
                myDataHandler.setZState(message.from_user.id)
                bot.send_message(message.chat.id, messageText)
            else:
                bot.send_message(message.chat.id,"خوش آمدید")
                myDataHandler.insertUser(str(message.from_user.id), logState)
                myDataHandler.removeFromUserSates(message.from_user.id)

    elif(myDataHandler.getUserState(message.from_user.id) == -1 and myDataHandler.getToken(message.from_user.id) == -1):
        messageText = "ابتدا باید وارد شوید. نام کاربری را وارد کنید"
        myDataHandler.setStateforUser(message.from_user.id, 0)
        bot.send_message(message.chat.id, messageText)

    elif(myDataHandler.getToken(message.from_user.id) != -1):
        if(message.text == API.CoreData.treatyText):
            getTreaties(message)
        elif(message.text == API.CoreData.packageText):
            getPackages(message)


bot.polling()