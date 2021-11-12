import os
from discord import *
from discord.ext import commands
import cogs.cb_util as util

TOKEN = os.getenv('DISCORD_TOKEN')

# activity = Game(name=gameStatus)
# activity = Streaming(name="c!help", url="twitch_url_here")
# activity = Activity(type=ActivityType.listening, name="!help")
# activity = Activity(type=ActivityType.watching, name="!help")

bot = commands.Bot(command_prefix=util.prefix, status=Status.online)

verbose_start = False

@bot.event
async def on_ready():
    bt_channel = bot.get_channel(util.channel_ids['BT-casbot']) 

    try:
        storage_channel = bot.get_channel(util.free_storage['CHANNEL'])
        storage_message = await storage_channel.fetch_message(util.free_storage['rel_ver'])

        release_ver = int(storage_message.content.replace("release version ", '')) + 1
        await storage_message.edit(content="release version "+str(release_ver))
    except Exception as e:
        err = e
        release_ver = None

    online_msg = await bt_channel.send(':cold_face: CASbot is online! rv '+str(release_ver))
    # await online_msg.edit(content = online_msg.content + f'\n:warning: Error.\n```\n{err}\n```') if err else None

    for ext in util.cog_exts:
        try:
            bot.load_extension('cogs.cog_'+ext)
            await online_msg.edit(content = online_msg.content + f'\n:white_check_mark: Cog extension `{ext}` loaded successfully!') if verbose_start else None
        except Exception as err:
            await online_msg.edit(content = online_msg.content + f'\n:warning: Could not load cog extension `{ext}`.\n```\n{err}\n```')

bot.run(TOKEN)
