from collections import deque
from collections.abc import Awaitable, Callable


class MessageStorage:
    def __init__(
        self, callback: Callable[[deque], Awaitable[None]], max_size: int
    ) -> None:
        self._messages: deque[str] = deque(maxlen=max_size)
        self._callback = callback

    async def append(self, message: str) -> None:
        self._messages.append(message)
        await self._callback(self._messages)
