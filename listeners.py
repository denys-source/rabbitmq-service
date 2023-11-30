import asyncio

from aio_pika import DeliveryMode, Message, connect
from aio_pika.abc import AbstractIncomingMessage
from colorama import Fore, Style

from handlers import MessageHandler
from utils import create_stdin_reader, read_line


class CommandListener:
    def __init__(
        self,
        host: str,
        port: int,
        login: str,
        password: str,
        virtualhost: str,
        message_handler: MessageHandler,
    ) -> None:
        self.host = host
        self.port = port
        self.login = login
        self.password = password
        self.virtualhost = virtualhost
        self.message_handler = message_handler

    async def on_command(self, command: AbstractIncomingMessage) -> None:
        await self.message_handler.handle_command(command)

    async def initialize(self) -> None:
        conn = await connect(
            host=self.host,
            port=self.port,
            login=self.login,
            password=self.password,
            virtualhost=self.virtualhost,
        )

        async with conn:
            channel = await conn.channel()
            await channel.set_qos(prefetch_count=1)

            queue = await channel.declare_queue("0", durable=True)

            await queue.consume(self.on_command)

            await self.message_handler.message_storage.append(
                f"{Fore.GREEN} [x] Waiting for commands. "
                f"Press ESC to submit command. Press Ctrl+C to exit{Style.RESET_ALL}"
            )
            await asyncio.Future()


class CommandInputListener:
    def __init__(
        self,
        host: str,
        port: int,
        login: str,
        password: str,
        virtualhost: str,
        message_handler: MessageHandler,
    ) -> None:
        self.host = host
        self.port = port
        self.login = login
        self.password = password
        self.virtualhost = virtualhost
        self.message_handler = message_handler

    async def initialize(self):
        conn = await connect(
            host=self.host,
            port=self.port,
            login=self.login,
            password=self.password,
            virtualhost=self.virtualhost,
        )

        async with conn:
            channel = await conn.channel()

            stdin_reader = await create_stdin_reader()

            while True:
                command = await read_line(stdin_reader)
                message = Message(
                    command.encode(), delivery_mode=DeliveryMode.PERSISTENT
                )

                await self.message_handler.message_storage.append(
                    f"{Fore.GREEN} [x] Sent command: {command}{Style.RESET_ALL}"
                )
                await channel.default_exchange.publish(
                    message, routing_key="0"
                )
