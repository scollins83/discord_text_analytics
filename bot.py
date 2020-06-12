# bot.py - https://realpython.com/how-to-make-a-discord-bot-python/
import os
import random
from summarizer import Summarizer
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='%')
client = discord.Client()

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

@bot.command(name='tldr_stmt', help="Summarizes a statement")
async def tldr_stmt(ctx, statement: str, length: int):
    model = Summarizer()
    result = model(statement, min_length=length)
    summary = ''.join(result)

    await ctx.send(summary)

@bot.command(name='tldr', help="Summarizes a channel. Enter %tldr followed by the channel name and receive an \
                               extractive summary of that channel.")
async def tldr(ctx, channel: discord.TextChannel):
    messages = await channel.history(limit=None).flatten()
    msg_filtered = []
    for msg in messages:
        if msg.content.startswith('%tldr'):
            pass
        elif msg.author == client.user:
            pass
        else:
            msg_filtered.append(msg.content.replace('<@', 'UserID_'))

    summ_messages = " ".join([msg for msg in msg_filtered])

    logger.info("Summarizing content of channel {}".format(channel.name))
    model = Summarizer()
    result = model(summ_messages, min_length=100)
    summary = ''.join(result)

    logger.info('Summary: {}'.format(summary))

    return_message = "**Summary of channel: {}** \n {}".format(channel.name, summary)

    author = ctx.author
    await author.send(return_message)

bot.run(TOKEN)