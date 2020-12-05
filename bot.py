import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from utils.functions import fetch_random_panel as frp
from utils.functions import is_valid
import time

#  global dict to keep track of user score in every server
#  key: (username, server id), value: user score in that server
scores = {}
valid_starters = ['what is ', 'What is ']
with open('config.txt', 'r') as f:
    TOKEN = f.readline().strip()

bot = commands.Bot(command_prefix='', case_insensitive=True, help_command=None)


def update_scores(message, score_update):
    global scores  # update dictionary globally
    if (message.author, message.guild.id) not in scores and score_update > 0:
        scores[(message.author, message.guild.id)] = score_update
    else:
        if scores[(message.author, message.guild.id)] + score_update < 0:
            scores[(message.author, message.guild.id)] = 0
        else:
            scores[(message.author, message.guild.id)] += score_update


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


# displays top scores in descending order
# scores are based on server
@bot.command(name='f.top')
async def display_server_scores(ctx):
    # makes sure bot doesn't respond to itself
    if ctx.author.bot:
        return
    print(str(ctx.message.author)+" requested scoreboard.")  # print check to console
    embed = discord.Embed(title=f'Top Scores on {ctx.message.guild.name}:', inline=False)
    if len(scores) == 0:
        embed.add_field(name="No Scores to Display!", value="Start playing by typing f.i", inline=False)
    sort_orders = sorted(scores.items(), key=lambda x: x[1], reverse=True)  # sorts dict in descending order
    for i in sort_orders:
        username = str(i[0][0])
        embed.add_field(name=username[:-5], value="$" + str(i[1]), inline=False)
    await ctx.send(embed=embed)


@bot.command(name='f.i', aliases=['f..i'])
async def await_rand_question(ctx):
    current_channel_id = ctx.channel.id
    # makes sure bot doesn't respond to itself
    if ctx.author.bot:
        return
    panel = frp()
    await ctx.send(embed=panel.get_embed())  # display panel
    # question/answer logic + time
    t_end = time.time() + 60
    while time.time() < t_end:
        try:
            attempt = await bot.wait_for('message')
            print('\"{}\" was sent by {} in channel:\'{}\''.format(attempt.content, attempt.author, attempt.channel.name))  # print to console
            if attempt.author.bot:
                return  # if the bot responds, end the function right away
            elif current_channel_id != attempt.channel.id:
                continue  # if the channel doesn't match, try again
            elif attempt.content in ['f.i', 'f.top']:
                break
            elif is_valid(attempt.content, panel):
                await ctx.send('Correct {}! You get ${}'.format(str(attempt.author)[:-5], panel.get_value()))
                update_scores(attempt, panel.get_value())  # increase score here
                return
            elif attempt.content != panel.get_answer():
                # print('Incorrect check\n')
                await ctx.send('That is incorrect {}. You lost ${}'.format(str(attempt.author)[:-5], panel.get_value()))
                update_scores(attempt, -1*panel.get_value())  # decrease score here
        except Exception as e:
            print("EXCEPTION: " + str(e))
    await ctx.send('Times up! The correct answer was \'{}\''.format(panel.get_answer()))

bot.run(TOKEN.strip())
