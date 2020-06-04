import os
import re
import random

from nonebot import on_command, CommandSession, MessageSegment, NoneBot
from nonebot.exceptions import CQHttpError

from hoshino import R, Service, Privilege
from hoshino.util import FreqLimiter, DailyNumberLimiter

_max = 10
EXCEED_NOTICE = f'您今天已经冲过{_max}次了，请明早5点后再来！'
_nlmt = DailyNumberLimiter(_max)
_flmt = FreqLimiter(5)

sv = Service('setu', manage_priv=Privilege.SUPERUSER, enable_on_default=True, visible=False)
setu_folder = R.img('setu/').path


JIO = 'jio'
NAIZI = 'naizi'
PANTSU = 'pantsu'


def setu_gener():
    setus = []
    for root, dirs, files in os.walk(setu_folder):
        for file in files:
            setus.append(os.path.join(root, file))
    now = 0
    if now == 0:
        random.shuffle(setus)
    now = (now + 1) % len(setus)
    yield R.img(setus[now])


def jio_gener():
    setus = []
    path = os.path.join(setu_folder, JIO)
    for root, dirs, files in os.walk(path):
        for file in files:
            setus.append(os.path.join(root, file))
    now = 0
    if now == 0:
        random.shuffle(setus)
    now = (now + 1) % len(setus)
    yield R.img(setus[now])


def naizi_gener():
    setus = []
    path = os.path.join(setu_folder, PANTSU)
    for root, dirs, files in os.walk(path):
        for file in files:
            setus.append(os.path.join(root, file))
    now = 0
    if now == 0:
        random.shuffle(setus)
    now = (now + 1) % len(setus)
    yield R.img(setus[now])


def pantsu_gener():
    setus = []
    path = os.path.join(setu_folder, JIO)
    for root, dirs, files in os.walk(path):
        for file in files:
            setus.append(os.path.join(root, file))
    now = 0
    if now == 0:
        random.shuffle(setus)
    now = (now + 1) % len(setus)
    yield R.img(setus[now])


setu_gener = setu_gener()
jio_gener = jio_gener()
naizi_gener = naizi_gener()
pantsu_gener = pantsu_gener()


@sv.on_rex(re.compile(r'不够[涩瑟色]|[涩瑟色]图|来一?[点份张].*[涩瑟色]|再来[点份张]|看过了|铜'), normalize=True)
async def normal(bot:NoneBot, ctx, match):
    await setu(bot, ctx, setu_gener)


@sv.on_rex(re.compile(r'舔脚|我要舔脚|舔jio|jio|脚'), normalize=True)
async def normal(bot:NoneBot, ctx, match):
    await setu(bot, ctx, jio_gener)


@sv.on_rex(re.compile(r'奶子|我要奶子'), normalize=True)
async def normal(bot:NoneBot, ctx, match):
    await setu(bot, ctx, naizi_gener)


@sv.on_rex(re.compile(r'胖次|我要胖次'), normalize=True)
async def normal(bot:NoneBot, ctx, match):
    await setu(bot, ctx, pantsu_gener)


async def setu(bot:NoneBot, ctx, gener):
    """随机叫一份涩图，对每个用户有冷却时间"""
    uid = ctx['user_id']
    if not _nlmt.check(uid):
        await bot.send(ctx, EXCEED_NOTICE, at_sender=True)
        return
    if not _flmt.check(uid):
        await bot.send(ctx, '您冲得太快了，请稍候再冲', at_sender=True)
        return
    _flmt.start_cd(uid)
    _nlmt.increase(uid)

    # conditions all ok, send a setu.
    pic = gener.__next__()
    try:
        await bot.send(ctx, pic.cqcode)
    except CQHttpError:
        sv.logger.error(f"发送图片{pic.path}失败")
        try:
            await bot.send(ctx, '涩图太涩，发不出去勒...')
        except:
            pass
