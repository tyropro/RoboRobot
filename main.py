from discord import (
  app_commands,
  Client,
  Intents
)
import asyncio
import discord

from config import Config
from commands.sync_commands import SyncCommands
from util.sync_utils import SyncUtils

import logging

discord.utils.setup_logging(level=logging.INFO, root=True)

LOG = logging.getLogger(__name__)

GUILD_ID = Config.CONFIG["Discord"]["GuildID"]
TOKEN = Config.CONFIG["Secrets"]["Discord"]["Token"]


class Bot(Client):
  def __init__(self):
    intents = Intents.default()
    intents.members = True
    intents.message_content = True
    intents.guilds = True
  
    super().__init__(intents=intents)

  async def on_ready(self):
    logging.info(f"Logged in as {self.user} (ID: {self.user.id})")

client = Bot()
tree = app_commands.CommandTree(client)

@client.event
async def on_guild_join(guild):
  tree.clear_commands(guild=guild)
  tree.copy_global_to(guild=guild)
  await tree.sync(guild=guild)
  
  
async def main():
  async with client:
    tree.add_command(SyncCommands(tree, client))
    SyncUtils.add_commands_to_tree(tree, client)
    await client.start(TOKEN)   

if __name__ == "__main__":
  asyncio.run(main())