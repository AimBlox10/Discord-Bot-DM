import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True  # Enable member intents for the on_member_join event
intents.message_content = True  # Enable message content intent

bot = commands.Bot(command_prefix="!", intents=intents)

SPECIFIED_CHANNEL_ID = 1242492829352198234  # Replace this with your specified channel ID

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def dm(ctx, username: discord.User, *, message: str):
    if ctx.channel.id != SPECIFIED_CHANNEL_ID:
        await ctx.send("This command can only be used in the specified channel.")
        return

    try:
        # Send a DM to the target user including a mention of the command issuer
        await username.send(f"{ctx.author.mention} says: {message}")
        # Reply in the channel confirming the message was sent
        await ctx.reply(f"DM succesfully sent to {username.name}")
    except discord.errors.HTTPException as e:
        await ctx.reply(f"Failed to send message: {e}")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
