#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MessageCreator():
    def __init__(self):
        pass

    def createPackageMessage(self, packages):
        messages = []
        for message in packages:
            #print (message)
            messageText = ""
            messageText += u'\U00002B50' + u'\U0001F31F' +"پکیج شماره ی " + str(message["id"]) +\
                            u'\U00002B50' + u'\U0001F31F' + '\n\n\n'
            messageText +=  message["name"] + u'\U0001F6EB' + u'\U0001F6EB' + '\n\n\n\n\n'
            messageText += "مدت اقامت :‌ " + u'\U0001F3DD' + '\n'
            messageText += '\t' + u'\U0001F31F' + str(message["stay_day_count"]) + "روز و " + str(message["stay_night_count"]) + \
                           "شب." + u'\U0001F31F' +  '\n\n\n'
            if('price' in message):
                messageText += u'\U0001F4B0' +"هزینه :‌" + (str(message["price"])[0:8]) + "ریال " + u'\U0001F4B8' +'\n'
            messages.append(messageText)
        return messages

    def createTreatyMessage(self, treaties):
        messages = []
        for message in treaties:
            messageText = ""
            messageText += u'\U0001F4CD' + " شناسه ی قرارداد :‌ " + str(message["treaty_number"]) + "\n\n\n"
            messageText += u'\U0001F4CD' + "مشخصات قرارداد : " + '\n\n'
            messageText += u'\U0001F4CE' + " نوع قرارداد :‌ " + str(message["treaty_type"]) + '\n'
            messageText += u'\U0001F4CE' + " نوع سرویس :‌" + str(message["service_type"]) + '\n'
            messageText += u'\U0001F4CE' + " مبلغ کل قرارداد :‌" + (str(message["total_amount"])[0:8]) + '\n'
            messageText += u'\U0001F4CE' + " مبلغ کل محاسبه شده :‌ " + (str(message["total_cal_amount"])[0:8]) + '\n'
            messageText += u'\U0001F4CE' + " شماره ملی :‌ " + str(message["national_identity_number"]) + '\n'
            messageText += u'\U0001F4CE' + " نام  نماینده : " + message["agent_name"] + '\n'
            messageText += u'\U0001F4CE' + " نام حسابدار : " + message["counter"] + "\n\n\n"
            messageText += (u'\U0001F33F') * 3
            messages.append(messageText)

        #messageText = ""
        #contact = message["contact_values"].split(',')
        #messageText += u'\U0001F4DE' + "شماره تماس ثابت : " + contact[0] + '\n\n'
        #messageText += u'\U0001F4F1' + " شماره تماس همراه : " + contact[1] + '\n\n'
        #messageText += u'\U0001F4E7' + " آدرس ایمیل :‌ " + contact[2] + '\n\n'
        #messageText += u'\U0001F4EE' +  " نشانی :‌ " + contact[3] + '\n\n'
        #messageText += (u'\U0001F33F') * 3
        #messages.append(messageText)

        return messages

    def createPickupMessage(self, pickups):
        messages = []
        for message in pickups:
            messageText = ""
            messageText += u'\U0001F3DB' + 'شناسه ی پیکاپ : ' + str(message["title"]) + '\n\n\n'
            messageText += u'\U0001F465' + 'نام و نام خانوادگی :‌ ' + str(message["native_full_name"]) + '\n\n'
            messageText += u'\U0001F310' + 'شماره پاسپورت : ' + str(message["passport_number"]) + '\n\n'
            messageText += u'\U0001F58C' + 'وضعیت پیکاپ : ' + str(message["state_name"]) + '\n\n\n'
            messageText += (u'\U0001F33F') * 3
            messages.append(messageText)
        return messages

    def signIn(self, state):
        messageText = ""
        if(state == 0):
            messageText = u'\U0001F338' "به بات نماگشت خوش آمدید" + u'\U0001F338' + '\n\n' + \
                          u'\U0001F464' +"لطفا نام کاربری خود را وارد نمایید " +  \
                          '\n\n' + (u'\U0001F33F') * 3
        elif(state == 1):
            messageText = u'\U0001F512' + " لطفا کلمه ی عبور خود را وارد نمایید :‌"

        return messageText

    def aboutUsMessage(self, message):
        messageText = ""
        contact = message["contact_values"].split(',')
        messageText += u'\U0001F4DE' + "شماره تماس ثابت : " + contact[0] + '\n\n'
        messageText += u'\U0001F4F1' + " شماره تماس همراه : " + contact[1] + '\n\n'
        messageText += u'\U0001F4E7' + " آدرس ایمیل :‌ " + contact[2] + '\n\n'
        messageText += u'\U0001F4EE' +  " نشانی :‌ " + contact[3] + '\n\n'
        messageText += (u'\U0001F33F') * 3

        return messageText

    def greetingMeessage(self):
        messageText = u'\U0001F338' + " خوش آمدید " + u'\U0001F338' + '\n\n' + \
                      u'\U0001F58C' + "لطفا سرویس مورد نظر خود را انتخاب نمایید "
        return messageText

    def badLogin(self):
        messageText = 'نام کاربری یا کلمه ی عبور اشتباه است ' + u'\U0001F6AB' + '\n\n' + \
                      u'\U0001F464' + "لطفا نام کاربری خود را وارد نمایید " + '\n\n' + (u'\U0001F33F') * 3
        return messageText






