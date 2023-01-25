import discord
from discord.ext import tasks, commands
from discord.utils import get
from dotenv import load_dotenv
import asyncio
import os
import openai

#For a more secure, we loaded the .env file and assign the token value to a variable 
load_dotenv(".env")
TOKEN = os.getenv("TOKEN")
api_tokens = 0.27

openai.api_key = os.getenv('api_key')
#Intents are permissions for the bot that are enabled based on the features necessary to run the bot.
intents=discord.Intents.all()

#Comman prefix is setup here, this is what you have to type to issue a command to the bot
prefix = '$'
bot = commands.Bot(command_prefix=prefix, intents=intents)

#Removed the help command to create a custom help guide
bot.remove_command('help')

#------------------------------------------------Events------------------------------------------------------#

#Basic Discord Bot Commands: Chat with your bot!
@bot.command(name='hi')
async def msg(ctx):
    if ctx.author == bot.user:
        return
    else:
        await ctx.send("Hello there!")

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
async def help(message):
    embed = discord.Embed(title="OpenAI Bot", description="A discord bot built with python used to interactive with the Open AI API")
    embed.add_field(name="Credits", value="Josh Nahamkes\nSanjin Dedic\nStable Diffusion")

    await message.channel.send(embed=embed)
    
@bot.command()
async def create_image(message, *args):
    try:
        
        print("Command Started!");
        global api_tokens
        api_tokens += 0.018
        line = ''
        for i in range(0, len(args)):
            line += str(args[i]) + " "
        line=line[:-1]
    
        print("Embed Started!");
        
        response = openai.Image.create(
            prompt=line,
            n=1,
            size="512x512"
        )
        
        print("Response Created!");
        image_url = response['data'][0]['url']
        embed = discord.Embed(title="Image with prompt: "+line, url=image_url, description="An image of: "+line)
        embed.set_image(url=image_url)
        print("Img Embed Loaded: "+image_url);
        
        #print(line)
        
        await message.channel.send(embed=embed)
        #await ctx.send(image_url + "\nIMAGES USED: " + str((api_tokens/18)*100) + "%")
    except Exception as e:
        print(e)
    



    

@bot.command()
#Checks whether the user has the correct permissions when this command is issued
@commands.has_permissions(manage_messages=True)
async def clear(context, amount=5):
    await context.channel.purge(limit=amount+1)

print("Command Started!");
#embed = discord.Embed(title="Image with prompt: "+message, description="A discord bot built with python used to interactive with the stable diffusion API")

'''
print("Embed Started!");
response = openai.Image.create(
  prompt='message',
  n=1,
  size="1024x1024"
)
print("Response Created!");
image_url = response['data'][0]['url']
#embed.setImage(image_url)
print("Img Embed Loaded: "+image_url);
'''
#Run the bot
bot.run(TOKEN)
