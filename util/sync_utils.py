from discord import app_commands, Client
from bot.commands.stream_commands import StreamCommands
import logging

LOG = logging.getLogger(__name__)


class SyncUtils:
    @staticmethod
    def add_commands_to_tree(
        tree: app_commands.CommandTree, client: Client, override: bool = False
    ):
        # tree.add_command(MemeCommands(tree, client), override=override)
        # tree.add_command(ModCommands(tree, client), override=override)
        # tree.add_command(ViewerCommands(tree, client), override=override)
        # tree.add_command(ManagerCommands(tree, client), override=override)
        # tree.add_command(ReactionCommands(tree, client), override=override)
        # tree.add_command(VodCommands(tree, client), override=override)
        # tree.add_command(TemproleCommands(tree, client), override=override)
        # tree.add_command(PointHistoryCommands(tree, client), override=override)
        # tree.add_command(ConnectFourCommands(tree, client), override=override)
        # tree.add_command(T3Commands(tree, client), override=override)
        # overlay_commands = OverlayCommands(tree, client)
        # LOG.info("---------------------------------------------")
        # for command in overlay_commands.walk_commands():
        #     LOG.info(f"overlay_command: {command.name}")
        # attr = getattr(overlay_commands, "test_command", None)
        # LOG.info(f"{attr=}")
        # tree.add_command(overlay_commands, override=override)
        
        tree.add_command(StreamCommands(tree, client), override=override)