import requests
from discord.ext import commands
from cogs.config import Config
from cogs.utils import send_message, send_error_message


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "Utility commands\nutils"
        self.cfg = Config()

    def _ensure_msglog_config(self, cfg):
        changed = False
        defaults = {
            "message_logger_webhook": "",
            "message_logger_enabled": False,
            "message_logger_only_added": False,
            "message_logger_allowed_channels": [],
            "message_logger_allowed_guilds": [],
            "message_logger_blocked_channels": [],
            "nitro_sniper_webhook": "",
        }
        for key, value in defaults.items():
            if key not in cfg.data:
                cfg.data[key] = value
                changed = True
        if changed:
            cfg.save()

    @commands.command(name="utils", description="Utility commands list", usage="")
    async def utils(self, ctx):
        cfg = self.cfg
        cfg.load()
        pages = {
            "codeblock": "connect :: Bind webhook to feature (1 hookembed / 2 msglogger / 3 sniper)\nrpc show :: Show your current RPC activity\nhyperlink :: Create a hyperlink\ncembed :: Create a custom embed\nnowplaying :: Show current playing song\nnitro sniper :: Webhook target 3 is reserved for sniper logs\nmessagelogger :: .msglog addchannel/addguild/blockchannel/removechannel/removeguild/unblockchannel/onlyadded\n",
            "embed": "**connect** Bind webhook to feature (1 hookembed / 2 msglogger / 3 sniper)\n**rpc show** Show your current RPC activity\n**hyperlink** Create a hyperlink\n**cembed** Create a custom embed\n**nowplaying** Show current playing song\n**nitro sniper** Webhook target 3 is reserved for sniper logs\n**messagelogger** .msglog addchannel/addguild/blockchannel/removechannel/removeguild/unblockchannel/onlyadded\n",
            "image": "**connect** Bind webhook to feature (1 hookembed / 2 msglogger / 3 sniper)\n**rpc show** Show your current RPC activity\n**hyperlink** Create a hyperlink\n**cembed** Create a custom embed\n**nowplaying** Show current playing song\n**nitro sniper** Webhook target 3 is reserved for sniper logs\n**messagelogger** .msglog addchannel/addguild/blockchannel/removechannel/removeguild/unblockchannel/onlyadded\n",
            "hookembed": "**connect** Bind webhook to feature (1 hookembed / 2 msglogger / 3 sniper)\n**rpc show** Show your current RPC activity\n**hyperlink** Create a hyperlink\n**cembed** Create a custom embed\n**nowplaying** Show current playing song\n**nitro sniper** Webhook target 3 is reserved for sniper logs\n**messagelogger** .msglog addchannel/addguild/blockchannel/removechannel/removeguild/unblockchannel/onlyadded\n",
        }
        style = cfg.get("message_settings")["style"]

        await send_message(
            ctx,
            {
                "title": "Utils Commands",
                "description": pages.get(style, pages["embed"]),
                "codeblock_desc": pages["codeblock"],
            },
        )
        await ctx.message.delete()

    @commands.command(
        name="messagelogger",
        aliases=["msglog"],
        description="Toggle message logger webhook",
        usage="[on|off|status|addchannel|addguild|blockchannel|removechannel|removeguild|unblockchannel|onlyadded]",
    )
    async def messagelogger(self, ctx, mode: str = "status", value: str = ""):
        cfg = self.cfg
        cfg.load()
        self._ensure_msglog_config(cfg)
        mode = mode.lower().strip()

        parts = mode.split()
        action = parts[0]

        if action not in (
            "on",
            "off",
            "status",
            "addchannel",
            "addguild",
            "blockchannel",
            "removechannel",
            "removeguild",
            "unblockchannel",
            "onlyadded",
        ):
            await send_error_message(
                ctx,
                "Usage: .msglog [on|off|status|addchannel <id>|addguild <id>|blockchannel <id>|removechannel <id>|removeguild <id>|unblockchannel <id>|onlyadded <true/false>]",
            )
            return

        if action == "on":
            if not cfg.get("message_logger_webhook"):
                await send_error_message(
                    ctx,
                    "No webhook bound. Use .connect <webhook_url> 2 first",
                )
                return
            cfg.data["message_logger_enabled"] = True
            cfg.save()
        elif action == "off":
            cfg.data["message_logger_enabled"] = False
            cfg.save()
        elif action == "addchannel":
            target_id = value.strip()
            if not target_id:
                await send_error_message(ctx, "Usage: .msglog addchannel <channel_id>")
                return
            if not target_id.isdigit():
                await send_error_message(ctx, "ID must be numeric")
                return

            if target_id not in cfg.data["message_logger_allowed_channels"]:
                cfg.data["message_logger_allowed_channels"].append(target_id)
            cfg.save()
            await send_message(
                ctx,
                {"title": "Message Logger", "description": f"Added channel ID **{target_id}**"},
            )
            await ctx.message.delete()
            return
        elif action == "addguild":
            target_id = value.strip()
            if not target_id:
                await send_error_message(ctx, "Usage: .msglog addguild <guild_id>")
                return
            if not target_id.isdigit():
                await send_error_message(ctx, "ID must be numeric")
                return

            if target_id not in cfg.data["message_logger_allowed_guilds"]:
                cfg.data["message_logger_allowed_guilds"].append(target_id)
            cfg.save()
            await send_message(
                ctx,
                {"title": "Message Logger", "description": f"Added guild ID **{target_id}**"},
            )
            await ctx.message.delete()
            return
        elif action == "removechannel":
            target_id = value.strip()
            if not target_id:
                await send_error_message(ctx, "Usage: .msglog removechannel <channel_id>")
                return
            if target_id in cfg.data["message_logger_allowed_channels"]:
                cfg.data["message_logger_allowed_channels"].remove(target_id)
            cfg.save()
            await send_message(
                ctx,
                {
                    "title": "Message Logger",
                    "description": f"Removed channel ID **{target_id}**",
                },
            )
            await ctx.message.delete()
            return
        elif action == "removeguild":
            target_id = value.strip()
            if not target_id:
                await send_error_message(ctx, "Usage: .msglog removeguild <guild_id>")
                return
            if target_id in cfg.data["message_logger_allowed_guilds"]:
                cfg.data["message_logger_allowed_guilds"].remove(target_id)
            cfg.save()
            await send_message(
                ctx,
                {
                    "title": "Message Logger",
                    "description": f"Removed guild ID **{target_id}**",
                },
            )
            await ctx.message.delete()
            return
        elif action == "blockchannel":
            target_id = value.strip()
            if not target_id:
                await send_error_message(ctx, "Usage: .msglog blockchannel <channel_id>")
                return
            if not target_id.isdigit():
                await send_error_message(ctx, "ID must be numeric")
                return
            if target_id not in cfg.data["message_logger_blocked_channels"]:
                cfg.data["message_logger_blocked_channels"].append(target_id)
            cfg.save()
            await send_message(
                ctx,
                {"title": "Message Logger", "description": f"Blocked channel ID **{target_id}**"},
            )
            await ctx.message.delete()
            return
        elif action == "unblockchannel":
            target_id = value.strip()
            if not target_id:
                await send_error_message(ctx, "Usage: .msglog unblockchannel <channel_id>")
                return
            if target_id in cfg.data["message_logger_blocked_channels"]:
                cfg.data["message_logger_blocked_channels"].remove(target_id)
            cfg.save()
            await send_message(
                ctx,
                {"title": "Message Logger", "description": f"Unblocked channel ID **{target_id}**"},
            )
            await ctx.message.delete()
            return
        elif action == "onlyadded":
            val = value.strip().lower()
            if not val:
                await send_error_message(ctx, "Usage: .msglog onlyadded <true|false>")
                return
            if val not in ("true", "false"):
                await send_error_message(ctx, "onlyadded value must be true or false")
                return
            cfg.data["message_logger_only_added"] = val == "true"
            cfg.save()

        enabled = cfg.get("message_logger_enabled") is True
        only_added = cfg.get("message_logger_only_added") is True
        channels_count = len(cfg.get("message_logger_allowed_channels") or [])
        guilds_count = len(cfg.get("message_logger_allowed_guilds") or [])
        blocked_channels = len(cfg.get("message_logger_blocked_channels") or [])
        await send_message(
            ctx,
            {
                "title": "Message Logger",
                "description": (
                    f"Status: **{'ON' if enabled else 'OFF'}**\n"
                    f"Only Added: **{only_added}**\n"
                    f"Allowed Channels: **{channels_count}**\n"
                    f"Allowed Guilds: **{guilds_count}**\n"
                    f"Blocked Channels: **{blocked_channels}**"
                ),
            },
        )
        await ctx.message.delete()

    def _should_log_message(self, cfg, message):
        if not cfg.get("message_logger_enabled"):
            return False

        if not cfg.get("message_logger_only_added"):
            return True

        allowed_channels = set(cfg.get("message_logger_allowed_channels") or [])
        allowed_guilds = set(cfg.get("message_logger_allowed_guilds") or [])
        blocked_channels = set(cfg.get("message_logger_blocked_channels") or [])

        channel_id = str(getattr(message.channel, "id", ""))
        guild_id = str(getattr(message.guild, "id", "")) if message.guild else ""

        if channel_id in blocked_channels:
            return False

        return channel_id in allowed_channels or guild_id in allowed_guilds

    def _post_log(self, embed):
        cfg = Config()
        webhook = cfg.get("message_logger_webhook")
        if not webhook:
            return
        try:
            requests.post(webhook, json={"embeds": [embed]}, timeout=10)
        except Exception:
            return

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        cfg = Config()
        self._ensure_msglog_config(cfg)
        if not self._should_log_message(cfg, message):
            return
        if getattr(message, "webhook_id", None):
            return
        if not message.content:
            return

        author = str(message.author) if message.author else "Unknown"
        channel = getattr(message.channel, "mention", "Unknown")
        guild = getattr(message.guild, "name", "DM") if message.guild else "DM"

        embed = {
            "title": "Message Deleted",
            "description": message.content[:3900],
            "color": int("ff4d4d", 16),
            "fields": [
                {"name": "Author", "value": author, "inline": True},
                {"name": "Channel", "value": channel, "inline": True},
                {"name": "Guild", "value": guild, "inline": True},
            ],
        }
        self._post_log(embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        cfg = Config()
        self._ensure_msglog_config(cfg)
        if not self._should_log_message(cfg, after):
            return
        if getattr(after, "webhook_id", None):
            return
        if before.content == after.content:
            return

        author = str(after.author) if after.author else "Unknown"
        channel = getattr(after.channel, "mention", "Unknown")
        guild = getattr(after.guild, "name", "DM") if after.guild else "DM"

        embed = {
            "title": "Message Edited",
            "color": int("ffaa33", 16),
            "fields": [
                {"name": "Author", "value": author, "inline": True},
                {"name": "Channel", "value": channel, "inline": True},
                {"name": "Guild", "value": guild, "inline": True},
                {
                    "name": "Before",
                    "value": (before.content or "(empty)")[:1024],
                    "inline": False,
                },
                {
                    "name": "After",
                    "value": (after.content or "(empty)")[:1024],
                    "inline": False,
                },
            ],
        }
        self._post_log(embed)


async def setup(bot):
    await bot.add_cog(Utils(bot))
