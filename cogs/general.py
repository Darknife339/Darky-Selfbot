import discord
from discord.ext import commands
import discord_self_embed
import random
import re
from cogs.config import Config
from cogs.utils import (
    send_message,
    send_error_message,
    generate_help_pages,
    get_command_full_name,
    fake_markdown,
)


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "Core commands\ngeneral"
        self.cfg = Config()

    @commands.command(
        name="help", description="Get help with a command", usage="[command]"
    )
    async def help(self, ctx, command: str = None):
        cfg = self.cfg

        if command is None:
            categories = []
            for cog_name, cog in self.bot.cogs.items():
                if cog_name.lower() != "general" and hasattr(cog, "description"):
                    desc = (
                        cog.description.split("\n")[0]
                        if "\n" in cog.description
                        else cog.description
                    )
                    categories.append(f"**{cog_name}** :: {desc}")

            categories.sort()
            desc_text = "\n".join(categories)

            await send_message(
                ctx,
                {
                    "title": cfg.theme.title,
                    "description": f"{desc_text}\n\nUse `.help [command]` for command info",
                    "codeblock_desc": desc_text,
                },
                extra_title=f"{len(self.bot.commands)} total commands",
            )
        else:
            cmd_obj = self.bot.get_command(command)
            if not cmd_obj:
                await send_error_message(ctx, f"Command **{command}** not found.")
                return

            info = {
                "name": cmd_obj.name,
                "description": cmd_obj.description or "No description",
                "usage": cmd_obj.usage or "None",
                "aliases": ", ".join(cmd_obj.aliases) if cmd_obj.aliases else "None",
            }
            max_key_length = max(len(key) for key in info)

            description_text = "\n".join(
                [f"**{key}:** {value}" for key, value in info.items()]
            )
            codeblock_text = "\n".join(
                [
                    f"{key}{' ' * (max_key_length - len(key))} :: {value}"
                    for key, value in info.items()
                ]
            )

            await send_message(
                ctx,
                {
                    "title": "Help",
                    "description": description_text,
                    "codeblock_desc": codeblock_text,
                },
            )

    @commands.command()
    async def ping(self, ctx):
        await send_message(
            ctx,
            {
                "title": "Pong!",
                "description": f"Latency: {round(self.bot.latency * 1000)}ms",
            },
        )


async def setup(bot):
    await bot.add_cog(General(bot))
