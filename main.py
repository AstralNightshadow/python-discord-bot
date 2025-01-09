# This example requires the 'message_content' intent.

import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author} in #{message.channel}: {message.content}')

    async def on_message_delete(self, message):
        print(f'{message.author} has deleted the message: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('MTMyNjg4OTgxMTU0NTY5MDEzMg.GnQb_j.FkWAoHfUPePLgWK6rAF3mgw3o4hGydw861mYJM')
