# monday-api 👷‍♂
api for Telegram Bot that automates attendance for Amitians.

## Endpoints 🛠
```/<TELEGRAM BOT TOKEN>``` - is set up as a webhook, and replies to messages sent to the Telegram Bot.

```/<AUTORES>?method=<available methods>``` - Requests to this endpoint are made from cron-job.org , to send messages automatically.
#### available methods:
* attendance - to get overall attendance
* attendanceForToday - to get today's attendance
* today - to get today's classes

```/setwebbook``` - is called only once to set the webhook for Telegram Bot

## Environmental Variables 🤔
* TOKEN - Telegram Bot token
* AUTORES - Any random string, just to keep someone else away from using second endpoint, and spamming you using your Bot.
* USERNAME - Amizone username
* PASSWORD - Amizone password
* CHATID - Telegram chat ID 

## setting up the Bot asap 🐇
1. Create a telegram bot using BotFather. Check intructions [here](https://www.process.st/telegram-bot/).
2. Keep the TOKEN given by BotFather, you'll need it later.
3. Start the telegram bot and go to the URL given below to get your Chat ID, you'll need it too.
```
https://api.telegram.org/bot<YourBOTToken>/getUpdates
```
4. Fork the repo.
5. Deploy on heroku using github and enable automatic deployment.
6. Set up all the environmental variable by going into project settings.
7. Go to the URL given below, to make your Chat bot work.
```
https://<your heroku url>/setwebhook
```
8. Create an account on [cron-job.org](https://cron-job.org) and create Cron Jobs according to your requirements. Use the second endpoint as request URL and add method as query. 

#### There maybe changes or fixes so keep the fork up to date 😉
Read about it [here](https://garrytrinder.github.io/2020/03/keeping-your-fork-up-to-date).

#### Feel free to contribute 🤝

#### Star if it helped! Thanks! 😁
Have a good day!