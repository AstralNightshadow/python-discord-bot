# Import necessary elements for Discord
import discord
from discord.ext import commands
# Import to be able to handle multiple things at once
import asyncio
# Import to read environment variable for token
import os

# Set the intents (permissions)
intents = discord.Intents.default()
intents.message_content = True  # Allow reading message content
intents.guilds = True  # Allow reading server(guild) data like audit logs

# Create the bot with intents
bot = commands.Bot(intents=intents)

# Runs when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')



###################
# On Message sent #
###################

# Logs every message sent in channels to the console
@bot.event
async def on_message(message):
    if message.author == bot.user:  # Ignores own messages
        return
    print(f'Message from {message.author} in #{message.channel}: \n{message.content}')
# NOTE: Maybe remove if bot is widely used.


######################
# On Message deleted #
######################

# Logs and reports deleted messages
@bot.event
async def on_message_delete(message):
    msg = f'Someone deleted the message from {message.author} in #{message.channel}: \n{message.content}'  # Default log message
    if message.guild:  # Check if the message was in server
        # Look for the user who deleted the message in the audit logs
        try:
            async for entry in message.guild.audit_logs(action=discord.AuditLogAction.message_delete, limit=1):
                if entry.target == message.author and entry.extra.channel == message.channel:  # Match the deleted message
                    msg = f'{entry.user} deleted the message from {message.author} in #{message.channel}: \n{message.content}'  # Update log message
                    break
        except:
            print(f"no audit log permissions in {message.guild}")
        # Find the "deleted-msg" channel in the server, if none are found don't send message
        channel = discord.utils.get(message.guild.channels, name='deleted-msg') or None
    else:
        channel = None

    if channel:
        await channel.send(msg)  # Send the log message to the appropriate channel
    print(msg)



########
# Ping #
########

# A slash command for to check ping
@bot.slash_command(description="Sends the bot's latency.")
async def ping(ctx): 
    await ctx.respond(f"Pong! Latency is {bot.latency * 1000:.2f} ms") 

# ctx is the context of the slash command
# ctx.respond makes the message a response to the slash command



############
# Reminder #
############

# A slash command to set reminders
@bot.slash_command(description="Sends you a reminder at the set time")
async def reminder(ctx, hours: int, minutes: int, message: str):
    """
    Set a reminder.
    :param hours: The amount of hours (eg. 5)
    :param minutes: The amount of minutes (eg. 35)
    :param message: The reminder message (eg. go to sleep)
    """

    # Check hours and minutes
    if hours < 0 or minutes < 0:
        await ctx.respond("Error: Hours and minutes must be non-negative values.")
        return
    elif minutes >= 60:
        await ctx.respond("Error: Minutes must be less than 60.")
        return
    if hours > 24:
        await ctx.respond("Error: Hours must be less than 24.")
        return
    if hours == 0 and minutes == 0:
        await ctx.respond("Error: Time must be greater than zero.")
        return

    # Check the message
    if not message.strip():
        await ctx.respond("Reminder message cannot be empty.")
        return
    if len(message) > 200:
        await ctx.respond("Reminder message is too long (max 200 characters).")
        return
    
    # Convert time into seconds
    delay = (minutes * 60) + (hours * 3600)

    # Give a confirmation message that the user set a reminder.
    if (hours > 0 & minutes > 0):
        await ctx.respond(f"Sucess! Reminder is due in {hours} hours and {minutes} minutes.")
    elif hours > 0:
        await ctx.respond(f"Sucess! Reminder is due in {hours} hours.")
    elif minutes > 0:
        await ctx.respond(f"Sucess! Reminder is due in {minutes} minutes")
    
    # Start the timer
    bot.loop.create_task(send_reminder(ctx, delay, message))

# Actually send the reminder
async def send_reminder(ctx, delay, message):
    await asyncio.sleep(delay)
    try:
        await ctx.author.send(f"Here is your scheduled reminder: \n{message}")
    except discord.Forbidden:
        await ctx.respond(f"{ctx.user.mention}, I couldn't send you a DM. Please make sure your DMs are open.")


# Start the bot
bot.run(os.environ['discord_bot_token'])
