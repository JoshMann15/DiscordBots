import discord
from discord.ext import tasks, commands
from discord.utils import get
from dotenv import load_dotenv
import asyncio
import os
from pychatgpt import ChatGPT
import time

load_dotenv(".env")
SessionID = os.getenv("SessionID")

intents=discord.Intents.all()

prefix = '$'
bot = commands.Bot(command_prefix=prefix, intents=intents)

bot.remove_command('help')

def get_api():
    api = None
    try:
      api = ChatGPT(SessionID)
    except Exception as e:
      print(f'get_api_error:', e)
      api = None
    return api
    
def get_response_from_chatgpt(api, text):
    if api is None:
        return "Openai said: I'm too tired. Let me lie down for a few days. If you like, you can visit my home."
    try:
      resp = api.send_message(text)
      response = resp['message']
    except:
      response = "Openai said: I'm so tired. Let me lie down for a few days. If you like, you can visit my home."
    return response

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
    

@bot.command()
async def query(ctx, *args):
    line = ''
    for i in range(0, len(args)):
        line += str(args[i]) + " "
    line=line[:-1]
    await ctx.send(get_response_from_chatgpt(get_api(), line))
    
bot.run(TOKEN)
