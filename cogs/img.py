import discord
from discord.ext import commands
import requests
from cogs.config import Config
from cogs.utils import send_message, send_error_message, generate_help_pages


class Img(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "Image related commands\nimg"
        self.cfg = Config()

    @commands.command(
        name="img", description="Image commands", aliases=["image"], usage=""
    )
    async def img(self, ctx, selected_page: int = 1):
        cfg = self.cfg
        pages = generate_help_pages(self.bot, "Img")

        await send_message(
            ctx,
            {
                "title": f"Image Commands",
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

    @commands.command(
        name="cat",
        description="Get a random cat picture",
        aliases=["catpic", "gato"],
        usage="",
    )
    async def cat(self, ctx):
        resp = requests.get("https://api.alexflipnote.dev/cats")
        if resp.status_code == 200:
            image = resp.json()["file"]
            await ctx.send(image)
            await ctx.message.delete()
        else:
            await send_error_message(ctx, "Failed to fetch cat image")

    @commands.command(
        name="dog",
        description="Get a random dog picture",
        aliases=["dogpic", "doggo"],
        usage="",
    )
    async def dog(self, ctx):
        resp = requests.get("https://api.alexflipnote.dev/dogs")
        if resp.status_code == 200:
            image = resp.json()["file"]
            await ctx.send(image)
            await ctx.message.delete()
        else:
            await send_error_message(ctx, "Failed to fetch dog image")

    @commands.command(
        name="bird",
        description="Get a random bird picture",
        aliases=["birb", "birdpic"],
        usage="",
    )
    async def bird(self, ctx):
        resp = requests.get("https://api.alexflipnote.dev/birb")
        if resp.status_code == 200:
            image = resp.json()["file"]
            await ctx.send(image)
            await ctx.message.delete()
        else:
            await send_error_message(ctx, "Failed to fetch bird image")

    @commands.command(
        name="fox", description="Get a random fox picture", aliases=["foxpic"], usage=""
    )
    async def fox(self, ctx):
        resp = requests.get("https://randomfox.ca/floof/")
        if resp.status_code == 200:
            image = resp.json()["image"]
            await ctx.send(image)
            await ctx.message.delete()
        else:
            await send_error_message(ctx, "Failed to fetch fox image")

    @commands.command(
        name="achievement",
        description="Make a custom Minecraft achievement",
        usage="[icon] [text]",
        aliases=["mcachievement"],
    )
    async def achievement(self, ctx, icon: str = "1", *, text: str = None):
        if not text:
            await send_error_message(ctx, "Please provide text for the achievement")
            return

        base_url = "https://api.alexflipnote.dev/achievement"
        resp = requests.get(f"{base_url}?text={text.replace(' ', '+')}&icon={icon}")

        if resp.status_code == 200:
            with open("achievement.png", "wb") as f:
                f.write(resp.content)
            await ctx.send(file=discord.File("achievement.png"))
            import os

            os.remove("achievement.png")
            await ctx.message.delete()
        else:
            await send_error_message(ctx, "Failed to generate achievement")

    @commands.command(
        name="discordmessage",
        description="Create a fake Discord message",
        usage="[user] [message]",
        aliases=["fakediscordmessage"],
    )
    async def discordmessage(
        self, ctx, user: discord.User = None, *, message: str = None
    ):
        if not user:
            await send_error_message(ctx, "Please specify a user")
            return

        if not message:
            await send_error_message(ctx, "Please specify a message")
            return

        avatar_url = user.display_avatar.replace(size=1024).url
        username = user.display_name
        api_url = f"https://benny.fun/api/discordmessage?avatar_url={avatar_url}&username={username}&text={message}"
        resp = requests.get(api_url)

        if resp.status_code == 200:
            with open("discordmsg.png", "wb") as f:
                f.write(resp.content)
            await ctx.send(file=discord.File("discordmsg.png"))
            import os

            os.remove("discordmsg.png")
            await ctx.message.delete()
        else:
            await send_error_message(ctx, "Failed to generate message")


async def setup(bot):
    await bot.add_cog(Img(bot))
