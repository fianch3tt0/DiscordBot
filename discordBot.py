import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("API_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in successfully as {bot.user.name}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

bot.run(token)