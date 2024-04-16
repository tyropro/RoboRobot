from discord import Interaction, app_commands, Client
from discord.utils import get
from config import Config
from util.sync_utils import SyncUtils
import logging

LOG = logging.getLogger(__name__)

# MOD_ROLE = Config.CONFIG["Discord"]["Roles"]["Mod"]


@app_commands.guild_only()
class SyncCommands(app_commands.Group, name="sync"):
    def __init__(self, tree: app_commands.CommandTree, client: Client) -> None:
        super().__init__()
        self.tree = tree
        self.client = client

    @app_commands.command(name="sync")
    @app_commands.checks.has_role("pink")
    async def sync(self, interaction: Interaction) -> None:
        """Manually sync slash commands to guild"""
        LOG.info(f"[{interaction.user}] Syncing commands to guild {interaction.guild}")
        guild = interaction.guild
        self.tree.clear_commands(guild=guild)
        SyncUtils.add_commands_to_tree(self.tree, self.client, override=True)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        await interaction.response.send_message("Commands synced", ephemeral=True)

    @app_commands.command(name="guild")
    @app_commands.checks.has_role("pink")
    @app_commands.describe(guild="Guild to sync commands to")
    async def guild(self, interaction: Interaction, guild: str) -> None:
        """Manually sync slash commands to guild"""
        guild = self.client.get_guild(int(guild))
        LOG.info(f"[{interaction.user}] Syncing commands to guild {guild}")
        self.tree.clear_commands(guild=guild)
        SyncUtils.add_commands_to_tree(self.tree, self.client, override=True)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        await interaction.response.send_message("Commands synced", ephemeral=True)
