import discord
from discord.ext import commands
import requests
import asyncio
import random
import datetime
from cogs.config import Config
from cogs.utils import send_message, send_error_message, generate_help_pages


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "Fun and games commands\nfun"
        self.cfg = Config()

    @commands.command(name="fun", description="Fun commands", usage="")
    async def fun(self, ctx, selected_page: int = 1):
        cfg = self.cfg
        pages = generate_help_pages(self.bot, "Fun")

        await send_message(
            ctx,
            {
                "title": f"Fun Commands",
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

    @commands.command(name="coinflip", description="Flip a coin", aliases=["cf"])
    async def coinflip(self, ctx):
        sides = ["heads", "tails"]
        result = random.choice(sides)
        await send_message(
            ctx,
            {"title": "Coin Flip", "description": f"The coin landed on **{result}**!"},
        )
        await ctx.message.delete()

    @commands.command(
        name="8ball",
        description="Ask the magic 8ball a question",
        usage="[question]",
        aliases=["magic8ball"],
    )
    async def eightball(self, ctx, *, question: str):
        responses = [
            "It is certain",
            "It is decidedly so",
            "Without a doubt",
            "Yes definitely",
            "You may rely on it",
            "As I see it, yes",
            "Most likely",
            "Outlook good",
            "Yes",
            "Signs point to yes",
            "Reply hazy try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful",
        ]

        await send_message(
            ctx, {"title": question, "description": random.choice(responses)}
        )
        await ctx.message.delete()

    @commands.command(
        name="dice",
        description="Roll a dice with specific sides",
        usage="[sides]",
        aliases=["roll"],
    )
    async def dice(self, ctx, sides: int = 6):
        number = random.randint(1, sides)
        await send_message(
            ctx,
            {
                "title": f"{sides} sided dice",
                "description": f"You rolled a **{number}**",
            },
        )
        await ctx.message.delete()

    @commands.command(name="dadjoke", description="Get a dad joke", usage="")
    async def dadjoke(self, ctx):
        r = requests.get(
            "https://icanhazdadjoke.com/", headers={"Accept": "application/json"}
        )
        joke = r.json()["joke"]
        await send_message(ctx, {"title": "Dad Joke", "description": joke})
        await ctx.message.delete()

    @commands.command(name="catfact", description="Get a random cat fact", usage="")
    async def catfact(self, ctx):
        r = requests.get("https://catfact.ninja/fact")
        fact = r.json()["fact"]
        await send_message(ctx, {"title": "Cat Fact", "description": fact})
        await ctx.message.delete()

    @commands.command(name="insult", description="Get a random insult", usage="")
    async def insult(self, ctx):
        r = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json")
        insult = r.json()["insult"]
        await ctx.send(insult)
        await ctx.message.delete()

    @commands.command(
        name="compliment", description="Get a random compliment", usage=""
    )
    async def compliment(self, ctx):
        r = requests.get(
            "https://8768zwfurd.execute-api.us-east-1.amazonaws.com/v1/compliments"
        )
        compliment = r.content.replace(b'"', b"").decode("utf-8")
        await ctx.send(compliment)
        await ctx.message.delete()

    @commands.command(name="meme", description="Get a random meme", usage="")
    async def meme(self, ctx):
        r = requests.get(
            "https://www.reddit.com/r/memes.json?sort=top&t=week",
            headers={"User-agent": "Mozilla/5.0"},
        )
        if r.status_code == 200:
            meme = random.choice(r.json()["data"]["children"])["data"]["url"]
            await ctx.send(meme)
            await ctx.message.delete()
        else:
            await send_error_message(ctx, "Failed to fetch meme")

    @commands.command(name="fakenitro", description="Fake a nitro gift", usage="")
    async def fakenitro(self, ctx):
        code = "".join(
            random.choices(
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=16
            )
        )
        await ctx.send(f"https://discord.gift/{code}")
        await ctx.message.delete()

    @commands.command(
        name="hyperlink",
        description="Create a hyperlink",
        usage="[link] [text]",
        aliases=["hyperl"],
    )
    async def hyperlink(self, ctx, link: str, *, text: str):
        await ctx.send(f"[{text}]({link})")
        await ctx.message.delete()

    @commands.command(name="rps", description="Play rock paper scissors", usage="")
    async def rps(self, ctx):
        choices = ["rock", "paper", "scissors"]
        result = random.choice(choices)
        await send_message(
            ctx,
            {
                "title": "Rock Paper Scissors",
                "description": f"Computer chose: **{result}**",
            },
        )
        await ctx.message.delete()

    @commands.command(
        name="slots", description="Play a slot machine", aliases=["slotmachine"]
    )
    async def slots(self, ctx):
        emojis = ["🍒", "🍊", "🍎", "💎", "🍆", "🍉", "7️⃣"]

        msg = await ctx.send("🎰 **Spinning...** 🎰")
        await ctx.message.delete()

        for _ in range(5):
            reels = [random.choice(emojis) for _ in range(3)]
            await msg.edit(
                content=f"```\n┌─────────────┐\n│ {reels[0]} {reels[1]} {reels[2]} │\n└─────────────┘```"
            )
            await asyncio.sleep(0.3)

        reels = [random.choice(emojis) for _ in range(3)]

        if reels[0] == reels[1] == reels[2]:
            result = "🎉 YOU WON! 🎉"
        elif reels[0] == reels[1] or reels[1] == reels[2] or reels[0] == reels[2]:
            result = "So close! Two matched!"
        else:
            result = "You lost!"

        await msg.edit(
            content=f"```\n╔═════════════════╗\n║  ▶ {reels[0]} {reels[1]} {reels[2]} ◀  ║\n╚═════════════════╝\n\n{result}```"
        )

    @commands.command(name="kanye", description="Random Kanye quote", usage="")
    async def kanye(self, ctx):
        resp = requests.get("https://api.kanye.rest/")
        if resp.status_code == 200:
            quote = resp.json()["quote"]
            await send_message(ctx, {"title": "Kanye Quote", "description": quote})
        else:
            await send_error_message(ctx, "Failed to get Kanye quote")
        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(Fun(bot))
