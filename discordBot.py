import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("API_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

words = ["python", "java", "steam", "javascript"]
chosen_word = ""
word_display = []
attempts = 6
guessed_letters = []

@bot.event
async def on_ready():
    print(f"Logged in successfully as {bot.user.name}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def hangman(ctx, guess: str = None):
    global chosen_word, word_display, attempts, guessed_letters

    if not chosen_word:
        chosen_word = random.choice(words)
        word_display = ["_" for _ in chosen_word]
        attempts = 6
        guessed_letters = []
        await ctx.send(f"Hangman game started.\nWord: `{' '.join(word_display)}` \nGuess a letter using `!hangman [letter]`")
        return

    if not guess:
        await ctx.send("Please provide a letter. Example: `!hangman a`")
        return

    guess = guess.lower()

    if guess in guessed_letters:
        await ctx.send(f"You have already guessed the letter `{guess}`.")
        return

    guessed_letters.append(guess)

    if guess in chosen_word:
        for i in range(len(chosen_word)):
            if chosen_word[i] == guess:
                word_display[i] = guess
        await ctx.send(f"Correct guess. `{guess}` is in the word.")
    else:
        attempts -= 1
        await ctx.send(f"Incorrect guess. `{guess}` is not in the word. Remaining attempts: {attempts}")

    await ctx.send(f"`{' '.join(word_display)}`")

    if "_" not in word_display:
        await ctx.send(f"Game won. The correct word was **{chosen_word}**.")
        chosen_word = ""  
    elif attempts <= 0:
        await ctx.send(f"Game over. The correct word was **{chosen_word}**.")
        chosen_word = ""  

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    server_name = guild.name
    member_count = guild.member_count
    created_at = guild.created_at.strftime("%B %d, %Y")
    
    response = (
        f"Server Name: {server_name}\n"
        f"Total Members: {member_count}\n"
        f"Creation Date: {created_at}"
    )
    await ctx.send(response)

@bot.command()
async def userinfo(ctx):
    user = ctx.author
    response = (
        f"User: {user.display_name}\n"
        f"Joined Server: {user.joined_at.strftime('%B %d, %Y')}\n"
        f"ID: {user.id}"
    )
    await ctx.send(response)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def deletemsg(ctx, amount: int = 0):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Cleared {amount} messages.", delete_after=3)

bot.run(token)