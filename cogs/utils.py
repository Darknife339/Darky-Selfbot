import discord
import random
import discord_self_embed
import re
import os
import asyncio
import requests
from discord.ext import commands
from cogs.config import Config
from .imgembed import Embed


class Codeblock:
    def __init__(self, title="Darky", description="", extra_title="", footer=""):
        self.title = title
        self.description = description
        self.extra_title = extra_title
        self.footer = footer

    def __str__(self):
        content = f"```ansi\n"
        if self.extra_title:
            content += f"\u001b[1;36m{self.title}\u001b[0m - \u001b[1;33m{self.extra_title}\u001b[0m\n"
        else:
            content += f"\u001b[1;36m{self.title}\u001b[0m\n"
        if self.description:
            content += f"\n{self.description}\n"
        if self.footer:
            content += f"\n\u001b[0;37m{self.footer}\u001b[0m"
        content += "```"
        return content


def cog_desc(cmd, desc):
    return f"{desc}\n{cmd}"


def get_command_full_name(cmd):
    return f"{cmd.parent.name} {cmd.name}" if cmd.parent else cmd.name


def fake_markdown(text):
    bold_alphabet = "𝗮,𝗯,𝗰,𝗱,𝗲,𝗳,𝗴,𝗵,𝗶,𝗷,𝗸,𝗹,𝗺,𝗻,𝗼,𝗽,𝗾,𝗿,𝘀,𝘁,𝘂,𝘃,𝘄,𝘅,𝘆,𝘇"
    bold_uppercase = "𝗔,𝗕,𝗖,𝗗,𝗘,𝗙,𝗚,𝗛,𝗜,𝗝,𝗞,𝗟,𝗠,𝗡,𝗢,𝗣,𝗤,𝗥,𝗦,𝗧,𝗨,𝗩,𝗪,𝗫,𝗬,𝗭"
    numbers = "𝟬,𝟭,𝟮,𝟯,𝟰,𝟱,𝟲,𝟳,𝟴,𝟵"

    lowercase_table = str.maketrans(
        "abcdefghijklmnopqrstuvwxyz", bold_alphabet.replace(",", "")
    )
    uppercase_table = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ", bold_uppercase.replace(",", "")
    )
    numbers_table = str.maketrans("0123456789", numbers.replace(",", ""))

    def replace(match):
        text = match.group(0)
        if text.startswith("**") and text.endswith("**"):
            return (
                text[2:-2]
                .translate(lowercase_table)
                .translate(uppercase_table)
                .translate(numbers_table)
            )
        else:
            return text

    return re.sub(r"\*\*.*?\*\*|.", replace, text)


