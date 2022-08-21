#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__     = "BSD 3-Clause License"
__version__     = "0.1"

import os
import json
import discord
import random

from os.path import join, dirname
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands
from threading import Thread

# load .env file
dir_path = os.path.dirname(os.path.realpath(__file__))

dotenv_path = join(dir_path, '.env')
load_dotenv(dotenv_path)

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# get path to data.json file
JSON_FILE = str(os.path.dirname(os.path.realpath(__file__))) + '/data.json'

# enable discord gateway intents
intents = discord.Intents.default()
intents.members = True

activity = discord.Streaming(name="!help", url="twitch.tv/noborder_")

bot = commands.Bot(command_prefix='/', activity=activity, intents=intents)

@bot.event
async def on_ready():
    """ Runs once the bot has established a connection with Discord """
    print(f'{bot.user.name} has connected to Discord')

    # check if bot has connected to guilds
    if len(bot.guilds) > 0:
        print('connected to the following guilds:')

        # list guilds
        for guild in bot.guilds:
            # display guild name, id and member count
            print(f'* {guild.name}#{guild.id}, nombre de membres: {len(guild.members)}.')
            # update the member count
            await update_member_count_channel_name(guild)


@bot.event
async def on_member_join(member):
    """ gets triggered when a new member joins a guild """
    print(f"* {member} joined {member.guild}")
    await update_member_count_channel_name(member.guild)


@bot.event
async def on_member_remove(member):
    """ gets triggered when a new member leaves or gets removed from a guild """
    print(f"* {member} left {member.guild}")
    await update_member_count_channel_name(member.guild)


@bot.command(name="update")
async def on_update_cmd(ctx):
    """ triggers manual update of member count channel """
    print(f"* {ctx.author} a actualisé le nombre de membres")
    await update_member_count_channel_name(ctx.guild)


@bot.command(name="info")
async def info(ctx):
    for guild in bot.guilds:
        print(f"* Appel de la commande donnant les informations du bot {bot.user.name} par {ctx.author}")
        await ctx.send(f"Je suis le bot personnalisé du serveur {guild.name}. J'appartiens à noborder#0314 !!")


@bot.command(name="commands")
async def commands(ctx):
    for guild in bot.guilds:
        print(f'* Appel de la commande donnant les commandes disponibles sur {guild.name} avec le bot {bot.user.name} par '
              f'{ctx.author}')
        await ctx.send(f"De nouvelles commandes sont en développement pour {bot.user.name}, commandes disponibles pour "
                       f"l'instant : !info !nbmembres !update (actualise le nombre de membres).")


@bot.command(name="nbmembres")
async def nbmembres(ctx):
    for guild in bot.guilds:
        print(f'* Appel de la commande donnant le nombre de membres sur {guild.name} par {ctx.author}')
        await ctx.send(f"Il y a {len(guild.members)} membres sur le serveur {guild.name}.")

async def update_member_count_channel_name(guild):
    """ updates the name of the member count channel """
    member_count_channel_id = get_guild_member_count_channel_id(guild)
    member_count_suffix = get_guild_member_count_suffix(guild)

    if member_count_channel_id != None and member_count_suffix != None:
        member_count_channel = discord.utils.get(guild.channels, id=member_count_channel_id)
        new_name = f"{get_guild_member_count(guild)} {member_count_suffix}"
        await member_count_channel.edit(name=new_name)

    else:
        print(f"* could not update member count channel for {guild}, id not found in {JSON_FILE}")


def get_guild_member_count(guild):
    """ returns the member count of a guild """
    return len(guild.members)


def get_guild_member_count_channel_id(guild):
    """ returns the channel id for the channel that should display the member count """
    with open(JSON_FILE) as json_file:
        # open JSON file
        data = json.load(json_file)
        for data_guild in data['guilds']:
            if int(data_guild['id']) == guild.id:
                return data_guild['channel_id']

            return None


def get_guild_member_count_suffix(guild):
    """ returns the the suffix that should be displayed after the member count """
    with open(JSON_FILE) as json_file:
        # open JSON file
        data = json.load(json_file)
        for data_guild in data['guilds']:
            if int(data_guild['id']) == guild.id:
                return data_guild['suffix']

            return None

# Setting `Playing ` status
#await bot.change_presence(activity=discord.Game(name="a game"))

# Setting `Streaming ` status
#await bot.change_presence(activity=discord.Streaming(name="Stream de noborder", url="twitch.tv/noborder_"))

# Setting `Listening ` status
#await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))

# Setting `Watching ` status
#await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))

if __name__ == "__main__":
    # launch bot
    bot.run(DISCORD_TOKEN)