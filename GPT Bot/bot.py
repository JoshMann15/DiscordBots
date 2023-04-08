import discord
from discord.ext import tasks, commands
from discord.utils import get
from dotenv import load_dotenv
import asyncio
import os
from pychatgpt import ChatGPT
import time

# get chat gpt api token from hidden file
load_dotenv(".env")
SessionID = os.getenv("SessionID")

intents=discord.Intents.all()

# set discord bot prefix
prefix = '$'
bot = commands.Bot(command_prefix=prefix, intents=intents)

bot.remove_command('help')

# Initialize ChatGPT api
def get_api():
    api = None
    # trys to initialize however does not throw error if unsuccessful instead we print errors for debugging
    try:
      api = ChatGPT(SessionID)
    except Exception as e:
      print(f'get_api_error:', e)
      api = None
    return api

# function to get a response from chatgpt api, with 2 args
def get_response_from_chatgpt(api, text):
    # if api did not initialize properly
    if api is None:
        return "Openai said: I'm too tired. Let me lie down for a few days. If you like, you can visit my home."
    try:
      # tries to get response from chatgpt api and format it
      resp = api.send_message(text)
      response = resp['message']
    except:
       # if api does not return a response or response is invalid
      response = "Openai said: I'm so tired. Let me lie down for a few days. If you like, you can visit my home."
    return response

# handles errors
@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await context.send("Oh no! Looks like you have missed out an argument for this command.")
    if isinstance(error, commands.MissingPermissions):
        await context.send("Oh no! Looks like you Dont have the permissions for this command.")
    if isinstance(error, commands.MissingRole):
        await context.send("Oh no! Looks like you Dont have the roles for this command.")
    
    if isinstance(error, commands.BotMissingPermissions):
        await context.send("Oh no! Looks like I Dont have the permissions for this command.")
    if isinstance(error, commands.BotMissingRole):
        await context.send("Oh no! Looks like I Dont have the roles for this command.")
    

# actual discord command to prompt chatgpt
@bot.command()
async def query(ctx, *args):
    # format prompt
    line = ''
    for i in range(0, len(args)):
        line += str(args[i]) + " "
    line=line[:-1]
    # send prompt then reutrn in discord channel
    await ctx.send(get_response_from_chatgpt(get_api(), line))
    
bot.run(TOKEN)
