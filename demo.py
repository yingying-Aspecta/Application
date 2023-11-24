

import asyncio
import functools
import time
from graia.broadcast.entities.decorater import Decorater

from graia.broadcast.exceptions import ExecutionStop

from graia.application import GraiaMiraiApplication, Session
from graia.application.friend import Friend
from graia.application.message.chain import MessageChain
from graia.application.group import Group, Member
from graia.broadcast import Broadcast

from graia.application.message.elements.internal import At, AtAll, Plain

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080",  # 填入 httpapi 服务运行的地址
        authKey="INITKEY3BLVMyaZ",  # 填入 authKey
        account=2580055873,  # 你的机器人的 qq 号
        websocket=True  # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)


def at_me1(func):
    @functools.wraps(func)
    def wrapper(app: GraiaMiraiApplication, message: MessageChain):
        if app.connect_info.account not in list(x.target for x in message[At]):
            raise ExecutionStop()
        return func(app, message)
    return wrapper


def at_me(message: MessageChain):
    # if app.connect_info.account not in list(x.target for x in message[At]):
    if message[At] != []:
        raise ExecutionStop()


@bcc.receiver("GroupMessage", priority=1)
async def group_message_handler(app: GraiaMiraiApplication, message: MessageChain, group: Group, member: Member):
    # print(message.asDisplay())
    # print("message[At]===========", app.connect_info.account)
    # print(app.connect_info.account in list(x.target for x in message[At]))
    # print(member.id) ## QQ

    if message.asDisplay().startswith("hi") or app.connect_info.account not in list(x.target for x in message[At]):
        await app.sendGroupMessage(group, message.asSendable())
        await app.sendGroupMessage(group, MessageChain.create([
            Plain("你需要在消息中包含至少一张图片!"),
            At(member.id)
        ]))


@bcc.receiver("GroupMessage", priority=15)
async def group_message_handler(app: GraiaMiraiApplication, message: MessageChain, group: Group):
    if message.asDisplay().startswith("hihi"):
        await app.sendGroupMessage(group, MessageChain(__root__=[
            Plain("Hello, World!"),
        ]))
        time.sleep(1)
        await app.sendGroupMessage(group, MessageChain(__root__=[
            Plain("Hello, World2")
        ]))


@bcc.receiver("FriendMessage")
async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend):
    await app.sendFriendMessage(friend, MessageChain(__root__=[
        Plain("Hello, World!")
    ]))
    # print(friend.id)

app.launch_blocking()





