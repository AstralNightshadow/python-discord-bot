# This example requires the 'message_content' intent.

import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author} in #{message.channel}: {message.content}')

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


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('MTMyNjg4OTgxMTU0NTY5MDEzMg.GnQb_j.FkWAoHfUPePLgWK6rAF3mgw3o4hGydw861mYJM')
