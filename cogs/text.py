import discord
from discord.ext import commands
import asyncio
import random
import art
from cogs.config import Config
from cogs.utils import send_message, send_error_message, generate_help_pages


class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "Text manipulation commands\ntext"
        self.cfg = Config()

    @commands.command(name="text", description="Text commands", usage="", aliases=["txt"])
    async def text(self, ctx, selected_page: int = 1):
        cfg = self.cfg
        pages = generate_help_pages(self.bot, "Text")

        await send_message(
            ctx,
            {
                "title": f"Text Commands",
                "description": pages[cfg.get("message_settings")["style"]][
                    selected_page - 1
                    if selected_page - 1
                    < len(pages[cfg.get("message_settings")["style"]])
                    else 0
                ],
                "footer": f"Page {selected_page}/{len(pages[cfg.get('message_settings')['style']])}",
                "codeblock_desc": pages["codeblock"][
                    selected_page - 1
                    if selected_page - 1 < len(pages["codeblock"])
                    else 0
                ],
            },
            extra_title=f"Page {selected_page}/{len(pages['codeblock'])}",
        )

    @commands.command(name="shrug", description="Shrug your arms", usage="")
    async def shrug(self, ctx):
        await ctx.send("¯\_(ツ)_/¯")
        await ctx.message.delete()

    @commands.command(name="tableflip", description="Flip the table", usage="")
    async def tableflip(self, ctx):
        await ctx.send("(╯°□°）╯︵ ┻━┻")
        await ctx.message.delete()

    @commands.command(name="unflip", description="Put the table back", usage="")
    async def unflip(self, ctx):
        await ctx.send("┬─┬ ノ( ゜-゜ノ)")
        await ctx.message.delete()

    @commands.command(
        name="lmgtfy",
        description="Let me Google that for you",
        usage="[search]",
        aliases=["letmegooglethatforyou"],
    )
    async def lmgtfy(self, ctx, *, search):
        await ctx.send(f"https://lmgtfy.app/?q={search.replace(' ', '+')}")
        await ctx.message.delete()

    @commands.command(
        name="blank", description="Send a blank message", usage="", aliases=["empty"]
    )
    async def blank(self, ctx):
        await ctx.send("** **")
        await ctx.message.delete()

    @commands.command(
        name="fakepurge", description="Flood chat with blank messages", usage=""
    )
    async def fakepurge(self, ctx):
        msgs = ["** **\n" * 5 for i in range(10)]
        for msg in msgs:
            await ctx.send(msg)
            await asyncio.sleep(0.5)
        await ctx.message.delete()

    @commands.command(
        name="ascii", description="Create ascii text art from text", usage="[text]"
    )
    async def ascii_(self, ctx, *, text: str):
        await ctx.send(f"```\n{art.text2art(text)}\n```")
        await ctx.message.delete()

    @commands.command(
        name="aesthetic", description="Make your text aesthetic", usage="[text]"
    )
    async def aesthetic(self, ctx, *, text: str):
        result = " ".join(list(text))
        await ctx.send(result)
        await ctx.message.delete()

    @commands.command(
        name="chatbypass",
        description="Bypass chat filters",
        usage="[text]",
        aliases=["bypass"],
    )
    async def chatbypass(self, ctx, *, text: str):
        result = " ".join(list(text))
        await ctx.send(result)
        await ctx.message.delete()

    @commands.command(
        name="regional", description="Make your text out of emojis", usage="[text]"
    )
    async def regional(self, ctx, *, text: str):
        regional_emojis = {
            "a": "🇦",
            "b": "🇧",
            "c": "🇨",
            "d": "🇩",
            "e": "🇪",
            "f": "🇫",
            "g": "🇬",
            "h": "🇭",
            "i": "🇮",
            "j": "🇯",
            "k": "🇰",
            "l": "🇱",
            "m": "🇲",
            "n": "🇳",
            "o": "🇴",
            "p": "🇵",
            "q": "🇶",
            "r": "🇷",
            "s": "🇸",
            "t": "🇹",
            "u": "🇺",
            "v": "🇻",
            "w": "🇼",
            "x": "🇽",
            "y": "🇾",
            "z": "🇿",
        }
        result = "".join([regional_emojis.get(char.lower(), char) for char in text])
        await ctx.send(result)
        await ctx.message.delete()

    @commands.command(
        name="randomcase", description="Make your text random case", usage="[text]"
    )
    async def randomcase(self, ctx, *, text: str):
        result = "".join([random.choice([char.upper(), char.lower()]) for char in text])
        await ctx.send(result)
        await ctx.message.delete()

    @commands.command(
        name="cembed",
        description="Create a custom embed",
        usage="[title] [description] [footer] [colour] [image]",
        aliases=["customembed"],
    )
    async def cembed(
        self,
        ctx,
        title: str,
        description: str,
        footer: str = "",
        colour: str = "8B5CF6",
        image: str = "",
    ):
        await send_message(
            ctx,
            {
                "title": title,
                "description": description,
                "footer": footer,
                "colour": "#" + colour.lstrip("#"),
                "thumbnail": image,
            },
            extra_title=footer,
        )
        await ctx.message.delete()

    @commands.command(
        name="codeblock",
        description="Create a codeblock",
        usage="[language] [code]",
        aliases=["block"],
    )
    async def codeblock(self, ctx, language: str, *, code: str):
        await ctx.send(f"```{language}\n{code}\n```")
        await ctx.message.delete()

    @commands.command(
        name="json",
        description="Create a json codeblock",
        usage="[json]",
        aliases=["jblock"],
    )
    async def json(self, ctx, *, json: str):
        await self.codeblock(ctx, "json", code=json)

    @commands.command(
        name="python",
        description="Create a python codeblock",
        usage="[python]",
        aliases=["pyblock"],
    )
    async def python(self, ctx, *, python: str):
        await self.codeblock(ctx, "python", code=python)

    @commands.command(name="reverse", description="Reverse your text", usage="[text]")
    async def reverse(self, ctx, *, text: str):
        await ctx.send(text[::-1])
        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(Text(bot))
