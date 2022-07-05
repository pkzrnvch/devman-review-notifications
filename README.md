# Devman review notifications bot

This program uses [Devman](https://dvmn.org) API to check whether any of the submitted tasks have been reviewed, and sends user a notification via a telegram bot.

### How to install

- Create an `.env` file in the project directory. Create a new telegram bot through a BotFather and assign its token to `TG_TOKEN` variable. 
- In case you have an account, you can find your token for Devman API [here](https://dvmn.org/api/docs/), assign it to `DEVMAN_TOKEN` variable. 
- Send a message to [@userinfobot](https://t.me/userinfobot) to get your chat_id, assign it to `TG_CHAT_ID` variable. 

Example of an `.env` file:

```
TG_BOT_TOKEN=YOUR_TOKEN
DEVMAN_TOKEN=YOUR_TOKEN
TG_CHAT_ID=YOUR_CHAT_ID
```

Python3 should already be installed. Use pip (or pip3, in case of conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### Usage

To run the program use the following command from the project directory:
```
python main.py
```

### To run with Docker

- Install [Docker](https://www.docker.com/products/docker-desktop/)
- Use the following command from the project directory to create image:
```
docker build -t notifications-bot .
```
- After that, another one to run a container:
```
docker run --env-file <path_to_env_file> devman-notifications-bot
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [Devman](https://dvmn.org).
