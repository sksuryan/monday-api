import os
from results.amizone import getAttendance, getToday
from flask import Flask, request, jsonify
import telegram

app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')

bot = telegram.Bot(token=TOKEN)

defaultMessage = ''' 
Hi, I'm monday
Here are my commands:
/attendance - to list attendance of all subjects
/today - to show today's classes and their attendance
'''

@app.route('/')
def default():
    return 'monday api built using flask by @sksuryan'

@app.route('/{}'.format(TOKEN),methods=['post'])
def respond():
    update = telegram.Update.de_json(request.get_json(),bot)
    chatID = update.message.chat.id

    receivedMsg = update.message.text.encode('utf-8').decode()
    response = ''
    bot.sendChatAction(chatID, telegram.ChatAction.TYPING)
    if receivedMsg == '/start':
        response = defaultMessage
    elif receivedMsg == '/attendance':
        response = getAttendance()
    elif receivedMsg == '/today':
        response = getToday()
    else:
        response = defaultMessage
    bot.sendMessage(chat_id=chatID, text=response)

    return 'ok'

if __name__ == '__main__':
    app.run()