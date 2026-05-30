import discord
from discord.ext import commands
from cogs.config import Config
from cogs.utils import send_message, send_error_message


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "Bot configuration\nsettings"
        self.cfg = Config()

    @commands.command(name="settings", description="View bot settings", usage="")
    async def settings(self, ctx):
        cfg = self.cfg

        embed_desc = f"""
**Message Style:** `{cfg.get("message_settings")["style"]}`
  Change: `.setstyle [codeblock/embed/image/hookembed]`

**Hook Webhook:** `{'set' if cfg.get('rich_embed_webhook') else 'not set'}`
  Set: `.connect [webhook_url]` then choose `1`

**Message Logger Webhook:** `{'set' if cfg.get('message_logger_webhook') else 'not set'}`
  Set: `.connect [webhook_url]` then choose `2`

**Nitro Sniper Webhook:** `{'set' if cfg.get('nitro_sniper_webhook') else 'not set'}`
  Set: `.connect [webhook_url]` then choose `3`

**Auto Delete Delay:** `{cfg.get("message_settings")["auto_delete_delay"]}s`
  Change: `.setdeletedelay [seconds]`

**Edit Original:** `{cfg.get("message_settings")["edit_og"]}`
  Toggle: `.editog`

**Theme Title:** `{cfg.theme.title}`
  Change: `.settitle [text]`

**Theme Colour:** `{cfg.theme.colour}`
  Change: `.setcolour [#hex]`

**Theme Footer:** `{cfg.theme.footer}`
  Change: `.setfooter [text]`

**Theme Emoji:** `{cfg.theme.emoji}`
  Change: `.setemoji [emoji]`

**Theme Image:** `{cfg.theme.image[:50]}...`
  Change: `.setimage [url]`
        """

        await send_message(ctx, {"title": "Darky Settings", "description": embed_desc})
        await ctx.message.delete()

    @commands.command(name="setstyle", description="Set message style", usage="[style]")
    async def setstyle(self, ctx, style: str):
        cfg = self.cfg
        valid_styles = ["codeblock", "embed", "image", "hookembed"]

        if style.lower() not in valid_styles:
            await send_error_message(
                ctx, f"Invalid style. Options: {', '.join(valid_styles)}"
            )
            return

        cfg.data["message_settings"]["style"] = style.lower()
        cfg.save()
        await send_message(
            ctx,
            {
                "title": "Success",
                "description": f"Message style set to **{style.lower()}**",
            },
        )
        await ctx.message.delete()

    @commands.command(name="connect", description="Bind webhook to feature", usage="[url]")
    async def connect(self, ctx, webhook_url: str):
        cfg = self.cfg
        if not webhook_url.startswith("https://discord.com/api/webhooks/"):
            await send_error_message(ctx, "Invalid webhook URL")
            return

        prompt = await send_message(
            ctx,
            {
                "title": "Connect Webhook",
                "description": (
                    "Choose target:\n"
                    "**1** Hookembed\n"
                    "**2** Messagelogger\n"
                    "**3** Sniper"
                ),
                "codeblock_desc": "Choose target:\n1 :: Hookembed\n2 :: Messagelogger\n3 :: Sniper",
            },
            delete_after=False,
        )

        def check(msg):
            return msg.author.id == ctx.author.id and msg.channel.id == ctx.channel.id

        try:
            reply = await self.bot.wait_for("message", timeout=30.0, check=check)
        except Exception:
            await send_error_message(ctx, "Connect timeout. Try again")
            await ctx.message.delete()
            return

        target = reply.content.strip().lower()
        if target == "1":
            cfg.data["rich_embed_webhook"] = webhook_url
            bind_name = "hookembed"
        elif target == "2":
            cfg.data["message_logger_webhook"] = webhook_url
            bind_name = "messagelogger"
        elif target == "3":
            cfg.data["nitro_sniper_webhook"] = webhook_url
            bind_name = "sniper"
        else:
            await send_error_message(
                ctx,
                "Invalid target. Use 1, 2 or 3",
            )
            await ctx.message.delete()
            try:
                await reply.delete()
            except Exception:
                pass
            try:
                await prompt.delete()
            except Exception:
                pass
            return

        cfg.save()
        await send_message(
            ctx,
            {
                "title": "Connected",
                "description": f"Webhook bound to **{bind_name}**",
            },
        )
        try:
            await reply.delete()
        except Exception:
            pass
        try:
            await prompt.delete()
        except Exception:
            pass
        await ctx.message.delete()

    @commands.command(
        name="setcolour", description="Set embed colour", usage="[hex colour]"
    )
    async def setcolour(self, ctx, colour: str):
        cfg = self.cfg

        if not colour.startswith("#"):
            colour = "#" + colour

        try:
            int(colour[1:], 16)
        except ValueError:
            await send_error_message(ctx, "Invalid hex colour. Use format: #RRGGBB")
            return

        cfg.data["theme"]["colour"] = colour
        cfg.save()
        await send_message(
            ctx,
            {"title": "Success", "description": f"Theme colour set to **{colour}**"},
        )
        await ctx.message.delete()

    @commands.command(name="setfooter", description="Set embed footer", usage="[text]")
    async def setfooter(self, ctx, *, text: str):
        cfg = self.cfg
        cfg.data["theme"]["footer"] = text
        cfg.save()
        await send_message(
            ctx, {"title": "Success", "description": f"Theme footer set to **{text}**"}
        )
        await ctx.message.delete()

    @commands.command(name="settitle", description="Set embed title", usage="[text]")
    async def settitle(self, ctx, *, text: str):
        cfg = self.cfg
        cfg.data["theme"]["title"] = text
        cfg.save()
        await send_message(
            ctx, {"title": "Success", "description": f"Theme title set to **{text}**"}
        )
        await ctx.message.delete()

    @commands.command(name="setemoji", description="Set theme emoji", usage="[emoji]")
    async def setemoji(self, ctx, emoji: str):
        cfg = self.cfg
        cfg.data["theme"]["emoji"] = emoji
        cfg.save()
        await send_message(
            ctx, {"title": "Success", "description": f"Theme emoji set to **{emoji}**"}
        )
        await ctx.message.delete()

    @commands.command(name="setimage", description="Set theme image", usage="[url]")
    async def setimage(self, ctx, url: str):
        cfg = self.cfg
        cfg.data["theme"]["image"] = url
        cfg.save()
        await send_message(
            ctx,
            {
                "title": "Success",
                "description": f"Theme image set to **{url[:50]}...**",
            },
        )
        await ctx.message.delete()

    @commands.command(
        name="setdeletedelay", description="Set auto-delete delay", usage="[seconds]"
    )
    async def setdeletedelay(self, ctx, seconds: int):
        cfg = self.cfg
        cfg.data["message_settings"]["auto_delete_delay"] = seconds
        cfg.save()
        await send_message(
            ctx,
            {
                "title": "Success",
                "description": f"Auto-delete delay set to **{seconds}s**",
            },
        )
        await ctx.message.delete()

    @commands.command(
        name="editog", description="Toggle editing original message", usage=""
    )
    async def editog(self, ctx):
        cfg = self.cfg
        current = cfg.get("message_settings")["edit_og"]
        cfg.data["message_settings"]["edit_og"] = not current
        cfg.save()
        await send_message(
            ctx,
            {
                "title": "Success",
                "description": f"Edit original message: **{'Enabled' if not current else 'Disabled'}**",
            },
        )
        await ctx.message.delete()

    @commands.command(name="reload", description="Reload configuration", usage="")
    async def reload(self, ctx):
        cfg = Config()
        await send_message(
            ctx, {"title": "Success", "description": "Configuration reloaded"}
        )
        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(Settings(bot))
