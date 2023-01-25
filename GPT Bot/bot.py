import discord
from discord.ext import tasks, commands
from discord.utils import get
from dotenv import load_dotenv
import asyncio
import os
from pychatgpt import ChatGPT
import time


#For a more secure, we loaded the .env file and assign the token value to a variable 
load_dotenv(".env")
SessionID = os.getenv("SessionID")

#Intents are permissions for the bot that are enabled based on the features necessary to run the bot.
intents=discord.Intents.all()

#Comman prefix is setup here, this is what you have to type to issue a command to the bot
prefix = '$'
bot = commands.Bot(command_prefix=prefix, intents=intents)

#Removed the help command to create a custom help guide
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

#-----------------------------------------Moderation---------------------------------------------------------------#

@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await context.send("Oh no! Looks like you have missed out an argument for this command.")
    if isinstance(error, commands.MissingPermissions):
        await context.send("Oh no! Looks like you Dont have the permissions for this command.")
    if isinstance(error, commands.MissingRole):
        await context.send("Oh no! Looks like you Dont have the roles for this command.")
    #bot errors
    if isinstance(error, commands.BotMissingPermissions):
        await context.send("Oh no! Looks like I Dont have the permissions for this command.")
    if isinstance(error, commands.BotMissingRole):
        await context.send("Oh no! Looks like I Dont have the roles for this command.")
    

#|------------------COMMANDS------------------|   

@bot.command()
async def query(ctx, *args):
    line = ''
    for i in range(0, len(args)):
        line += str(args[i]) + " "
    line=line[:-1]
    await ctx.send(get_response_from_chatgpt(get_api(), line))
    

#Run the bot
bot.run(TOKEN)
