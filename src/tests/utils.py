from typing import TYPE_CHECKING

from nonebug.mixin.call_api import ApiContext

if TYPE_CHECKING:
    from nonebot.adapters.onebot.v11 import Message as OB11Message
    from nonebot.adapters.onebot.v11 import Bot as OB11Bot


def create_obv11_bot(ctx: ApiContext) -> "OB11Bot":
    from nonebot import get_adapter
    from nonebot.adapters.onebot.v11 import Adapter as OB11Adapter
    from nonebot.adapters.onebot.v11 import Bot as OB11Bot

    return ctx.create_bot(
        base=OB11Bot,
        adapter=get_adapter(OB11Adapter.get_name())
    )


def mock_obv11_message_event(message: "OB11Message", group: bool = False, message_id: int = 1234):
    from nonebot.adapters.onebot.v11.event import Sender
    from nonebot.adapters.onebot.v11 import GroupMessageEvent as OB11GroupMessageEvent
    from nonebot.adapters.onebot.v11 import (
        PrivateMessageEvent as OB11PrivateMessageEvent,
    )

    if not group:
        return OB11PrivateMessageEvent(
            time=1122,
            self_id=2233,
            post_type="message",
            sub_type="",
            user_id=2233,
            message_type="private",
            message_id=message_id,
            message=message,
            original_message=message,
            raw_message=str(message),
            font=1,
            sender=Sender(user_id=2233),
            to_me=False,
        )
    else:
        return OB11GroupMessageEvent(
            time=1122,
            self_id=2233,
            group_id=3344,
            post_type="message",
            sub_type="",
            user_id=2233,
            message_type="group",
            message_id=message_id,
            message=message,
            original_message=message,
            raw_message=str(message),
            font=1,
            sender=Sender(user_id=2233),
            to_me=False,
        )
