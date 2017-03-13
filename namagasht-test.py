import requests, telebot
#import test
import API.request
import API.CoreData
import API.CoreDataHandler
from telebot import types

myReqHandler = API.request.RequestHandler()
myDataHandler = API.CoreDataHandler.DataHandler()

bot = telebot.TeleBot("355663026:AAHqFh4FznycH8V5fE9zP3bVdM_Aeiqf9pA")

def getPackages(message, token):
    #token = myDataHandler.getToken(message.from_user.id)
    messagesToSend = myReqHandler.getFinalPackages(token)
    for messageToSend in messagesToSend:
        bot.send_message(message.chat.id, messageToSend)

def getTreaties(message, token):
    #token = myDataHandler.getToken(message.from_user.id)
    messagesToSend = myReqHandler.getFinalTreaties(token)
    for messageToSend in messagesToSend:
        bot.send_message(message.chat.id, messageToSend)

def getPickups(message, token):
    #token = myDataHandler.getToken(message.from_user.id)
    messagesToSend = myReqHandler.getFinalPickups(token)
    #print(str(len(messagesToSend)))
    for messageToSend in messagesToSend:
        bot.send_message(message.chat.id, messageToSend)

def contactUs(message, token):
    messageToSend = myReqHandler.aboutUs(token)
    bot.send_message(message.chat.id, messageToSend)

@bot.message_handler(commands=['start'])
def start(message):
    if(myDataHandler.getToken(message.from_user.id) != -1):
        #bot.send_message(message.from_user.id, "خوش آمدید")
        #markup = types.ReplyKeyboardMarkup(row_width=2, selective=False)
        serviceMarkup = types.ReplyKeyboardMarkup(row_width=2, selective=False)
        treatyBtn = types.KeyboardButton(API.CoreData.treatyText)
        packageBtn = types.KeyboardButton(API.CoreData.packageText)
        pickupBtn = types.KeyboardButton(API.CoreData.pickupText)
        contactBtn = types.KeyboardButton(API.CoreData.contactText)
        logoutBtn = types.KeyboardButton(API.CoreData.logoutText)
        serviceMarkup.row(treatyBtn, packageBtn)
        serviceMarkup.row(pickupBtn)
        serviceMarkup.row(logoutBtn, contactBtn)
        serviceMarkup.resize_keyboard = True
        messageText = myReqHandler.messageCreator.greetingMeessage()
        bot.send_message(message.chat.id, messageText, reply_markup=serviceMarkup)

    else:
        myDataHandler.setStateforUser(message.from_user.id, 0)
        #API.CoreDataHandler2.setStateforUser(message.from_user.id, 0)
        messageText = myReqHandler.messageCreator.signIn(0)
        removeMarkup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, messageText, reply_markup=removeMarkup)
        #bot.send_message(message.chat.id, messageText)

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
            bot.send_message(message.chat.id, "لطفا صبر کنید" + u'\U000023F3')
            userPass = myDataHandler.getUserUsernamePass(message.from_user.id)
            logState = myReqHandler.signIn(userPass[0], userPass[1])
            if(not logState):
                #messageText = "نام کاربری یا رمز اشتباه است دوباره تلاش کنید" + '\n\n'
                #bot.send_message(message.chat.id, messageText)
                #messageText = myReqHandler.messageCreator.signIn(0)
                messageText = myReqHandler.messageCreator.badLogin()
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
                getTreaties(message, myUserToken)
                myDataHandler.setTreaty(message.from_user.id, 0)
                #treatyRemoveMarkup = types.ReplyKeyboardRemove()

                #bot.send_message(message.from_user.id, "لطفا شماره ی قرارداد خود را وارد نمایید", reply_markup=treatyRemoveMarkup)
                backMarkup = types.ReplyKeyboardMarkup()
                returnBtn = types.KeyboardButton(API.CoreData.returnText)
                backMarkup.row(returnBtn)
                backMarkup.resize_keyboard = True
                toSendText = u'\U0001F58C' + "لطفا شناسه ی قرارداد خود را وارد نمایید"
                bot.send_message(message.chat.id, toSendText, reply_markup= backMarkup)

            elif(message.text == API.CoreData.packageText):
                getPackages(message, myUserToken)

            elif(message.text == API.CoreData.pickupText):
                getPickups(message, myUserToken)

            elif(message.text == API.CoreData.contactText):
                contactUs(message, myUserToken)

            elif(message.text == API.CoreData.logoutText):
                logout(message)

        else:

            if(message.text == API.CoreData.treatyText or
               message.text == API.CoreData.packageText or
               message.text == API.CoreData.pickupText or
               message.text == API.CoreData.contactText):
                myDataHandler.removeFromTreaty(message.from_user.id)
                handleCommand(message)

            if(myUserTreaty == 0):
                if(message.text == API.CoreData.returnText):
                    myDataHandler.removeFromTreaty(message.from_user.id)
                    serviceMarkup = types.ReplyKeyboardMarkup(row_width=2, selective=False)
                    treatyBtn = types.KeyboardButton(API.CoreData.treatyText)
                    packageBtn = types.KeyboardButton(API.CoreData.packageText)
                    pickupBtn = types.KeyboardButton(API.CoreData.pickupText)
                    contactBtn = types.KeyboardButton(API.CoreData.contactText)
                    logoutBtn = types.KeyboardButton(API.CoreData.logoutText)
                    serviceMarkup.row(treatyBtn, packageBtn)
                    serviceMarkup.row(pickupBtn)
                    serviceMarkup.row(logoutBtn, contactBtn)
                    serviceMarkup.resize_keyboard = True
                    toSendText = u'\U0001F58C' + "لطفا سرویس مورد نظر خود را انتخاب نمایید "
                    bot.send_message(message.chat.id, toSendText, reply_markup=serviceMarkup)

                else:
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
                    toSendText = u'\U0001F58C' + "لطفا سرویس قرارداد خود را انتخاب نمایید "
                    bot.send_message(message.from_user.id, toSendText,reply_markup= treatyMarkup)

            elif(myUserTreaty == 1):

                if(message.text == API.CoreData.returnText):
                    myDataHandler.removeFromTreaty(message.from_user.id)
                    serviceMarkup = types.ReplyKeyboardMarkup(row_width=2, selective=False)
                    treatyBtn = types.KeyboardButton(API.CoreData.treatyText)
                    packageBtn = types.KeyboardButton(API.CoreData.packageText)
                    pickupBtn = types.KeyboardButton(API.CoreData.pickupText)
                    contactBtn = types.KeyboardButton(API.CoreData.contactText)
                    logoutBtn = types.KeyboardButton(API.CoreData.logoutText)
                    serviceMarkup.row(treatyBtn, packageBtn)
                    serviceMarkup.row(pickupBtn)
                    serviceMarkup.row(logoutBtn, contactBtn)
                    serviceMarkup.resize_keyboard = True
                    toSendText = u'\U0001F58C' + "لطفا سرویس مورد نظر خود را انتخاب نمایید "
                    bot.send_message(message.chat.id, toSendText, reply_markup=serviceMarkup)
                    #bot.send_message(message.chat.id, "سرویس خود را انتخاب کنید", reply_markup=serviceMarkup)

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