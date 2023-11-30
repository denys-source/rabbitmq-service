import os
import signal
import asyncio
import tty
import sys
from asyncio import StreamReader, StreamReaderProtocol
from collections import deque

from ansi_controls import (
    clear_line,
    delete_line,
    move_back_one_char,
    move_to_bottom_of_screen,
    move_to_top_of_screen,
    restore_cursor_position,
    save_cursor_position,
)


async def read_line(stream: StreamReader) -> str:
    buffer: deque[str] = deque()
    delete_char = b"\x7f"

    def clear_last_char() -> None:
        move_back_one_char()
        sys.stdout.write(" ")
        move_back_one_char()

    while (char := await stream.read(1)) != chr(27).encode():
        if char == delete_char:
            if len(buffer) > 0:
                buffer.pop()
                clear_last_char()
                sys.stdout.flush()
        else:
            decoded_char = char.decode()
            buffer.append(decoded_char)
            sys.stdout.write(decoded_char)
            sys.stdout.flush()
    clear_line()
    return "".join(buffer)


async def redraw_messages(messages: deque) -> None:
    save_cursor_position()
    move_to_top_of_screen()

    for message in messages:
        delete_line()
        print(message)

    restore_cursor_position()


async def create_stdin_reader() -> StreamReader:
    stream_reader = StreamReader()
    protocol = StreamReaderProtocol(stream_reader)
    loop = asyncio.get_running_loop()
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    return stream_reader


def add_signal_handlers() -> None:
    loop = asyncio.get_running_loop()

    async def shutdown() -> None:
        tasks = []
        for task in asyncio.all_tasks():
            if task is not asyncio.current_task():
                task.cancel()
                tasks.append(task)
        loop.run_until_complete(*tasks)
        loop.stop()

    for sig in [signal.SIGINT, signal.SIGTERM]:
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown()))


def configure_terminal() -> int:
    os.system("")
    tty.setcbreak(sys.stdin)
    os.system("clear")

    total_rows = move_to_bottom_of_screen()
    return total_rows
