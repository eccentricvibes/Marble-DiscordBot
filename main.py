import aiohttp
from discord.ext import commands
import os
import asyncio


def bot_task_callback(future: asyncio.Future):
    if future.exception():
        raise future.exception()


async def run_bot():
    try:
        bot = commands.Bot(command_prefix='!')
        bot.session = aiohttp.ClientSession()
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                bot.load_extension(f"cogs.{file[:-3]}")
        await bot.start('BOT_TOKEN')
    finally:
        if isinstance(bot.session, aiohttp.ClientSession):
            await bot.session.close()
        await bot.close()


loop = asyncio.get_event_loop()
try:
    future = asyncio.ensure_future(
        run_bot(),
        loop=loop
    )
    future.add_done_callback(bot_task_callback)
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.close()


# import aiohttp
# from discord.ext import commands
# import discord
# import os
#
# bot = commands.Bot(command_prefix='!')
# bot.session = aiohttp.ClientSession()
# await session.close()
#
# for file in os.listdir('./cogs'):
#     if file.endswith('.py'):
#         bot.load_extension(f"cogs.{file[:-3]}")
#
# bot.run('ODc1MDg2NTU4MzY0MDUzNTQ0.YRQZ3Q.HxUfUjleEqviH51M8XkdOBJMs6M')
