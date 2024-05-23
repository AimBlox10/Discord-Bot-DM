import discord
from discord.ext import commands
import os
from keep_alive import keep_alive # Import the keep_alive function

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True

# Specify the role IDs that are allowed to use the commands
allowed_roles = [1241381829966172251, 1241382114457419907, 1241382218593603768, 1242075256861102163]

# Function to check if user has allowed roles
def has_allowed_role(ctx):
    return any(role.id in allowed_roles for role in ctx.author.roles)

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Event to confirm bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Command to kick a user
@bot.command()
@commands.check(has_allowed_role)
async def kick(ctx, member: discord.Member, *, reason='No reason provided'):
    await member.send(f'You have been kicked from {ctx.guild.name} for the following reason: {reason}')
    await member.kick(reason=reason)
    await ctx.reply(f'{member.mention} has been kicked for reason : {reason}')
    # Save kick history to file
    with open('history.txt', 'a') as file:
        file.write(f'KICK: {member.id} - {member.name} - {reason}\n')

# Command to ban a user
@bot.command()
@commands.check(has_allowed_role)
async def ban(ctx, member: discord.Member, *, reason='No reason provided'):
    await member.send(f'You have been banned from {ctx.guild.name} for the following reason: {reason}')
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned for reason : {reason}')
    # Save ban history to file
    with open('history.txt', 'a') as file:
        file.write(f'BAN: {member.id} - {member.name} - {reason}\n')

# Command to show kick and ban history
@bot.command()
@commands.check(has_allowed_role)
async def history(ctx):
    try:
        with open('history.txt', 'r') as file:
            history = file.read()
            await ctx.reply('**Kick and Ban History:**\n```' + history + '```')
    except FileNotFoundError:
        await ctx.reply("No history found.")

# Function to send direct messages
@bot.command()
async def dm(ctx, username: discord.User, *, message: str):
    SPECIFIED_CHANNEL_ID = 1243299332804055280 # Replace this with your specified channel ID
    if ctx.channel.id != SPECIFIED_CHANNEL_ID:
        await ctx.reply("This command can only be used in the specified channel.")
        return

    try:
        # Send a DM to the target user including a mention of the command issuer
        await username.send(f"{ctx.author.mention} says: {message}")
        # Reply in the channel confirming the message was sent
        await ctx.reply(f"DM successfully sent to {username.name}")
    except discord.errors.HTTPException as e:
        await ctx.reply(f"Failed to send message: {e}")

# Keep the bot alive with Flask
keep_alive()

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
