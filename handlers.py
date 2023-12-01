import aiohttp
from aio_pika.abc import AbstractIncomingMessage
from aiogram import Bot, Dispatcher
from aiogram.types import Message as AiogramMessage
from colorama import Fore, Style

from storage import MessageStorage


class MessageHandler:
    def __init__(
        self, message_storage: MessageStorage, external_url: str
    ) -> None:
        self.message_storage = message_storage
        self.last_message = None
        self.external_url = external_url

    async def handle_telegram_message(self, message: AiogramMessage):
        self.last_message = message.text
        await self.message_storage.append(
            f"{Fore.YELLOW}Telegram message: {self.last_message}{Style.RESET_ALL}"
            if self.last_message
            else f"{Fore.RED}Message doesn't contain text{Style.RESET_ALL}"
        )

    async def handle_command(self, command: AbstractIncomingMessage):
        if command.body == b"print":
            await self.message_storage.append(
                f"Last message: {self.last_message}"
            )
        elif command.body == b"send":
            if not self.external_url:
                await self.message_storage.append(
                    f"{Fore.RED}External API url is not set{Style.RESET_ALL}"
                )
            else:
                await self.message_storage.append(
                    f"{Fore.GREEN} [x] Sending POST request to {self.external_url}{Style.RESET_ALL}"
                )
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        self.external_url,
                        json={"last_message": self.last_message},
                    ) as resp:
                        await self.message_storage.append(
                            f"Response status code: {resp.status}"
                        )

        await command.ack()


class BotHandler:
    def __init__(
        self, bot_token: str, message_handler: MessageHandler
    ) -> None:
        self.bot_token = bot_token
        self.message_handler = message_handler
        self.dp = Dispatcher()

    async def initialize(self) -> None:
        bot = Bot(self.bot_token)
        self.dp.message.register(self.echo_message)
        await self.dp.start_polling(bot, handle_signals=False)

    async def echo_message(self, message: AiogramMessage) -> None:
        await self.message_handler.handle_telegram_message(message)
