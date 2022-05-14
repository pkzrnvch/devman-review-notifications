# Devman review notifications bot

This program uses [Devman](https://dvmn.org) API to check whether any of the submitted tasks have been reviewed, and sends user a notification via a telegram bot.

### How to install

- Create an `.env` file in the project directory. Create a new telegram bot through a BotFather and assign its token to `TG_TOKEN` variable. 
- In case you have an account, you can find your token for Devman API [here](https://dvmn.org/api/docs/), assign it to `DEVMAN_TOKEN` variable. 
- Send a message to [@userinfobot](https://t.me/userinfobot) to get your chat_id, assign it to `TG_CHAT_ID` variable. 

Example of an `.env` file:

```
TG_BOT_TOKEN="YOUR_TOKEN"
DEVMAN_TOKEN="YOUR_TOKEN"
TG_CHAT_ID="YOUR_CHAT_ID"
```

Python3 should already be installed. Use pip (or pip3, in case of conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### Usage

To run the programm use the following command from the project directory:
```
python main.py
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [Devman](https://dvmn.org).
