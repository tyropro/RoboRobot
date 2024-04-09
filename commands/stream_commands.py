from discord import app_commands, Interaction, Client
from config import Config
import requests
import logging

LOG = logging.getLogger(__name__)


@app_commands.guild_only()
class StreamCommands(app_commands.Group, name="stream"):
    def __init__(self, tree: app_commands.CommandTree, client: Client) -> None:
        super().__init__()
        self.tree = tree
        self.client = client

    @app_commands.command(name="title")
    @app_commands.checks.has_role("pink")
    @app_commands.describe(title="Title of the stream")
    async def title(self, interaction: Interaction, title: str):
        """Change the stream title"""
        # Makes a PATCH request to the Twitch Helix API to change
        # the title of the stream to the provided title from the user
        
        LOG.info(f"[{interaction.user}] Title: {title}")
        
        headers = \
            {
                "Authorization": "Bearer " + Config.CONFIG["Secrets"]["Twitch"]["OAuth"],
                "Client-ID": Config.CONFIG["Twitch"]["ClientID"],
                "Content-Type": "application/json",
            }
        params = \
            {
                "title": title,
                "broadcaster_id": Config.CONFIG["Twitch"]["ChannelID"]
            }
        
        try:
            requests.patch("https://api.twitch.tv/helix/channels", headers=headers, params=params).raise_for_status()
        except requests.exceptions.HTTPError:
            LOG.error(f"[{interaction.user}] Error changing title")
            await interaction.response.send_message(f"Error", ephemeral=True)
            return
        
        await interaction.response.send_message(
            f"Title changed to: {title}", ephemeral=True
        )
    
    @app_commands.command(name="game")
    @app_commands.checks.has_role("pink")
    @app_commands.describe(game="Game the streamer is playing")
    async def game(self, interaction: Interaction, game: str):
        """Change the currently played game on stream"""
        # Makes a GET request to the Twitch Helix API to get the game ID
        # of the provided game name. Then makes a PATCH request to the Twitch
        # Helix API to change the game of the stream to the provided game from the user
        
        LOG.info(f"[{interaction.user}] Game: {game}")
        
        headers = \
            {
                "Authorization": "Bearer " + Config.CONFIG["Secrets"]["Twitch"]["OAuth"],
                "Client-ID": Config.CONFIG["Twitch"]["ClientID"],
                "Content-Type": "application/json",
            }
        params = \
            {
                "name": game
            }
        
        r = requests.get("https://api.twitch.tv/helix/games", headers=headers, params=params).json()
        
        if len(r["data"]) == 0:
            LOG.error(f"[{interaction.user}] Error fetching game")
            await interaction.response.send_message(f"Game not found", ephemeral=True)
            return
        
        game_id = r["data"][0]["id"]
        
        params = \
            {
                "game_id": game_id,
                "broadcaster_id": Config.CONFIG["Twitch"]["ChannelID"]
            }
        
        try:
            requests.patch("https://api.twitch.tv/helix/channels", headers=headers, params=params).raise_for_status()
        except requests.exceptions.HTTPError:
            LOG.error(f"[{interaction.user}] Error changing game")
            await interaction.response.send_message(f"Error", ephemeral=True)
            return
        
        await interaction.response.send_message(f"Game set to: {r["data"][0]["name"]}", ephemeral=True)