async def send_message(
    ctx, embed_obj: dict, extra_title="", extra_message="", delete_after=None
):
    cfg = Config()
    theme = cfg.theme

    title = embed_obj.get("title", theme.title)
    description = embed_obj.get("description", "")
    colour = embed_obj.get("colour", theme.colour)
    footer = embed_obj.get("footer", theme.footer)
    thumbnail = embed_obj.get("thumbnail", theme.image)
    codeblock_desc = embed_obj.get("codeblock_desc", description)

    if delete_after is False:
        delete_after = None
    elif delete_after is None:
        delete_after = cfg.get("message_settings")["auto_delete_delay"]

    msg_style = cfg.get("message_settings")["style"]

    if msg_style == "codeblock":
        description = re.sub(r"[*_~`]", "", codeblock_desc)
        if title == theme.title:
            title = f"{theme.emoji} {title}"

        if len(description.split("\n")) == 1:
            extra_title = description
            description = ""

        content = str(
            Codeblock(
                title=title,
                description=description,
                extra_title=extra_title,
                footer=footer,
            )
        )

        if cfg.get("message_settings")["edit_og"]:
            msg = await ctx.message.edit(content=content, delete_after=delete_after)
        else:
            msg = await ctx.send(content, delete_after=delete_after)

    elif msg_style == "embed":
        print(f"\n[EMBED DEBUG] === Starting embed generation ===")

        if title == theme.title:
            title = f"{theme.emoji} {title}"

        # Parse page number from footer if present
        current_page = 1
        total_pages = 1
        if footer and "page" in footer.lower():
            try:
                page_info = footer.split()[-1]
                current_page = int(page_info.split("/")[0])
            except:
                pass

        # Split description into pages (320 char limit for embeds)
        max_desc_length = 320
        description = description.strip()

        # Add footer to last page only
        if theme.footer and "page" not in (footer or "").lower():
            footer_text = f"\n\n{theme.footer}"
        else:
            footer_text = ""

        # Split into pages
        pages = []
        if len(description) <= max_desc_length:
            pages.append(description + footer_text)
            total_pages = 1
        else:
            # Split by lines first, then by characters
            lines = description.split("\n")
            current_page_text = ""
            for line in lines:
                if len(current_page_text) + len(line) + 1 <= max_desc_length:
                    current_page_text += line + "\n"
                else:
                    pages.append(current_page_text.strip())
                    current_page_text = line + "\n"
            if current_page_text.strip():
                pages.append(current_page_text.strip() + footer_text)
            total_pages = len(pages)

        # Get current page content
        page_index = current_page - 1
        if page_index >= len(pages):
            page_index = 0
        page_desc = pages[page_index]

        page_title = (
            f"{title} ({current_page}/{total_pages})" if total_pages > 1 else title
        )

        print(f"[EMBED DEBUG] Title: {page_title}")
        print(f"[EMBED DEBUG] Description length: {len(page_desc)}")
        print(f"[EMBED DEBUG] Page: {current_page}/{total_pages}")

        try:
            embed = discord_self_embed.Embed(
                "",
                description=fake_markdown(page_desc.strip()),
                colour=colour.lstrip("#"),
            )
            embed.set_image(thumbnail)
            embed.set_author(name=page_title.title())

            url = embed.generate_url(hide_url=False, shorten_url=False)

            if not url:
                raise Exception("URL generation failed")

            content = f"[Darky]({url}&v={random.randint(100000, 999999)})"

            if cfg.get("message_settings")["edit_og"]:
                msg = await ctx.message.edit(content=content, delete_after=delete_after)
            else:
                msg = await ctx.send(content, delete_after=delete_after)

            print(f"[EMBED DEBUG] Message sent successfully!")
            print(f"[EMBED DEBUG] === Embed generation complete ===\n")

        except Exception as e:
            print(f"[EMBED DEBUG] ERROR: {e}")
            content = str(
                Codeblock(
                    title="Embed Error",
                    description=str(e),
                    extra_title=title,
                    footer=footer,
                )
            )
            msg = await ctx.send(content, delete_after=delete_after)

            print(f"[EMBED DEBUG] Message sent successfully!")
            print(f"[EMBED DEBUG] === Embed generation complete ===\n")

        except Exception as e:
            print(f"[EMBED DEBUG] ERROR: {e}")
            print(f"[EMBED DEBUG] Falling back to codeblock...")

            content = str(
                Codeblock(
                    title="Embed Error",
                    description=str(e),
                    extra_title=title,
                    footer=footer,
                )
            )
            msg = await ctx.send(content, delete_after=delete_after)

    elif msg_style == "hookembed":
        webhook_url = cfg.get("rich_embed_webhook")
        if not webhook_url:
            return await send_error_message(
                ctx,
                "hookembed requires webhook. Use .connect <webhook_url>",
            )

        if title == theme.title:
            title = f"{theme.emoji} {title}"

        payload = {
            "embeds": [
                {
                    "title": title,
                    "description": description,
                    "color": int(colour.lstrip("#"), 16),
                    "footer": {"text": footer} if footer else None,
                    "thumbnail": {"url": thumbnail} if thumbnail else None,
                }
            ]
        }
        if payload["embeds"][0]["footer"] is None:
            del payload["embeds"][0]["footer"]
        if payload["embeds"][0]["thumbnail"] is None:
            del payload["embeds"][0]["thumbnail"]

        try:
            webhook_resp = requests.post(
                f"{webhook_url}?wait=true", json=payload, timeout=10
            )
            if webhook_resp.status_code not in (200, 204):
                raise Exception(f"Webhook send failed: {webhook_resp.status_code}")

            sent = webhook_resp.json()
            sent_id = sent["id"]
            sent_channel_id = sent["channel_id"]
            sent_guild_id = sent.get("guild_id")

            forward_resp = requests.post(
                f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
                headers={
                    "Authorization": cfg.get("token"),
                    "Content-Type": "application/json",
                },
                json={
                    "content": "",
                    "flags": 0,
                    "message_reference": {
                        "channel_id": sent_channel_id,
                        "guild_id": sent_guild_id,
                        "message_id": sent_id,
                        "type": 1,
                    },
                },
                timeout=10,
            )

            if forward_resp.status_code not in (200, 201):
                raise Exception(f"Forward failed: {forward_resp.status_code}")

            forwarded = forward_resp.json()
            forwarded_id = forwarded["id"]
            msg = await ctx.channel.fetch_message(int(forwarded_id))

            if delete_after is not None:
                await asyncio.sleep(delete_after)
                try:
                    requests.delete(
                        f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages/{forwarded_id}",
                        headers={"Authorization": cfg.get("token")},
                        timeout=10,
                    )
                except Exception:
                    pass
                try:
                    requests.delete(
                        f"{webhook_url}/messages/{sent_id}",
                        timeout=10,
                    )
                except Exception:
                    pass
        except Exception as e:
            msg = await ctx.send(f"hookembed error: {e}", delete_after=delete_after)

    elif msg_style == "image":
        clean_title = (
            title.replace(theme.emoji, "").strip() if theme.emoji in title else title
        )
        clean_title = re.sub(r"[^\w\s]", "", clean_title).strip()

        description = description.strip()

        embed = Embed(
            title=clean_title, description=description, colour=colour.lstrip("#")
        )
        embed.set_footer(text=footer)
        embed.set_thumbnail(thumbnail)

        embed_file = embed.save()

        msg = await ctx.send(
            file=discord.File(embed_file, filename=embed_file.split("/")[-1]),
            delete_after=delete_after,
        )
        os.remove(embed_file)

    if extra_message:
        extra_msg = await ctx.send(extra_message, delete_after=delete_after)
        try:
            if hasattr(ctx, "message") and delete_after is not None:
                await ctx.message.delete(delay=delete_after)
        except Exception:
            pass
        return msg, extra_msg

    try:
        if hasattr(ctx, "message") and delete_after is not None:
            await ctx.message.delete(delay=delete_after)
    except Exception:
        pass

    return msg


