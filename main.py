from discord.ext import commands
import asyncio
from cogs.config import Config
import art


async def main():
    cfg = Config()

    bot = commands.Bot(
        command_prefix=cfg.get("prefix"), self_bot=True, help_command=None
    )
    bot.cfg = cfg

    @bot.event
    async def on_ready():
        print("\n" + "=" * 50)
        print(art.text2art("Darky", font="starwars"))
        print(" " * 15 + "Version 1.0")
        print("=" * 50)
        print(f"User: {bot.user.name}")
        print(f"ID: {bot.user.id}")
        print(f"Prefix: {cfg.get('prefix')}")
        print(f"Style: {cfg.get('message_settings')['style']}")
        print("=" * 50 + "\n")

    @bot.event
    async def on_message(message):
        if message.author.id != bot.user.id:
            await bot.process_commands(message)
            return

        if message.content.startswith(cfg.get("prefix")):
            print(f"[COMMAND] {message.content}")

        await bot.process_commands(message)

    @bot.command(name="reloadconfig")
    async def reloadconfig(ctx):
        cfg.load()
        await ctx.send("Configuration reloaded")
        await ctx.message.delete()

    cogs = [
        "general",
        "text",
        "fun",
        "img",
        "settings",
        "animations",
        "legit",
        "utility",
    ]
    for cog in cogs:
        try:
            await bot.load_extension(f"cogs.{cog}")
            print(f"Loaded: {cog}")
        except Exception as e:
            print(f"Error {cog}: {e}")

    await bot.start(cfg.get("token"))


if __name__ == "__main__":
    asyncio.run(main())
