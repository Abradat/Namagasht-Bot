import requests, telebot
import json
#import test
import API.request
import API.CoreData
#import API.CoreDataHandler
import API.CoreDataHandler2
from telebot import types

bot = telebot.TeleBot("355663026:AAHqFh4FznycH8V5fE9zP3bVdM_Aeiqf9pA")


@bot.message_handler(commands=['start'])
def start(message):
    pdfText = requests.get('http://84.241.44.153:8585/api/v1/treaties/' + '325' + '/hotel', headers={
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImI1OTEwM2MxMGNmN2M4YmNkMDM0MDE3MTNiMTg1OGE4YzUwMmJlZTAwZDdiMzNjYzFhODE0NzY2NWVjMzQzNjUwNjBkMzYyMTM0MmQ1NmZiIn0.eyJhdWQiOiIxIiwianRpIjoiYjU5MTAzYzEwY2Y3YzhiY2QwMzQwMTcxM2IxODU4YThjNTAyYmVlMDBkN2IzM2NjMWE4MTQ3NjY1ZWMzNDM2NTA2MGQzNjIxMzQyZDU2ZmIiLCJpYXQiOjE0ODg5NjE2NjIsIm5iZiI6MTQ4ODk2MTY2MiwiZXhwIjo0NjQ0NjM1MjYxLCJzdWIiOiI4MiIsInNjb3BlcyI6W119.CTV9PTLLnb6_n6qdYpyVJ7wBjOwrx4MkIgoBpy732vddqxBYE24VJEY5vxKWRjjxNkBC0KQ5PcGKi6eyWiNg6neJ37k09SAde9lmlS1dCQQ9tSxfqHgXh9E0bfW1wri-ogAlQp-2DgQ7EVWg8p_1235pEekMDrG1LryS7qgqsdJ8dU6lDHPx_X9TtIYrpx8uUzJsoMo7_0nIxMMUD4v2e96IouF--mPExFo3lR5qqs8UaidM3tnj1YTNlC_d2RmHdQjNcm8wzdhuHNjJd-bgyGb2gT7uVks6DcNCNc9KklhPOO3D-KALuEbpZPuxUc0MM4nOwj3HCOwKyUxwCyMfiNLb-lQfFB4VV-3I8T217Nqiicm8WWvKhpni660xRWkjJmUxaTVziwJaQ7-MlqkOBWz_bw_YWSLkF2weS2f-wcynASkaSvQcc7b1ksmoQVMrxvDM7iSOZEaaeMDNO9_6PD6ks6ur3rLSq0QgenOhLfb7vWIIxEStn0mlVB1jXS75f9MCe1LP9WgYS0qkcCRhB9JzfpnfNK79DFMxIkMg28pq0cUg70dTXJ6hHgeCrcopSaphBSHZhd6COhRwr9wL2hf3kasYtglteUaUKS05uaIxxJcJGz2R-qo2QnH5IR6wPgEY6FGt6PWTAau85ttqtVqRz5lh6M9c0ADvlfcQN8o',
        'Accept': 'application/json'
    })
    #print(pdfText.json())
    an = {}
    #b = json.load(pdfText)
    #print (b)
    #an['file'] = ({'length' : pdfText.json()['length'], 'type' : pdfText.json()['type'], 'content' : pdfText.json()['content']})

    #bot.send_document(message.chat.id, an)
    an = json.loads(pdfText.text)['content']
    #print(an)
    #print(pdfText.text)
    bot.send_document(message.chat.id, data= open('API/Files/kiri.pdf',  'rb'))

bot.polling()