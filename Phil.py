import config
import discord
import asyncio
import PlantFarm
from discord.ext import commands

async def farm_loop():
  PlantFarm.plant_farm(True)


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='phil, ', intents=intents)

@bot.command()
async def start(ctx):
  bot.loop.create_task(farm_loop)
  await ctx.send('Farm loop started on Bear\'s park.')

@bot.command()
async def stop(ctx):
  tasks = [task for task in asyncio.all_tasks() if task.get_name() == 'farm_loop']
  for task in tasks:
    task.cancel()
  await ctx.send('Farm loop terminated on Bear\'s park.')

@bot.event
async def on_ready():
  await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Plant Farming Simulator"))
  channel = bot.get_channel(config.CHANNEL_ID)
  await channel.send("Phil is online")
  
bot.run(config.BOT_TOKEN)