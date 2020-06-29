import os
import random
import time
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix='!')

enrollments = {}


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command(name='enroll', help="Enrolls YOU in the Player list.")
async def enroll(ctx):
    raw_player = ctx.message
    channel = raw_player.channel.id
    player_id = raw_player.author.id
    player_name = raw_player.author.name
    player = []
    player.append(player_id)
    player.append(player_name)

    # See if channel in dict
    look_for_channel(ctx.message.channel.id)

    if player not in enrollments[channel]:
        enrollments[channel].append(player)
        await ctx.send("{} has been added to the players list".format(player[1]))
    else:
        await ctx.send("{} already in the players list".format(player[1]))


@bot.command(name='list', help="List players enrolled in the player order generator.")
async def list(ctx):
    count = 0
    look_for_channel(ctx.message.channel.id)
    print(enrollments[ctx.message.channel.id])
    players_output = ''
    for player in enrollments[ctx.message.channel.id]:
        count += 1
        players_output += "{}. {}\n".format(count, player[1])
    await ctx.send("Players Enrolled:\n{}".format(players_output))


@bot.command(name='reset', help="Remove all players from Players list.")
async def reset(ctx):
    look_for_channel(ctx.message.channel.id)
    del enrollments[ctx.message.channel.id][0:]
    await ctx.send("All Players have been removed from the Players list.")


@bot.command(name='generate', help='Generate Player Order')
async def generate(ctx):
    look_for_channel(ctx.message.channel.id)
    async with ctx.typing():
        await ctx.send("Generating player order...")
        time.sleep(random.randrange(1, 6))
        random.shuffle(enrollments[ctx.message.channel.id])
        player_output = ''
        position = 0
        for player in enrollments[ctx.message.channel.id]:
            position += 1
            player_output += '{}. {}\n'.format(position, player[1])
        await ctx.send("Your Player order is:\n{}".format(player_output))


@bot.command(name='unenroll', help='Removes all players from Players list.')
async def unenroll(ctx):
    raw_player = ctx.author
    player = []

    player.append(raw_player.id)
    player.append(raw_player.name)

    for p in enrollments[ctx.message.channel.id]:
        if player == p:
            del enrollments[ctx.message.channel.id][enrollments[ctx.message.channel.id].index(p)]

    await ctx.send('{} has been removed from the Players list.'.format(player[1]))


@bot.command(name='remove', help='Remove specified user from Players list.')
async def remove(ctx):
    user_input = ctx.message.content[8:]
    player_position = -1
    print(int(user_input))
    try:
        player_position = int(user_input) - 1
        print(player_position)
    except ValueError:
        await ctx.send("Input must be a number")

    if player_position >= 0:
        try:
            name = enrollments[ctx.message.channel.id][player_position][1]
            del enrollments[ctx.message.channel.id][player_position]
            await ctx.send("{} has been removed from the Players List".format(name))
        except IndexError:
            await ctx.send("There is no player {}".format(player_position + 1))
    else:
        await ctx.send("There is no player {}".format(player_position + 1))


@bot.command(name='enrollplayer', help='Force enroll a user')
async def enrollplayer(ctx):
    user_input = ctx.message.content[14:]
    player = []
    player.append("1")
    player.append(user_input)
    if player not in enrollments[ctx.message.channel.id]:
        enrollments[ctx.message.channel.id].append(player)
        await ctx.send("{} has been added to the players list".format(player[1]))
    else:
        await ctx.send("{} already in the players list".format(player[1]))


@bot.command(name='dev')
async def dev(ctx):
    print(ctx.message)
    print(ctx.message.channel.id)
    print(ctx.message.author.id)
    print(ctx.message.author.name)


def look_for_channel(channel):
    # See if channel in list
    if channel not in enrollments:
        enrollments[channel] = []


bot.run(TOKEN)
