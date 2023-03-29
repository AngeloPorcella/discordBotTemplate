# bot.py
# Made by Angelo P
import os
import random
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)  # Commands when I can figure out how exactly this works
global guild


# Code block activates when bot goes online
@client.event
async def on_ready():
    global guild
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(f'{client.user} is connected to {guild.name} (id:{guild.id})')


# new members to the server will be DM'd by the bot (if active)
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hello  {member.name}, This is a custom message sent to new members'
    )

# TODO Add more stats to stats file
# Increments count inside a file when called.
def updateCount():
    with open("stats.txt", "r") as file:
        count = int(file.read().strip())
    count += 1
    with open("stats.txt", "w") as file:
        file.write(str(count))


# Returns number of times the bot has been used
def getCount():
    with open("stats.txt", "r") as file:
        count = int(file.read().strip())
    updateCount()
    return "The number of times this bot has been used is " + str(count)

# Method that activates each time a message is sent on the server
@client.event
async def on_message(message):
    # Stops the bot from recognizing its own messages (nightmare)
    if message.author == client.user:
        return
    user_message = str(message.content)

    # if the word 'game' or 'gaming' is mentioned in a message, bot will reply with a gif and sentence
    # Change keywords to whatever you want
    if 'gaming' in user_message or 'game' in user_message or 'Game' in user_message or 'Gaming' in user_message:
        gifList = [
            'Insert tenor link for gifs here']

        responseList = ['Have the bot send a text message along with a gif'
            ]

        await message.channel.send(random.choice(gifList))#Select Random Gif
        await message.channel.send(random.choice(responseList))#Select Random Sentence
        updateCount()

    # Returns bot stats
    # Currently only counts the number of times the bot has been used
    if '!stats' in user_message:
        await message.channel.send(getCount())

    # Lists the bots current functionality
    if '!help' in user_message:
        await message.channel.send("This bot is able to play mp3's in a voice channel\n"
                                   "Enter '!play' + the file name you want\n"
                                   "Enter as many commands as you want in a line\n"
                                   "The bot can look for keywords in messages and then reply with an image or sentence\n"
                                   "Made by Angelo P aka Meatus")
        updateCount()

    # Plays a specified mp3 through a voice channel using ffmpeg
    if '!play' in user_message:
        ffmpegEx = "Insert File Path for ffmpegEx"
        sourceMP3 = "Insert Directory path for mp3 files"
        channel = message.author.voice.channel

        # mp3 file names minus the file type (.mp3)
        # add as many as you want
        soundList = [
            'filename without file type', 'whatever you want to invoke in chat']

        if channel is not None:
            vc = await channel.connect()
            print(f'the bot has joined the voice channel: {channel}')
            # Time for bot to pause before playing audio
            await asyncio.sleep(1.5)

            # plays a chain of sounds in order
            userArray = user_message.split(" ")
            for word in userArray:
                for sound in soundList:
                    if sound == word:
                        vc.play(discord.FFmpegPCMAudio(executable=ffmpegEx, source=sourceMP3 + sound + ".mp3"))
                        while vc.is_playing():
                            await asyncio.sleep(0.2)
            await vc.disconnect()
            updateCount()
        print(f'the bot has left the voice channel: {channel}')


client.run(TOKEN)
