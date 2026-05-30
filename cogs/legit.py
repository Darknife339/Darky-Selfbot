import discord
from discord.ext import commands
import asyncio
import random
import requests
import subprocess
import json
from cogs.config import Config
from cogs.utils import send_message, send_error_message

try:
    from winmedia_controller.media_controller import MediaController
except Exception:
    MediaController = None


async def type_delay(ctx, min_time=0.1, max_time=0.3):
    await ctx.channel.typing()
    await asyncio.sleep(random.uniform(min_time, max_time))


class Legit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "Legitimacy features\nlegit"
        self.rate_limit_delay = 0.5
        self.cfg = Config()
        self.nowplaying_tasks = {}
        self.nowplaying_messages = {}
        self.media_controller = MediaController() if MediaController is not None else None
        self.last_activities = []

    @commands.command(name="typing", description="Toggle typing indicator", usage="")
    async def typing_cmd(self, ctx):
        await ctx.send("Typing indicator is now enabled by default for all commands")
        await ctx.message.delete()

    @commands.command(
        name="ratelimit", description="Set rate limit delay", usage="[seconds]"
    )
    async def ratelimit(self, ctx, seconds: float = 0.5):
        self.rate_limit_delay = seconds
        await ctx.send(f"Rate limit delay set to {seconds}s")
        await ctx.message.delete()

    @commands.command(
        name="status",
        description="Set your custom status with optional emoji",
        usage='[emoji(optional)] [text]',
    )
    async def status(self, ctx, emoji_or_text: str = None, *, text: str = None):
        if emoji_or_text is None:
            await send_error_message(ctx, "Usage: .status [emoji(optional)] [text]")
            return

        emoji = None
        status_text = emoji_or_text

        if text is not None:
            emoji = emoji_or_text
            status_text = text

        activity = discord.CustomActivity(name=status_text, emoji=emoji)
        await self.bot.change_presence(activity=activity)
        await send_message(
            ctx,
            {
                "title": "Status Updated",
                "description": f"{emoji + ' ' if emoji else ''}{status_text}",
            },
        )
        await ctx.message.delete()

    @commands.command(name="rpc", description="Show or set your RPC/activity", usage="show|playing|streaming|listen|figting [text]")
    async def rpc(self, ctx, action: str = "show", *, text: str = None):
        action = action.lower().strip()

        if action in ("playing", "streaming", "listen", "figting"):
            if not text or not text.strip():
                await send_error_message(
                    ctx,
                    "Usage: .rpc playing <text> | .rpc streaming <text> | .rpc listen <text> | .rpc figting <text>",
                )
                return

            if action == "playing":
                activity = discord.Game(name=text)
            elif action == "streaming":
                activity = discord.Streaming(name=text, url="https://twitch.tv/discord")
            elif action == "listen":
                activity = discord.Activity(type=discord.ActivityType.listening, name=text)
            else:
                activity = discord.Activity(type=discord.ActivityType.competing, name=text)

            await self.bot.change_presence(activity=activity)
            await send_message(
                ctx,
                {
                    "title": "RPC Updated",
                    "description": f"Set **{action}** to: **{text}**",
                },
            )
            await ctx.message.delete()
            return

        if action != "show":
            await send_error_message(
                ctx,
                "Usage: .rpc show | .rpc playing <text> | .rpc streaming <text> | .rpc listen <text> | .rpc figting <text>",
            )
            return

        activities = []

        # 1) Try member activities from current guild
        if ctx.guild:
            me = ctx.guild.get_member(self.bot.user.id)
            if me and getattr(me, "activities", None):
                activities = list(me.activities)

        # 2) Try author activities (works in many selfbot contexts)
        if not activities and getattr(ctx.author, "activities", None):
            activities = list(ctx.author.activities)

        # 3) Try cached activities from presence updates
        if not activities and self.last_activities:
            activities = list(self.last_activities)

        # 4) Fallback to user object activities
        if not activities and getattr(self.bot.user, "activities", None):
            activities = list(self.bot.user.activities)

        if len(activities) == 0:
            await send_error_message(ctx, "No activity/RPC is currently shown")
            return

        activity = activities[0]
        name = getattr(activity, "name", "Unknown") or "Unknown"
        details = getattr(activity, "details", "") or ""
        state = getattr(activity, "state", "") or ""

        assets = getattr(activity, "assets", None)
        large_text = getattr(assets, "large_text", "") if assets else ""
        small_text = getattr(assets, "small_text", "") if assets else ""

        large_url = ""
        small_url = ""
        if assets:
            try:
                if getattr(assets, "large_image", None):
                    large_url = getattr(assets.large_image, "url", "") or ""
            except Exception:
                large_url = ""
            try:
                if getattr(assets, "small_image", None):
                    small_url = getattr(assets.small_image, "url", "") or ""
            except Exception:
                small_url = ""

        activity_type = getattr(activity, "type", None)
        activity_type_map = {
            discord.ActivityType.playing: "Playing",
            discord.ActivityType.streaming: "Streaming",
            discord.ActivityType.listening: "Listening",
            discord.ActivityType.watching: "Watching",
            discord.ActivityType.custom: "Custom",
            discord.ActivityType.competing: "Fighting/Competing",
        }
        type_label = activity_type_map.get(activity_type, str(activity_type).split(".")[-1].title())

        lines = [f"**Type:** {type_label}", f"**Name:** {name}"]
        if details:
            lines.append(f"**Details:** {details}")
        if state:
            lines.append(f"**State:** {state}")
        if large_text:
            lines.append(f"**Large Image Text:** {large_text}")
        if small_text:
            lines.append(f"**Small Image Text:** {small_text}")

        style = self.cfg.get("message_settings")["style"]
        if style in ("hookembed", "codeblock"):
            if large_url:
                lines.append(f"**Large Image URL:** {large_url}")
            if small_url:
                lines.append(f"**Small Image URL:** {small_url}")

        thumbnail = large_url or small_url or self.cfg.theme.image
        await send_message(
            ctx,
            {
                "title": "RPC Show",
                "description": "\n".join(lines),
                "codeblock_desc": "\n".join(line.replace("**", "") for line in lines),
                "thumbnail": thumbnail,
            },
            delete_after=False,
        )
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        if not self.bot.user:
            return
        if after.id != self.bot.user.id:
            return
        if getattr(after, "activities", None):
            self.last_activities = list(after.activities)

    async def _get_current_media(self):
        if self.media_controller is not None:
            try:
                info = await self.media_controller.get_media_info()
                if not info:
                    return None

                title = str(info.get("title", "")).strip()
                artist = str(info.get("artist", "")).strip()

                if not title and not artist:
                    return None

                return {
                    "title": title or "Unknown title",
                    "artist": artist or "Unknown artist",
                }
            except Exception:
                pass

        ps_script = "[Windows.Media.Control.GlobalSystemMediaTransportControlsSessionManager, Windows.Media.Control, ContentType=WindowsRuntime] > $null; $m=[Windows.Media.Control.GlobalSystemMediaTransportControlsSessionManager]::RequestAsync().GetAwaiter().GetResult(); $s=$m.GetCurrentSession(); if($null -eq $s){ '{\"title\":\"\",\"artist\":\"\"}'; exit }; $p=$s.TryGetMediaPropertiesAsync().GetAwaiter().GetResult(); @{title=[string]$p.Title;artist=[string]$p.Artist} | ConvertTo-Json -Compress"

        try:
            proc = await asyncio.to_thread(
                subprocess.run,
                ["powershell", "-NoProfile", "-Command", ps_script],
                capture_output=True,
                text=True,
                timeout=6,
            )
        except Exception:
            return None

        if proc.returncode != 0:
            return None

        try:
            payload = json.loads(proc.stdout.strip() or "{}")
        except Exception:
            return None

        title = str(payload.get("title", "")).strip()
        artist = str(payload.get("artist", "")).strip()

        if not title and not artist:
            return None

        return {"title": title or "Unknown title", "artist": artist or "Unknown artist"}

    def _get_cover_url(self, title, artist):
        query = f"{title} {artist}".strip().replace(" ", "+")
        try:
            resp = requests.get(
                f"https://itunes.apple.com/search?term={query}&entity=song&limit=1",
                timeout=8,
            )
            if resp.status_code != 200:
                return ""
            data = resp.json()
            if data.get("resultCount", 0) == 0:
                return ""
            result = data["results"][0]
            return result.get("artworkUrl100", "").replace("100x100bb", "600x600bb")
        except Exception:
            return ""

    async def _stop_nowplaying(self, channel_id):
        task = self.nowplaying_tasks.pop(channel_id, None)
        self.nowplaying_messages.pop(channel_id, None)
        if task and not task.done():
            task.cancel()

    async def _nowplaying_loop(self, ctx):
        channel_id = ctx.channel.id
        last_key = None

        try:
            while channel_id in self.nowplaying_tasks:
                media = await self._get_current_media()
                if media is None:
                    await asyncio.sleep(2)
                    continue

                key = (media["title"], media["artist"])
                if key != last_key:
                    old_message_id = self.nowplaying_messages.get(channel_id)
                    if old_message_id:
                        try:
                            old_msg = await ctx.channel.fetch_message(old_message_id)
                            await old_msg.delete()
                        except Exception:
                            pass

                    cfg = self.cfg
                    style = cfg.get("message_settings")["style"]
                    cover_url = ""
                    if style in ("image", "embed"):
                        cover_url = self._get_cover_url(media["title"], media["artist"])

                    new_msg = await send_message(
                        ctx,
                        {
                            "title": "Now Playing",
                            "description": f"**Track:** {media['title']}\n**Artist:** {media['artist']}",
                            "codeblock_desc": f"Track  :: {media['title']}\nArtist :: {media['artist']}",
                            "thumbnail": cover_url or cfg.theme.image,
                        },
                        delete_after=False,
                    )
                    self.nowplaying_messages[channel_id] = new_msg.id
                    last_key = key

                await asyncio.sleep(2)
        except asyncio.CancelledError:
            return

    @commands.command(name="nowplaying", description="Show current playing song", usage="")
    async def nowplaying(self, ctx):
        if self.media_controller is None:
            await send_error_message(
                ctx,
                "winmedia_controller is not installed. Run pip install -r requirements.txt",
            )
            return

        media = await self._get_current_media()
        if media is None:
            await send_error_message(ctx, "No active media session found on this PC")
            return

        await self._stop_nowplaying(ctx.channel.id)
        task = asyncio.create_task(self._nowplaying_loop(ctx))
        self.nowplaying_tasks[ctx.channel.id] = task
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        channel_id = payload.channel_id
        message_id = payload.message_id
        tracked_message_id = self.nowplaying_messages.get(channel_id)

        if tracked_message_id and tracked_message_id == message_id:
            await self._stop_nowplaying(channel_id)


async def setup(bot):
    await bot.add_cog(Legit(bot))
