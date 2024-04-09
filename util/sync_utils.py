from discord import app_commands, Client
from commands.stream_commands import StreamCommands
from commands.music_commands import MusicCommands
import logging

LOG = logging.getLogger(__name__)


class SyncUtils:
    @staticmethod
    def add_commands_to_tree(
        tree: app_commands.CommandTree, client: Client, override: bool = False
    ):
        tree.add_command(StreamCommands(tree, client), override=override)
        tree.add_command(MusicCommands(tree, client), override=override)
