import discord
from discord.ext import commands
import time

intents = discord.Intents.all()
# intents.members = True
bot = commands.Bot(command_prefix='Hi Phil, ', intents=intents)

@bot.event
async def on_ready():
  await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Plant Farming Simulator"))
  channel = bot.get_channel(1058332414860079155)
  await channel.send("bear wants to let u know he loves u <33")
  await bot.change_presence(status=discord.Status.dnd, activity=None)

