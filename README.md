# Discode

**Termux Discord Bot Manager**

A powerful CLI tool for creating and managing Discord bots directly from Termux on Android. Build, customize, and deploy Discord bots with ease!

## Features

- Create and manage multiple Discord bots
- Add custom commands to your bots
- Plugin system for extending functionality
- Built-in command management
- Easy token management
- Colorful Termux-optimized interface

## Installation

### Quick Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/SonicZ-z/Discode.git
cd Discode

# Make setup script executable
chmod +x setup.sh

# Run the setup
./setup.sh
```

The setup script will:
1. Install Python and pip (if not already installed)
2. Install discord.py library
3. Install the Discode CLI
4. Create necessary directories
5. Set up command aliases

### Manual Installation

```bash
# Install dependencies
pkg update && pkg upgrade
pkg install python -y
pip install discord.py

# Install Discode
mkdir -p ~/.discode/bots ~/.discode/commands
cp discode.py $PREFIX/bin/discode
chmod +x $PREFIX/bin/discode

# Add to PATH (add to ~/.bashrc)
echo 'export PATH=$PATH:~/.discode' >> ~/.bashrc
source ~/.bashrc
```

## Usage

### Getting Started

First, you need a Discord bot token. Run:
```bash
discode token-guide
```

This will show you how to create a Discord bot and get its token.

### Creating a Bot

```bash
# Create a new bot with token
discode create mybot --token YOUR_BOT_TOKEN_HERE

# Or create and enter token interactively
discode create mybot
# You'll be prompted to enter the token

# Create with custom prefix
discode create mybot --token YOUR_TOKEN --prefix $ 
```

### Managing Bots

```bash
# List all configured bots
discode list

# Set a bot as default
discode default mybot

# Delete a bot
discode delete mybot
```

### Adding Custom Commands

```bash
# Add a custom command to a bot
discode add-cmd mybot hello "Hello! Welcome to the server!"

# Add command with description
discode add-cmd mybot rules "Server rules: 1. Be nice 2. No spam" --desc "Show server rules"

# List all commands for a bot
discode list-cmd mybot

# Delete a command
discode del-cmd mybot hello
```

### Starting Your Bot

```bash
# Start a specific bot
discode start mybot

# Start the default bot
discode start
```

### Plugin System

Create custom plugins to extend your bot's functionality:

```bash
# Create a new plugin
discode plugin create myplugin

# List all plugins
discode plugin list
```

After creating a plugin, edit the file at `~/.discode/commands/myplugin.py` and add your custom commands.

### Plugin Example

Edit your plugin file and add commands:

```python
"""
MyPlugin Plugin for Discode
Custom commands for Discord bots
"""

import discord
from discord.ext import commands

class Myplugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f"Hello {ctx.author.mention}! Welcome!")
    
    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(
            title="Server Info",
            description=f"Server: {ctx.guild.name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Members", value=ctx.guild.member_count)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Myplugin(bot))
```

Then place the plugin file in your bot's `plugins` directory.

## Command Reference

### Main Commands

| Command | Description |
|---------|-------------|
| `discode create <name>` | Create a new Discord bot |
| `discode list` | List all configured bots |
| `discode delete <name>` | Delete a bot |
| `discode default <name>` | Set default bot |
| `discode start [name]` | Start a bot |
| `discode token-guide` | Show how to get a bot token |

### Command Management

| Command | Description |
|---------|-------------|
| `discode add-cmd <bot> <name> <response>` | Add custom command |
| `discode list-cmd <bot>` | List bot commands |
| `discode del-cmd <bot> <name>` | Delete a command |

### Plugin Management

| Command | Description |
|---------|-------------|
| `discode plugin create <name>` | Create a new plugin |
| `discode plugin list` | List all plugins |

## Bot Commands

Once your bot is running, it will respond to these commands:

- `!help` - Show help message with all available commands
- `!ping` - Check bot latency
- Any custom commands you've added

## Directory Structure

```
~/.discode/
├── config.json          # Main configuration file
├── bots/                # Bot files and directories
│   └── mybot/           # Individual bot directory
│       ├── mybot.py     # Bot source file
│       └── plugins/     # Bot-specific plugins
└── commands/            # Global plugins
    └── myplugin.py      # Plugin files
```

## Troubleshooting

### "discode: command not found"

Make sure the script is in your PATH:
```bash
# Check if it's installed
ls $PREFIX/bin/discode

# If not, install it
cp discode.py $PREFIX/bin/discode
chmod +x $PREFIX/bin/discode
```

### ModuleNotFoundError: discord

Install discord.py:
```bash
pip install discord.py
```

### Python not found

Install Python:
```bash
pkg install python -y
```

## Updating

To update Discode:

```bash
cd Discode
git pull origin main
cp discode.py $PREFIX/bin/discode
chmod +x $PREFIX/bin/discode
```

## Contributing

Feel free to contribute by:
- Reporting bugs
- Suggesting features
- Submitting pull requests

## License

MIT License - see LICENSE file for details.

## Support

For help and support:
- Check the built-in help: `discode --help`
- Run `discode token-guide` for token assistance
- Create an issue on GitHub

---

**Happy bot building!**

*Made for Termux users who want to create Discord bots on their Android devices.*
