import os
from flask import Flask, request, jsonify
import telegram

app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')

bot = telegram.Bot(token=TOKEN)

@app.route('/')
def default():
    return 'monday api built using flask by @sksuryan'

@app.route('/{}'.format(TOKEN),methods=['post'])
def respond():
    update = telegram.Update.de_json(request.get_json(),bot)
    chatID = update.message.chat.id

    bot.sendMessage(chat_id=chatID, text='suppp')

    return 'ok'

if __name__ == '__main__':
    app.run()