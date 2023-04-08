import discord
from discord.ext import tasks, commands
from discord.utils import get
from dotenv import load_dotenv
import asyncio
import os
import openai

# Loads my discord bot token
load_dotenv(".env")
TOKEN = os.getenv("TOKEN")
api_tokens = 0.27

openai.api_key = os.getenv('api_key')

intents=discord.Intents.all()

# Sets bot prefixs
prefix = '$'
bot = commands.Bot(command_prefix=prefix, intents=intents)


bot.remove_command('help')

# Use '@' Decorator for command with argument name='hi'
@bot.command(name='hi')
async def msg(ctx):
    if ctx.author == bot.user:
        # Check if the command was sent by a bot
        return
    else:
        # send message in channel
        await ctx.send("Hello there!")

# resolves errors
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
async def help(message):
    # creates a variable of type discord.Embed 
    embed = discord.Embed(title="OpenAI Bot", description="A discord bot built with python used to interactive with the Open AI API")
    embed.add_field(name="Credits", value="Josh Nahamkes\nSanjin Dedic\nStable Diffusion")
    
    # sends Embed
    await message.channel.send(embed=embed)
    
# uses argument '*args' to get all words written after command
@bot.command()
async def create_image(message, *args):
    try:
        
        print("Command Started!");
        
        # format args into ai prompt
        global api_tokens
        api_tokens += 0.018
        line = ''
        for i in range(0, len(args)):
            line += str(args[i]) + " "
        line=line[:-1]
    
        print("Embed Started!");
        
        # Generates ai image from prompt with size 512x512
        response = openai.Image.create(
            prompt=line,
            n=1,
            size="512x512"
        )
        
        print("Response Created!");
        # format response
        image_url = response['data'][0]['url']
        embed = discord.Embed(title="Image with prompt: "+line, url=image_url, description="An image of: "+line)
        embed.set_image(url=image_url)
        print("Img Embed Loaded: "+image_url);
        
        
        #send embed of image
        await message.channel.send(embed=embed)
        
    except Exception as e:
        #log exception for debug
        print(e)
    

@bot.command()

@commands.has_permissions(manage_messages=True)
async def clear(context, amount=5):
    await context.channel.purge(limit=amount+1)

print("Command Started!");


'''
print("Embed Started!");
response = openai.Image.create(
  prompt='message',
  n=1,
  size="1024x1024"
)
print("Response Created!");
image_url = response['data'][0]['url']

print("Img Embed Loaded: "+image_url);
'''

bot.run(TOKEN)
