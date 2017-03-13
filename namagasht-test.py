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

@bot.message_handler(commands=['treaties'])
def getPickups(message):
    token = myDataHandler.getToken(message.from_user.id)

@bot.message_handler(commands=['start'])
def start(message):
    if(myDataHandler.getToken(message.from_user.id) != -1):
        bot.send_message(message.from_user.id, "خوش آمدید")
        #markup = types.ReplyKeyboardMarkup(row_width=2, selective=False)
        serviceMarkup = types.ReplyKeyboardMarkup(row_width=2, selective=False)
        treatyBtn = types.KeyboardButton(API.CoreData.treatyText)
        packageBtn = types.KeyboardButton(API.CoreData.packageText)
        pickupBtn = types.KeyboardButton(API.CoreData.pickupText)
        serviceMarkup.row(treatyBtn, packageBtn)
        serviceMarkup.row(pickupBtn)
        serviceMarkup.resize_keyboard = True
        bot.send_message(message.chat.id, "سرویس خود را انتخاب کنید", reply_markup=serviceMarkup)

    else:
        myDataHandler.setStateforUser(message.from_user.id, 0)
        #API.CoreDataHandler2.setStateforUser(message.from_user.id, 0)
        messageText = myReqHandler.messageCreator.signIn(0)
        bot.send_message(message.chat.id, messageText)

@bot.message_handler(commands=['logout'])
def logout(message):
    myDataHandler.removeFromUsers(message.from_user.id)
    start(message)

@bot.message_handler(content_types= ['text'])
def handleCommand(message):

    myUserState = myDataHandler.getUserState(message.from_user.id)
    myUserToken = myDataHandler.getToken(message.from_user.id)
    myUserTreaty = myDataHandler.getTreatyState(message.from_user.id)

    if(myUserState != -1 and myUserToken == -1):
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
                #bot.send_message(message.chat.id,"خوش آمدید")
                myDataHandler.insertUser(str(message.from_user.id), logState)
                myDataHandler.removeFromUserSates(message.from_user.id)
                start(message)

    elif(myUserState == -1 and myUserToken == -1):
        messageText = "ابتدا باید وارد شوید. نام کاربری را وارد کنید"
        myDataHandler.setStateforUser(message.from_user.id, 0)
        bot.send_message(message.chat.id, messageText)

    elif(myUserToken != -1):

        if(myUserTreaty == -1):

            if(message.text == API.CoreData.treatyText):
                getTreaties(message)
                myDataHandler.setTreaty(message.from_user.id, 0)
                treatyRemoveMarkup = types.ReplyKeyboardRemove()
                bot.send_message(message.from_user.id, "لطفا شماره ی قرارداد خود را وارد نمایید", reply_markup=treatyRemoveMarkup)

            elif(message.text == API.CoreData.packageText):
                getPackages(message)

            elif(message.text == API.CoreData.pickupText):
                getPickups()

        else:

            if(message.text == API.CoreData.treatyText or
               message.text == API.CoreData.packageText or
               message.text == API.CoreData.pickupText):
                myDataHandler.removeFromTreaty(message.from_user.id)
                handleCommand(message)

            if(myUserTreaty == 0):
                myDataHandler.setTreaty(message.from_user.id, 1, message.text)
                treatyMarkup = types.ReplyKeyboardMarkup()
                hotelBtn = types.KeyboardButton(API.CoreData.hotelText)
                ticketBtn = types.KeyboardButton(API.CoreData.ticketText)
                recieptBtn = types.KeyboardButton(API.CoreData.receiptText)
                returnBtn = types.KeyboardButton(API.CoreData.returnText)
                treatyMarkup.row(hotelBtn, ticketBtn)
                treatyMarkup.row(recieptBtn)
                treatyMarkup.row(returnBtn)
                treatyMarkup.resize_keyboard = True
                bot.send_message(message.from_user.id, "لطفا سرویس قرارداد را انتخاب نمایید",reply_markup= treatyMarkup)

            elif(myUserTreaty == 1):

                if(message.text == API.CoreData.returnText):
                    myDataHandler.removeFromTreaty(message.from_user.id)
                    serviceMarkup = types.ReplyKeyboardMarkup(row_width=2, selective=False)
                    treatyBtn = types.KeyboardButton(API.CoreData.treatyText)
                    packageBtn = types.KeyboardButton(API.CoreData.packageText)
                    pickupBtn = types.KeyboardButton(API.CoreData.pickupText)
                    serviceMarkup.row(treatyBtn, packageBtn)
                    serviceMarkup.row(pickupBtn)
                    serviceMarkup.resize_keyboard = True
                    bot.send_message(message.chat.id, "سرویس خود را انتخاب کنید", reply_markup=serviceMarkup)

                elif(message.text == API.CoreData.hotelText):
                    treatyNum = myDataHandler.getTreatyMessage(message.from_user.id)
                    myDataHandler.generateHotelPdf(myReqHandler.getHotel(myUserToken, treatyNum), treatyNum)
                    bot.send_document(message.chat.id, data= open(
                        'API/Files/' + str(treatyNum) + '-hotel.pdf', 'rb'
                    ))
                    myDataHandler.removeHotelPdf(treatyNum)

                elif(message.text == API.CoreData.ticketText):
                    treatyNum = myDataHandler.getTreatyMessage(message.from_user.id)
                    myDataHandler.generateTicketPdf(myReqHandler.getTicket(myUserToken, treatyNum), treatyNum)
                    bot.send_document(message.chat.id, data= open(
                        'API/Files/' + str(treatyNum) + '-ticket.pdf', 'rb'
                    ))
                    myDataHandler.removeTicketPdf(treatyNum)

                elif(message.text == API.CoreData.receiptText):
                    treatyNum = myDataHandler.getTreatyMessage(message.from_user.id)
                    myDataHandler.generateReceiptPdf(myReqHandler.getReceipt(myUserToken, treatyNum), treatyNum)
                    bot.send_document(message.chat.id, data=open(
                        'API/Files/' + str(treatyNum) + '-receipt.pdf', 'rb'
                    ))
                    myDataHandler.removeReceiptPdf(treatyNum)


bot.polling()