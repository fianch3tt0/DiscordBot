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


bot.run(token)