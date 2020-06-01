# bot.py - https://realpython.com/how-to-make-a-discord-bot-python/
import os
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='%')

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@bot.command(name='mock', help='Mocks, like dank memer.')
async def mock(ctx, statement: str):
    statement = statement.lower()
    mocked_statement = ''

    for i in range(len(statement)):
        letter_add = statement[i]
        if i % 2 == 0:
            letter_add = letter_add.upper()
        mocked_statement += letter_add

    await ctx.send(mocked_statement)

bot.run(TOKEN)