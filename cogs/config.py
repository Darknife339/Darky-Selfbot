import discord
from discord.ext import commands
import json
import os


class Config:
    def __init__(self):
        self.config_file = "config.json"
        self.load()

    def load(self):
        if not os.path.exists(self.config_file):
            self.create_default()
        with open(self.config_file, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def create_default(self):
        default = {
            "token": "YOUR_TOKEN_HERE",
            "prefix": ".",
            "message_settings": {
                "style": "image",
                "auto_delete_delay": 10,
                "edit_og": False,
            },
            "theme": {
                "title": "Darky selfbot",
                "emoji": "🌑",
                "colour": "#8B5CF6",
                "footer": "Darky v1.0",
                "image": "https://raw.githubusercontent.com/Darknife339/just-pictures/refs/heads/main/DeWatermark.ai_1761290696876.jpeg",
            },
            "apis": {"serpapi": ""},
            "rich_embed_webhook": "",
            "message_logger_webhook": "",
            "message_logger_enabled": False,
            "message_logger_only_added": False,
            "message_logger_allowed_channels": [],
            "message_logger_allowed_guilds": [],
            "message_logger_blocked_channels": [],
            "nitro_sniper_webhook": "",
            "nitro_sniper_enabled": False,
        }
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=4)
        self.data = default

    def save(self):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    @property
    def theme(self):
        class Theme:
            def __init__(self, data):
                self.title = data["theme"]["title"]
                self.emoji = data["theme"]["emoji"]
                self.colour = data["theme"]["colour"]
                self.footer = data["theme"]["footer"]
                self.image = data["theme"]["image"]

        return Theme(self.data)
