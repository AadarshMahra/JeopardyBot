import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import random
from utils.functions import fetch_random_panel as frp
from utils.functions import is_valid
from utils.question import QuestionPanel
import time



with open('config.txt', 'r') as f:
    TOKEN = f.readline().strip()

bot = commands.Bot(command_prefix='', case_insensitive=True, help_command=None)


@bot.event
async def on_ready():
    print('Bot online')
    print('Name: {}'.format(bot.user.name))
    print('ID: {}'.format(bot.user.id))

# ignore CommandNotFound Errors !
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

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

    random_row = int(random.random()*216930)
    panel = frp(random_row)
    await ctx.send(embed=panel.get_embed())  # display panel

    t_end = time.time() + 60
    while time.time() < t_end:
        try:
            attempt = await bot.wait_for('message')
            print('\"{}\" was sent by {}'.format(attempt.content, attempt.author))  # for console
            if attempt.content == 't.q':
                break
            elif is_valid(attempt.content, panel.get_answer()):
                await ctx.send('Correct {}!'.format(str(attempt.author)[:-5]))
                return
            elif attempt.content != panel.get_answer():
                await ctx.send('That is incorrect {}.'.format(str(attempt.author)[:-5]))
                continue
        except Exception as e:
            print(e)
    await ctx.send('Times up! The correct answer was \'{}\''.format(panel.get_answer()))

bot.run(TOKEN.strip())
