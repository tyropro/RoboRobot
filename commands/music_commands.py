from discord import (
    app_commands,
    Interaction,
    Client,
    FFmpegPCMAudio,
    PCMVolumeTransformer,
    Embed,
    Color,
)
from datetime import datetime
import yt_dlp
import logging
import asyncio

LOG = logging.getLogger(__name__)

YTDL_FORMAT_OPTIONS = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

FFMPEG_OPTIONS = {
    "options": "-vn",
}

ytdl = yt_dlp.YoutubeDL(YTDL_FORMAT_OPTIONS)


class YTDLSource(PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream)
        )

        if "entries" in data:
            # take first item from a playlist
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)


@app_commands.guild_only()
class MusicCommands(app_commands.Group, name="music"):
    def __init__(self, tree: app_commands.CommandTree, client: Client) -> None:
        super().__init__()
        self.tree = tree
        self.client = client

    @app_commands.command(name="join")
    async def join(self, interaction: Interaction):
        """Joins a voice channel"""

        if interaction.guild.voice_client is not None:
            return await interaction.guild.voice_client.move_to(
                interaction.user.voice.channel
            )

        await interaction.user.voice.channel.connect()

    @app_commands.command(name="file")
    @app_commands.describe(query="Search query")
    async def play_file(self, interaction: Interaction, query: str):
        """Play a song from local filesystem"""

        await self.ensure_voice(interaction)

        await interaction.response.send_message(f"Now playing: {query}")

        source = PCMVolumeTransformer(FFmpegPCMAudio(query))
        interaction.guild.voice_client.play(
            source, after=lambda e: print(f"Player error: {e}") if e else None
        )

    @app_commands.command(name="play")
    @app_commands.describe(url="URL of the song")
    async def play(self, interaction: Interaction, url: str):
        """Plays from a url (almost anything youtube_dl supports)"""

        await self.ensure_voice(interaction)

        embed = Embed(
            title="Tyro's Super Epic Music Bot",
            description="Searching for the song...",
            color=Color.blurple(),
        )
        embed.add_field(name="URL: ", value=url, inline=False)

        await interaction.response.send_message(embed=embed)

        async with interaction.channel.typing():
            player = await YTDLSource.from_url(url, loop=self.client.loop, stream=False)

            embed = Embed(
                title="Tyro's Super Epic Music Bot",
                description=f"Now playing",
                color=Color.purple(),
            )
            embed.add_field(name="Track: ", value=player.title, inline=False)

            await interaction.edit_original_response(embed=embed)

            interaction.guild.voice_client.play(
                player, after=lambda e: print(f"Player error: {e}") if e else None
            )

    @app_commands.command(name="volume")
    @app_commands.describe(volume="Volume in %")
    async def volume(self, interaction: Interaction, volume: int):
        """Changes the player's volume"""

        if interaction.guild.voice_client is None:
            await interaction.response.send_message("Not connected to a voice channel.")
            return

        interaction.guild.voice_client.source.volume = volume / 100
        await interaction.response.send_message(f"Changed volume to {volume}%")

    @app_commands.command(name="stop")
    async def stop(self, interaction: Interaction):
        """Stops and disconnects the bot from voice"""

        if interaction.guild.voice_client is None:
            await interaction.response.send_message("Not connected to a voice channel.")
            return

        interaction.guild.voice_client.stop()
        await interaction.guild.voice_client.disconnect()

        await interaction.response.send_message("Bye bye! (´・ω・｀)")

    async def ensure_voice(self, interaction: Interaction):
        if interaction.guild.voice_client is None:
            if interaction.user.voice:
                await interaction.user.voice.channel.connect()
            else:
                await interaction.response.send_message(
                    "You are not connected to a voice channel."
                )
                raise app_commands.CommandError(
                    "Author not connected to a voice channel."
                )
        elif interaction.guild.voice_client.is_playing():
            interaction.guild.voice_client.stop()

    async def get_yt(self, interaction: Interaction, url: str):
        player = await YTDLSource.from_url(url, loop=self.client.loop)
        return player
