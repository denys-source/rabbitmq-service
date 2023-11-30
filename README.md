# RabbitMQ Service 🐰

This application listens to a RabbitMQ queue and dynamically retrieves the latest incoming message sent to a Telegram bot, responding to the message content. The application displays messages on-screen as soon as they are sent to the Telegram bot while concurrently processing commands from the RabbitMQ queue.

## ⚙️ Installing using GitHub

Linux/MacOS:

```shell
git clone https://github.com/denys-source/rabbitmq-service
cd rabbitmq-service/
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Windows:
```shell
git clone https://github.com/denys-source/rabbitmq-service
cd rabbitmq-service/
python venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Set environment variables using `.env.sample`.
Use following bot token to test it out:
```
6647145707:AAGTjvstSgdw4zM-PoUcDIB0C0WWHiqo7-8
```
You can access bot at https://t.me/rabbitmq_service_bot

To run application execute:
```
python3 main.py
```


## 🐳 Running with docker

Install Docker and set environment variables. Then execute:
```shell
docker-compose run --build --rm app
```

## 📍 Features

* **RabbitMQ Integration:** Listens to a RabbitMQ queue for incoming messages.
* **Telegram Bot Integration:** Retrieves the latest incoming message sent to a Telegram bot.
* **Dynamic Message Handling:** Processes the content of the received Telegram message dynamically.
* **Real-Time Display:** Displays Telegram messages on-screen immediately upon their arrival.
* **Continuous Listening:** Continuously listens to the RabbitMQ queue for incoming messages and processes commands.
* **Flexible Command Processing:** Handles various commands received from the RabbitMQ queue.

## ✅ Demo

![image](https://github.com/denys-source/rabbitmq-service/assets/72623693/ec8fc2e9-60dc-4f3c-af52-503e2ee208d1)
