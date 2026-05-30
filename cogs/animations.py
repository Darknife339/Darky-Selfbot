import discord
from discord.ext import commands
import asyncio
import random
import time
from cogs.config import Config
from cogs.utils import send_message, send_error_message

running_animations = {}


class Animations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "Text animation commands\nanimations"
        self.cfg = Config()
        self.running_animations = {}
        self.auto_animation = None
        self.suppress_auto_until = {}

    @commands.command(
        name="animations", description="View animation commands", usage="", aliases=["anim"]
    )
    async def animations(self, ctx, selected_page: int = 1):
        cfg = self.cfg
        pages = {
            "codeblock": [
                "animate :: Type text letter by letter",
                "animatebold :: Type text with bold letters",
                "animateupper :: Type text with uppercase letters",
                "animateboldupper :: Type text with bold uppercase letters",
                "typewriter :: Typewriter effect",
                "glitch :: Glitch text effect (10 iterations)",
                "lineappear :: Reveal text from right to left",
                "lineappearfade :: Reveal, then hide text",
                "textfall :: Make text fall down",
                "textfallbounce :: Fall down and rise back",
                "looptextfall :: Loop fall and rise (use .stop)",
                "autoanim :: Auto animate your next messages",
                "autoanim glitch :: Auto glitch animation",
                "autoanim typewriter :: Auto typewriter animation",
                "loopglitch :: Looping glitch (use .stop to end)",
                "looptext :: Looping text wave (use .stop to end)",
                "loopspin :: Looping spinner (use .stop to end)",
            ],
            "embed": [
                "**animate** Type text letter by letter",
                "**animatebold** Type text with bold letters",
                "**animateupper** Type text with uppercase letters",
                "**animateboldupper** Type text with bold uppercase letters",
                "**typewriter** Typewriter effect",
                "**glitch** Glitch text effect (10 iterations)",
                "**lineappear** Reveal text from right to left",
                "**lineappearfade** Reveal, then hide text",
                "**textfall** Make text fall down",
                "**textfallbounce** Fall down and rise back",
                "**looptextfall** Loop fall and rise (use .stop)",
                "**autoanim** Auto animate your next messages",
                "**autoanim glitch** Auto glitch animation",
                "**autoanim typewriter** Auto typewriter animation",
                "**loopglitch** Looping glitch (use .stop to end)",
                "**looptext** Looping text wave (use .stop to end)",
                "**loopspin** Looping spinner (use .stop to end)",
            ],
        }

        page_content = pages.get(cfg.get("message_settings")["style"], pages["embed"])

        await send_message(
            ctx,
            {
                "title": "Animation Commands",
                "description": "\n".join(page_content),
                "footer": f"Page {selected_page}/1",
            },
        )
        await ctx.message.delete()

    async def type_delay(self):
        await asyncio.sleep(random.uniform(0.05, 0.15))

    @commands.command(
        name="animate", description="Animate text letter by letter", usage="[text]"
    )
    async def animate(self, ctx, *, text: str):
        output = ""
        msg = await ctx.send(text[0] if text else " ")
        await ctx.message.delete()

        for letter in text:
            output += letter
            await msg.edit(content=output)
            await self.type_delay()

    @commands.command(
        name="animatebold", description="Animate text with bold letters", usage="[text]"
    )
    async def animatebold(self, ctx, *, text: str):
        bold_map = str.maketrans(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
            "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵",
        )
        output = ""
        msg = await ctx.send(text[0].translate(bold_map) if text else " ")
        await ctx.message.delete()

        for letter in text:
            output += letter.translate(bold_map)
            await msg.edit(content=output)
            await self.type_delay()

    @commands.command(
        name="animateupper", description="Animate text with uppercase", usage="[text]"
    )
    async def animateupper(self, ctx, *, text: str):
        output = ""
        msg = await ctx.send(text[0].upper() if text else " ")
        await ctx.message.delete()

        for letter in text:
            output += letter.upper()
            await msg.edit(content=output)
            await self.type_delay()

    @commands.command(
        name="animateboldupper",
        description="Animate with bold uppercase",
        usage="[text]",
    )
    async def animateboldupper(self, ctx, *, text: str):
        bold_upper = str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
            "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵",
        )
        output = ""
        msg = await ctx.send(text[0].upper().translate(bold_upper) if text else " ")
        await ctx.message.delete()

        for letter in text:
            output += letter.upper().translate(bold_upper)
            await msg.edit(content=output)
            await self.type_delay()

    @commands.command(
        name="typewriter", description="Typewriter effect", usage="[text]"
    )
    async def typewriter(self, ctx, *, text: str):
        output = ""
        msg = await ctx.send("▌")
        await ctx.message.delete()

        for letter in text:
            output += letter
            await msg.edit(content=output + "▌")
            await self.type_delay()
        await msg.edit(content=output)

    @commands.command(name="glitch", description="Glitch text effect", usage="[text]")
    async def glitch(self, ctx, *, text: str):
        glitch_chars = "░▒▓█▀▄▌▐▖▗▘▙▚▛▜▝▞▟"
        msg = await ctx.send(text)
        await ctx.message.delete()

        for _ in range(8):
            glitched = "".join(
                [
                    c if random.random() > 0.4 else random.choice(glitch_chars)
                    for c in text
                ]
            )
            await msg.edit(content=glitched)
            await asyncio.sleep(0.15)
        await msg.edit(content=text)

    @commands.command(
        name="lineappear", description="Reveal text from right to left", usage="[text]"
    )
    async def lineappear(self, ctx, *, text: str):
        if not text:
            await send_error_message(ctx, "Please provide text to animate")
            return

        length = len(text)
        msg = await ctx.send("-" * length)
        await ctx.message.delete()

        for i in range(1, length + 1):
            visible = text[-i:]
            hidden = "-" * (length - i)
            await msg.edit(content=f"{visible}{hidden}")
            await asyncio.sleep(0.2)

    @commands.command(
        name="lineappearfade",
        description="Reveal text, then hide it back",
        usage="[text]",
        aliases=["laf"],
    )
    async def lineappearfade(self, ctx, *, text: str):
        if not text:
            await send_error_message(ctx, "Please provide text to animate")
            return

        length = len(text)
        msg = await ctx.send("-" * length)
        await ctx.message.delete()

        for i in range(1, length + 1):
            visible = text[-i:]
            hidden = "-" * (length - i)
            await msg.edit(content=f"{visible}{hidden}")
            await asyncio.sleep(0.2)

        for i in range(length - 1, -1, -1):
            visible = text[-i:] if i > 0 else ""
            hidden = "-" * (length - i)
            await msg.edit(content=f"{visible}{hidden}")
            await asyncio.sleep(0.2)

    @commands.command(
        name="textfall", description="Make text fall down", usage="[text]"
    )
    async def textfall(self, ctx, *, text: str):
        if not text:
            await send_error_message(ctx, "Please provide text to animate")
            return

        steps = 8
        blank_line = "** **"
        lines = [blank_line for _ in range(steps + 1)]
        lines[0] = text

        msg = await ctx.send("\n".join(lines))
        await ctx.message.delete()

        for i in range(1, steps + 1):
            frame_lines = [blank_line for _ in range(steps + 1)]
            frame_lines[i] = text
            await msg.edit(content="\n".join(frame_lines))
            await asyncio.sleep(0.2)

    @commands.command(
        name="textfallbounce", description="Fall down and rise back", usage="[text]", aliases=["tfb"]
    )
    async def textfallbounce(self, ctx, *, text: str):
        if not text:
            await send_error_message(ctx, "Please provide text to animate")
            return

        steps = 8
        blank_line = "** **"
        lines = [blank_line for _ in range(steps + 1)]
        lines[0] = text

        msg = await ctx.send("\n".join(lines))
        await ctx.message.delete()

        for i in range(1, steps + 1):
            frame_lines = [blank_line for _ in range(steps + 1)]
            frame_lines[i] = text
            await msg.edit(content="\n".join(frame_lines))
            await asyncio.sleep(0.2)

        for i in range(steps - 1, -1, -1):
            frame_lines = [blank_line for _ in range(steps + 1)]
            frame_lines[i] = text
            await msg.edit(content="\n".join(frame_lines))
            await asyncio.sleep(0.2)

    @commands.command(
        name="looptextfall", description="Looping fall and rise", usage="[text]", aliases=["ltf"]
    )
    async def looptextfall(self, ctx, *, text: str):
        if not text:
            await send_error_message(ctx, "Please provide text to animate")
            return

        steps = 8
        blank_line = "** **"
        lines = [blank_line for _ in range(steps + 1)]
        lines[0] = text

        msg = await ctx.send("\n".join(lines))
        await ctx.message.delete()
        self.running_animations[ctx.channel.id] = msg

        try:
            while (
                ctx.channel.id in self.running_animations
                and self.running_animations[ctx.channel.id] == msg
            ):
                for i in range(1, steps + 1):
                    frame_lines = [blank_line for _ in range(steps + 1)]
                    frame_lines[i] = text
                    await msg.edit(content="\n".join(frame_lines))
                    await asyncio.sleep(0.2)

                for i in range(steps - 1, -1, -1):
                    frame_lines = [blank_line for _ in range(steps + 1)]
                    frame_lines[i] = text
                    await msg.edit(content="\n".join(frame_lines))
                    await asyncio.sleep(0.2)
        except:
            pass

    @commands.command(
        name="autoanim",
        description="Auto animate your next non-command messages",
        usage="[off|lineappear|lineappearfade|textfall|textfallbounce|glitch|typewriter]",
        aliases=["autanim"],
    )
    async def autoanim(self, ctx, mode: str = "off"):
        mode = mode.lower().strip()
        valid = {
            "off",
            "lineappear",
            "lineappearfade",
            "textfall",
            "textfallbounce",
            "glitch",
            "typewriter",
        }

        if mode not in valid:
            await send_error_message(ctx, f"Invalid mode. Options: {', '.join(sorted(valid))}")
            return

        self.auto_animation = None if mode == "off" else mode
        await send_message(
            ctx,
            {
                "title": "Auto Animation",
                "description": "Disabled" if mode == "off" else f"Enabled: **{mode}**",
            },
        )
        await ctx.message.delete()

    @commands.command(
        name="loopglitch", description="Looping glitch animation", usage="[text]", aliases=["lg"]
    )
    async def loopglitch(self, ctx, *, text: str):
        glitch_chars = "░▒▓█▀▄▌▐▖▗▘▙▚▛▜▝▞▟"
        msg = await ctx.send(text)
        await ctx.message.delete()

        self.running_animations[ctx.channel.id] = msg

        try:
            while (
                ctx.channel.id in self.running_animations
                and self.running_animations[ctx.channel.id] == msg
            ):
                glitched = "".join(
                    [
                        c if random.random() > 0.5 else random.choice(glitch_chars)
                        for c in text
                    ]
                )
                await msg.edit(content=glitched)
                await asyncio.sleep(0.3)
        except:
            pass

    @commands.command(
        name="looptext", description="Looping text wave animation", usage="[text]", aliases=["lt"]
    )
    async def looptext(self, ctx, *, text: str):
        msg = await ctx.send(text)
        await ctx.message.delete()

        self.running_animations[ctx.channel.id] = msg

        try:
            pos = 0
            while (
                ctx.channel.id in self.running_animations
                and self.running_animations[ctx.channel.id] == msg
            ):
                result = ""
                for i, c in enumerate(text):
                    if i == pos % len(text):
                        result += c.upper()
                    else:
                        result += c.lower()
                await msg.edit(content=result)
                pos += 1
                await asyncio.sleep(0.2)
        except:
            pass

    @commands.command(
        name="loopspin", description="Looping spinner animation", usage="[text]", aliases=["ls"]
    )
    async def loopspin(self, ctx, *, text: str = "Loading"):
        spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        msg = await ctx.send(f"{spinner[0]} {text}")
        await ctx.message.delete()

        self.running_animations[ctx.channel.id] = msg

        try:
            i = 0
            while (
                ctx.channel.id in self.running_animations
                and self.running_animations[ctx.channel.id] == msg
            ):
                await msg.edit(content=f"{spinner[i % len(spinner)]} {text}")
                i += 1
                await asyncio.sleep(0.15)
        except:
            pass

    @commands.command(name="stop", description="Stop running loop animation", usage="")
    async def stop(self, ctx):
        if ctx.channel.id in self.running_animations:
            del self.running_animations[ctx.channel.id]
            await send_message(
                ctx, {"title": "Stopped", "description": "Animation stopped"}
            )
            await ctx.message.delete()
        else:
            await send_error_message(ctx, "No running animation in this channel")

    @commands.command(name="loopcount", description="Show running animations", usage="")
    async def loopcount(self, ctx):
        count = len(self.running_animations)
        await send_message(
            ctx,
            {
                "title": "Running Animations",
                "description": f"**{count}** animation(s) running",
            },
        )
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.suppress_auto_until[ctx.channel.id] = time.time() + 3

    async def _run_auto_animation(self, message, mode):
        text = message.content
        if not text.strip():
            return

        if mode == "glitch":
            glitch_chars = "░▒▓█▀▄▌▐▖▗▘▙▚▛▜▝▞▟"
            original = text
            for _ in range(8):
                glitched = "".join(
                    [
                        c if random.random() > 0.4 else random.choice(glitch_chars)
                        for c in original
                    ]
                )
                await message.edit(content=glitched)
                await asyncio.sleep(0.15)
            await message.edit(content=original)
            return

        if mode == "typewriter":
            output = ""
            for letter in text:
                output += letter
                await message.edit(content=output + "▌")
                await asyncio.sleep(random.uniform(0.05, 0.15))
            await message.edit(content=output)
            return

        if mode == "lineappear":
            length = len(text)
            for i in range(1, length + 1):
                visible = text[-i:]
                hidden = "-" * (length - i)
                await message.edit(content=f"{visible}{hidden}")
                await asyncio.sleep(0.2)
            return

        if mode == "lineappearfade":
            length = len(text)
            for i in range(1, length + 1):
                visible = text[-i:]
                hidden = "-" * (length - i)
                await message.edit(content=f"{visible}{hidden}")
                await asyncio.sleep(0.2)
            for i in range(length - 1, -1, -1):
                visible = text[-i:] if i > 0 else ""
                hidden = "-" * (length - i)
                await message.edit(content=f"{visible}{hidden}")
                await asyncio.sleep(0.2)
            return

        steps = 8
        blank_line = "** **"
        lines = [blank_line for _ in range(steps + 1)]
        lines[0] = text
        await message.edit(content="\n".join(lines))

        for i in range(1, steps + 1):
            frame_lines = [blank_line for _ in range(steps + 1)]
            frame_lines[i] = text
            await message.edit(content="\n".join(frame_lines))
            await asyncio.sleep(0.2)

        if mode == "textfallbounce":
            for i in range(steps - 1, -1, -1):
                frame_lines = [blank_line for _ in range(steps + 1)]
                frame_lines[i] = text
                await message.edit(content="\n".join(frame_lines))
                await asyncio.sleep(0.2)

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.auto_animation is None:
            return
        if not self.bot.user or message.author.id != self.bot.user.id:
            return

        prefix = self.cfg.get("prefix")
        if message.content.startswith(prefix):
            return

        if message.channel.id in self.suppress_auto_until:
            if time.time() < self.suppress_auto_until[message.channel.id]:
                return

        try:
            await self._run_auto_animation(message, self.auto_animation)
        except Exception:
            return


async def setup(bot):
    await bot.add_cog(Animations(bot))
