# imports necessary elements for discord
import discord
from discord.ext import commands

#creating the discord client
class MyClient(discord.Client):

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='$', intents=intents)

    #write message as soon as it is ready
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    #print every message as soon as they are written
    async def on_message(self, message):
        print(f'Message from {message.author} in #{message.channel}: {message.content}')

    #print and write a message to a specific channel or the channel it was sent in
    async def on_message_delete(self, message):
        msg = f'{message.author} has deleted the message: {message.content}'
        try:
            channel = discord.utils.get(client.get_all_channels(), name='deleted-msg')
            channel_id = channel.id
        except:
            channel_id = message.channel.id
        
        channel = client.get_channel(channel_id)
        await channel.send(msg)
        print (msg)

    # this decorator makes a slash command
    @bot.hybrid_command(description="Sends the bot's latency.") 
    # a slash command will be created with the name "ping"
    async def ping(ctx): 
        await ctx.respond(f"Pong! Latency is {bot.latency}")


    bot.add_command(ping)

#set the intents(rights it has)
intents = discord.Intents.default()
intents.message_content = True

#start the client with the token
client = MyClient(intents=intents)
client.run('MTMyNjg4OTgxMTU0NTY5MDEzMg.GnQb_j.FkWAoHfUPePLgWK6rAF3mgw3o4hGydw861mYJM')
