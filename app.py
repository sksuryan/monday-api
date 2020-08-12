from results.amizone import getAttendance, getDay, getAttendanceForDay
from flask import Flask, request, jsonify
import telegram
import datetime
import os


app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')
AUTORES=os.environ.get('AUTORES')

bot = telegram.Bot(token=TOKEN)

defaultMessage = ''' 
Hi, I'm monday
Here are my commands:
/attendance - to list attendance of all subjects
/today - to show today's classes and their attendance
/attendanceForToday - show attendance for today's classes
'''

@app.route('/')
def default():
    return 'monday api built using flask by @sksuryan'

@app.route('/{}'.format(TOKEN),methods=['post'])
def respond():
    update = telegram.Update.de_json(request.get_json(),bot)
    chatID = update.message.chat.id
    reqdChatID = int(os.environ.get('CHATID'))

    receivedMsg = update.message.text.encode('utf-8').decode()
    response = ''
    bot.sendChatAction(chatID, telegram.ChatAction.TYPING)

    date = datetime.date.today()

    if reqdChatID != chatID:
        response = f'Sorry, monday is for personal use 😅'
    else:
        if receivedMsg == '/start':
            response = defaultMessage
        elif receivedMsg == '/attendance':
            response = getAttendance()
        elif receivedMsg == '/today':
            date = date.strftime('%Y-%m-%d')
            response = getDay(date)
        elif receivedMsg == '/attendanceForToday':
            date = date.strftime('%Y-%m-%d')
            response = getAttendanceForDay(date)
        elif receivedMsg == '/yesterday':
            date = date - datetime.timedelta(days=1)
            date = date.strftime('%Y-%m-%d')
            response = getAttendanceForDay(date)
        elif receivedMsg == '/tomorrow':
            date = date + datetime.timedelta(days=1)
            date = date.strftime('%Y-%m-%d')
            response = getDay(date)
        else:
            response = defaultMessage

    bot.sendMessage(chat_id=chatID, text=response)

    return 'ok'

@app.route('/{}'.format(AUTORES))
def autores():
    method = request.args.get('method')
    chatID = os.environ.get('CHATID')
    response = ''

    date = datetime.date.today()

    if method == 'attendance':
        response = getAttendance()
    elif method == 'today':
        date = date.strftime('%Y-%m-%d')
        response = getDay(date)
    elif method == 'attendanceForToday':
        date = date.strftime('%Y-%m-%d')
        response = getAttendanceForDay(date)
    elif method == 'tomorrow':
        date = date + datetime.timedelta(days=1)
        date = date.strftime('%Y-%m-%d')
        response = getDay(date)
    elif method == 'yesterday':
        date = date - datetime.timedelta(days=1)
        date = date.strftime('%Y-%m-%d')
        response = getAttendanceForDay(date)

    bot.sendMessage(chat_id=chatID, text=response)

    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    bot = telegram.Bot(token=os.environ.get('TOKEN'))
    URL = f'https://{request.args.get("name")}.herokuapp.com/'
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=os.environ.get('TOKEN')))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

if __name__ == '__main__':
    app.run()