import discord
from discord.ext import commands
import random
from utils.functions import fetch_random_panel as frp
from utils.question import QuestionPanel
import time
import asyncio


with open('config.txt', 'r') as f:
    TOKEN = f.readline().strip()

bot = commands.Bot(command_prefix='', case_insensitive=True, help_command=None)


@bot.event
async def on_ready():
    print('Bot online')
    print('Name: {}'.format(bot.user.name))
    print('ID: {}'.format(bot.user.id))


@bot.event
async def on_message(message):
    if message.content == 'host?':
        await message.channel.send("Hi. I'm your host!")
    await bot.process_commands(message)


def check(m, panel):
    return m.content == panel.get_answer()


@bot.command(name='t.q', aliases=['Random'])
async def await_rand_question(ctx):
    # makes sure bot doesn't respond to itself
    if ctx.author.bot:
        return
    attempt = ''
    random_row = int(random.random()*216930)
    panel = frp(random_row)
    await ctx.send(embed=panel.get_embed())
    t_end = time.time() + 5
    while True:
        try:
            attempt = await bot.wait_for('message')
            print('\"{}\" was sent by {}'.format(attempt.content, attempt.author))
            if time.time() > t_end:
                await ctx.send('You ran out of time!')
                return
            elif attempt == 't.q':
                return
            elif attempt.content == panel.get_answer():
                await ctx.send('Correct!')
                return
            else:
                await ctx.send('incorrect...')
                continue
        except asyncio.TimeoutError:
            await ctx.send('Time out error...')


bot.run(TOKEN.strip())
