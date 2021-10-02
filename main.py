import os

import discord
import datetime
from discord.ext import commands


client = commands.Bot(command_prefix=".", description='Paü discord botu')



@client.event
async def on_ready():
    print(f"[{datetime.date.today()}] Bot başlatılıyor..\n")
    await client.change_presence(status=discord.Status.idle,
                                 activity=discord.Activity(type=discord.ActivityType.watching, name="Paü'yü"))
    setup()

def setup():
    for file in os.listdir("cogs"):
        if ".py" in file:
            try:
                client.load_extension(f"cogs.{file.replace('.py','')}")
            except Exception as e:
                print(e)
client.run("", bot=True, reconnect=True)