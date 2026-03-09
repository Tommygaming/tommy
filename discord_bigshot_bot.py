#!/usr/bin/env python3
"""Discord bot that posts "now your chance to be a [[bigshot]]." every 5 minutes."""

import os

import discord
from discord.ext import commands, tasks

MESSAGE = "now your chance to be a [[bigshot]]."

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

if not TOKEN:
    raise RuntimeError("Missing DISCORD_BOT_TOKEN environment variable")

if not CHANNEL_ID:
    raise RuntimeError("Missing DISCORD_CHANNEL_ID environment variable")

try:
    CHANNEL_ID_INT = int(CHANNEL_ID)
except ValueError as exc:
    raise RuntimeError("DISCORD_CHANNEL_ID must be an integer") from exc

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@tasks.loop(minutes=5)
async def post_bigshot_message() -> None:
    channel = bot.get_channel(CHANNEL_ID_INT)

    if channel is None:
        channel = await bot.fetch_channel(CHANNEL_ID_INT)

    await channel.send(MESSAGE)


@bot.event
async def on_ready() -> None:
    if not post_bigshot_message.is_running():
        post_bigshot_message.start()

    print(f"Logged in as {bot.user} and posting every 5 minutes.")


if __name__ == "__main__":
    bot.run(TOKEN)
