# Darky Selfbot

A Discord selfbot with text animations, utilities, and customization options.

## Warning

This project not fully completed

## What it does

- Text animations (glitch, typewriter, falling text, etc.)
- Image commands (cats, dogs, Minecraft achievements, fake Discord messages)
- Fun commands (coin flip, 8ball, slots, memes, jokes)
- Text manipulation (ASCII art, case changing, regional letters)
- Custom embeds and codeblocks
- Status and RPC management
- Message logger (tracks deleted/edited messages)
- Nitro sniper support (optional webhook)

## Requirements

- Python 3.10+
- A Discord account
- Your Discord token

## Installation

```bash
git clone https://github.com/yourusername/darky-selfbot.git
cd darky-selfbot
pip install -r requirements.txt
python main.py
```

Or just run `setup.py` which installs dependencies and starts the bot.

## Configuration

Edit `config.json` with your settings:

```json
{
    "token": "YOUR_TOKEN_HERE",
    "prefix": ".",
    "message_settings": {
        "style": "hookembed",
        "auto_delete_delay": 100,
        "edit_og": false
    },
    "theme": {
        "title": "Darky selfbot",
        "emoji": "🌑",
        "colour": "#8B5CF6",
        "footer": "Darky v1.0"
    }
}
```

## Commands

Prefix is `.` by default.

### Animations
```
.animate [text]        - Letter by letter
.animatebold [text]    - Bold letters
.typewriter [text]     - Typewriter effect
.glitch [text]         - Glitch effect
.textfall [text]       - Falling text
.autoanim [mode]       - Auto animate next messages
.stop                  - Stop running animation
```

### Images
```
.cat                   - Random cat picture
.dog                   - Random dog picture
.bird                  - Random bird picture
.fox                   - Random fox picture
.achievement [icon] [text] - Minecraft achievement
.discordmessage [user] [text] - Fake Discord message
```

### Fun
```
.coinflip              - Flip a coin
.8ball [question]      - Magic 8ball
.dice [sides]          - Roll a dice
.dadjoke               - Dad joke
.catfact               - Cat fact
.meme                  - Random meme
.slots                 - Slot machine
.kanye                 - Kanye quote
```

### Text
```
.shrug                 - ¯\_(ツ)_/¯
.tableflip             - (╯°□°)╯︵ ┻━┻
.unflip                - Put table back
.ascii [text]          - ASCII art
.aesthetic [text]      - Aesthetic text
.regional [text]       - Regional indicator emojis
.cembed [title] [desc] - Custom embed
.codeblock [lang] [code] - Code block
```

### Settings
```
.settings              - View settings
.setstyle [style]      - Change message style
.setcolour [#hex]      - Set embed color
.setfooter [text]      - Set footer text
.settitle [text]       - Set title text
.setemoji [emoji]      - Set emoji
.connect [webhook]     - Bind webhook (hookembed/logger/sniper)
.reloadconfig          - Reload config
```

### Utility
```
.rpc show              - Show current RPC
.rpc playing [text]    - Set playing status
.rpc listen [text]     - Set listening status
.nowplaying            - Show current song (auto-updates)
.msglog on/off         - Toggle message logger
.msglog addchannel [id] - Add channel to logger
```

## Message Styles

You can change how messages appear:

- `codeblock` - ANSI colored codeblocks
- `embed` - Discord embeds via API
- `hookembed` - Embeds via webhook
- `imageembed` - PNG images with embeds

Use `.setstyle [name]` to change.

## Project Structure

```
darky-selfbot/
├── main.py              # Entry point
├── config.json          # Configuration
├── requirements.txt     # Dependencies
├── setup.py            # Installer script
├── cogs/               # Command modules
│   ├── animations.py
│   ├── fun.py
│   ├── img.py
│   ├── text.py
│   ├── settings.py
│   ├── utility.py
└── └── legit.py
```

## Dependencies

```
discord.py-self
art
requests
Pillow
faker
keyboard
git+https://github.com/ghostselfbot/discord.py-self_embed.git
```

## Troubleshooting

**Login failed** - Check your token is correct

**Module not found** - Run `pip install -r requirements.txt`

**Nowplaying not working** - Requires Windows and working media session

## License

MIT License

## Disclaimer

This is for educational purposes. I'm not responsible if you get banned or anything bad happens. Selfbots are against Discord ToS and can get your account terminated. You've been warned.
