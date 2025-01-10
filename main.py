# Import necessary elements for Discord
import discord
from discord.ext import commands

# Set the intents (permissions)
intents = discord.Intents.default()
intents.message_content = True  # Allow reading message content
intents.guilds = True  # Access guild data like audit logs

# Create the bot with intents
bot = commands.Bot(intents=intents)

# Runs when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

# Logs every message sent in a channel
@bot.event
async def on_message(message):
    if message.author == bot.user:  # Avoid self-replies
        return
    print(f'Message from {message.author} in #{message.channel}: {message.content}')

# Logs and reports deleted messages
@bot.event
async def on_message_delete(message):
    msg = f'Someone deleted the message from {message.author} in #{message.channel}: {message.content}'  # Default log message
    if message.guild:  # Check if the message was in a server
        # Look for the user who deleted the message in the audit logs
        try:
            async for entry in message.guild.audit_logs(action=discord.AuditLogAction.message_delete, limit=1):
                if entry.target == message.author and entry.extra.channel == message.channel:  # Match the deleted message
                    msg = f'{entry.user} deleted the message from {message.author} in #{message.channel}: {message.content}'  # Update log message
                    break
        except:
            print(f"no audit log permissions in {message.guild}")
        # Find the "deleted-msg" channel in the server otherwise default to the
        channel = discord.utils.get(message.guild.channels, name='deleted-msg') or None
    else:
        channel = None

    if channel:
        await channel.send(msg)  # Send the log message to the appropriate channel
    print(msg)

# A slash command to display bot latency
@bot.slash_command(description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {bot.latency * 1000:.2f} ms")

# Start the bot
bot.run('MTMyNjg4OTgxMTU0NTY5MDEzMg.GnQb_j.FkWAoHfUPePLgWK6rAF3mgw3o4hGydw861mYJM')
