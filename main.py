import os
import sys
import asyncio
import logging

from aio_pika.exceptions import AMQPConnectionError
from colorama import init as colorama_init
from colorama import Fore, Style
from dotenv import load_dotenv
from aiogram.utils.token import TokenValidationError

from storage import MessageStorage
from utils import (
    add_signal_handlers,
    configure_terminal,
    redraw_messages,
)
from handlers import MessageHandler, BotHandler
from listeners import CommandListener, CommandInputListener


load_dotenv()


AMQP_USER = os.environ.get("AMQP_USER", "guest")
AMQP_PASSWORD = os.environ.get("AMQP_PASSWORD", "guest")
AMQP_ADDRESS = os.environ.get("AMQP_ADDRESS", "localhost")
AMQP_VHOST = os.environ.get("AMQP_VHOST", "/")
AMQP_PORT = os.environ.get("AMQP_PORT", 5672)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
EXTERNAL_API_URL = os.environ.get("EXTERNAL_API_URL")


colorama_init()

logging.basicConfig(level=logging.DEBUG, filename="logs.log")


async def main():
    total_rows = configure_terminal()
    num_messages = total_rows - 1

    message_storage = MessageStorage(redraw_messages, num_messages)
    message_handler = MessageHandler(
        message_storage, external_url=EXTERNAL_API_URL
    )

    bot_handler = BotHandler(BOT_TOKEN, message_handler)
    command_listener = CommandListener(
        host=AMQP_ADDRESS,
        port=AMQP_PORT,
        login=AMQP_USER,
        password=AMQP_PASSWORD,
        virtualhost=AMQP_VHOST,
        message_handler=message_handler,
    )
    command_input_listener = CommandInputListener(
        host=AMQP_ADDRESS,
        port=AMQP_PORT,
        login=AMQP_USER,
        password=AMQP_PASSWORD,
        virtualhost=AMQP_VHOST,
        message_handler=message_handler,
    )

    tasks = [
        asyncio.create_task(bot_handler.initialize()),
        asyncio.create_task(command_listener.initialize()),
        asyncio.create_task(command_input_listener.initialize()),
    ]

    add_signal_handlers()

    try:
        await asyncio.gather(*tasks)
    except AMQPConnectionError:
        await message_storage.append(
            f"{Fore.RED}Connect call failed!{Style.RESET_ALL}"
        )
        logging.exception("Connect call failed!")
        sys.exit(1)
    except TokenValidationError:
        await message_storage.append(
            f"{Fore.RED}Telegram token is invalid{Style.RESET_ALL}"
        )
        logging.exception("Telegram token is invalid!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