async def send_error_message(ctx, error_text):
    await send_message(
        ctx, {"title": "Error", "description": error_text, "colour": "#ff0000"}
    )


def split_into_pages(commands_list, max_length):
    pages = []
    current_page = ""
    for cmd in commands_list:
        if len(current_page) + len(cmd) > max_length:
            pages.append(current_page)
            current_page = ""
        current_page += f"{cmd}\n"
    if current_page:
        pages.append(current_page)
    return pages


def generate_help_pages(bot, cog_name):
    cog = bot.get_cog(cog_name)
    if not cog:
        return {"codeblock": [], "image": [], "embed": []}

    commands = cog.walk_commands()
    command_details = []
    max_name_length = 0

    for cmd in commands:
        if cmd.name.lower() != cog_name.lower():
            full_name = get_command_full_name(cmd)
            max_name_length = max(max_name_length, len(full_name))
            command_details.append((full_name, cmd.description or "No description"))

    formatted_commands = []
    formatted_commands_codeblock = []
    formatted_commands_embed = []

    for name, description in command_details:
        padded_name = name.ljust(max_name_length)
        if description.endswith("."):
            description = description[:-1]
        formatted_commands_codeblock.append(f"{padded_name} :: {description}")
        formatted_commands.append(f"**{name}** {description}")
        formatted_commands_embed.append(f"{bot.command_prefix}{name} :: {description}")

    codeblock_pages = split_into_pages(formatted_commands_codeblock, 1000)
    image_pages = split_into_pages(formatted_commands, 400)
    embed_pages = split_into_pages(formatted_commands_embed, 300)

    return {
        "codeblock": codeblock_pages,
        "image": image_pages,
        "embed": embed_pages,
        "hookembed": embed_pages,
    }
