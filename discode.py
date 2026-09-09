#!/usr/bin/env python3
"""
Discode - Termux CLI for Discord Bot Management
A simple command-line tool to create and manage Discord bots with custom commands.
"""

import os
import sys
import json
import time
import subprocess
import argparse
from pathlib import Path

# Colors for Termux
class Colors:
    RESET = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BOLD = '\033[1m'

CONFIG_DIR = Path.home() / ".discode"
BOTS_DIR = CONFIG_DIR / "bots"
COMMANDS_DIR = CONFIG_DIR / "commands"
CONFIG_FILE = CONFIG_DIR / "config.json"


def print_header():
    """Print Discode header"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}")
    print("  ██████╗ ██╗██████╗ ██████╗ ███████╗    ██████╗ ██████╗ ██████╗ ███████╗")
    print("  ██╔══██╗██║██╔══██╗██╔══██╗██╔════╝    ██╔══██╗██╔══██╗██╔══██╗██╔════╝")
    print("  ██████╔╝██║██████╔╝██████╔╝█████╗      ██║  ██║██████╔╝██████╔╝█████╗  ")
    print("  ██╔═══╝ ██║██╔══██╗██╔══██╗██╔══╝      ██║  ██║██╔══██╗██╔══██╗██╔══╝  ")
    print("  ██║     ██║██║  ██║██║  ██║███████╗    ██████╔╝██║  ██║██║  ██║███████╗")
    print("  ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝")
    print(f"{Colors.RESET}")
    print(f"{Colors.YELLOW}  Termux Discord Bot Manager{Colors.RESET}\n")


def ensure_config():
    """Create config directories if they don't exist"""
    CONFIG_DIR.mkdir(exist_ok=True)
    BOTS_DIR.mkdir(exist_ok=True)
    COMMANDS_DIR.mkdir(exist_ok=True)
    
    if not CONFIG_FILE.exists():
        default_config = {
            "bots": {},
            "commands": {},
            "default_bot": None
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(default_config, f, indent=2)


def get_config():
    """Load configuration"""
    ensure_config()
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)


def save_config(config):
    """Save configuration"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def check_dependencies():
    """Check if required dependencies are installed"""
    required = ['python3', 'pip']
    missing = []
    
    for dep in required:
        try:
            subprocess.run([dep, '--version'], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
        except FileNotFoundError:
            missing.append(dep)
    
    # Check for discord.py
    try:
        import discord
    except ImportError:
        missing.append('discord.py')
    
    return missing


def install_dependencies():
    """Install required Python packages"""
    print(f"{Colors.YELLOW}Installing dependencies...{Colors.RESET}")
    
    # Update pip
    subprocess.run(['pip', 'install', '--upgrade', 'pip'], 
                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Install discord.py
    subprocess.run(['pip', 'install', 'discord.py'], 
                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print(f"{Colors.GREEN}Dependencies installed!{Colors.RESET}")


def create_bot(bot_name, token, prefix="!"):
    """Create a new Discord bot configuration"""
    config = get_config()
    
    if bot_name in config['bots']:
        print(f"{Colors.RED}Error: Bot '{bot_name}' already exists!{Colors.RESET}")
        return False
    
    bot_config = {
        "token": token,
        "prefix": prefix,
        "commands": [],
        "status": "offline",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    config['bots'][bot_name] = bot_config
    
    if not config['default_bot']:
        config['default_bot'] = bot_name
    
    save_config(config)
    
    # Create bot directory
    bot_dir = BOTS_DIR / bot_name
    bot_dir.mkdir(exist_ok=True)
    
    # Create bot file
    bot_file = bot_dir / f"{bot_name}.py"
    create_bot_file(bot_name, token, prefix, bot_file)
    
    print(f"{Colors.GREEN}Bot '{bot_name}' created successfully!{Colors.RESET}")
    return True


def create_bot_file(bot_name, token, prefix, bot_file):
    """Generate the bot Python file"""
    bot_code = f'''import discord
import asyncio
from discord.ext import commands

class {bot_name.capitalize()}Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="{prefix}",
            intents=discord.Intents.all()
        )
    
    async def setup_hook(self):
        print("Bot is starting...")
    
    async def on_ready(self):
        print(f"Logged in as {{self.user}} (ID: {{self.user.id}})")
        print(f"Prefix: {prefix}")
        print("------")
        await self.change_presence(activity=discord.Game(name="{prefix}help"))

bot = {bot_name.capitalize()}Bot()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Handle commands
    if message.content.startswith("{prefix}"):
        cmd = message.content[len("{prefix}"):].split()[0].lower()
        args = message.content[len("{prefix}") + len(cmd):].strip()
        
        # Load custom commands
        try:
            import json
            from pathlib import Path
            config_dir = Path.home() / ".discode"
            config_file = config_dir / "config.json"
            
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                
                if "{bot_name}" in config["bots"]:
                    custom_commands = config["bots"]["{bot_name}"]["commands"]
                    
                    for cmd_data in custom_commands:
                        if cmd_data["name"] == cmd:
                            await message.channel.send(cmd_data["response"])
                            return
        except Exception as e:
            print(f"Error loading custom commands: {{e}}")
    
    await bot.process_commands(message)

@bot.command()
async def help(ctx):
    """Show help message"""
    embed = discord.Embed(
        title="{bot_name.capitalize()} Bot Help",
        description="Available commands:",
        color=discord.Color.blue()
    )
    embed.add_field(name="{prefix}help", value="Show this help message", inline=False)
    embed.add_field(name="{prefix}ping", value="Check bot latency", inline=False)
    
    # Add custom commands to help
    try:
        import json
        from pathlib import Path
        config_dir = Path.home() / ".discode"
        config_file = config_dir / "config.json"
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            if "{bot_name}" in config["bots"]:
                custom_commands = config["bots"]["{bot_name}"]["commands"]
                
                for cmd_data in custom_commands:
                    embed.add_field(
                        name=f"{prefix}{{cmd_data['name']}}",
                        value=cmd_data.get("description", "Custom command"),
                        inline=False
                    )
    except Exception as e:
        print(f"Error loading custom commands for help: {{e}}")
    
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    """Check bot latency"""
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! {{latency}}ms")

# Load cogs/commands from plugins directory
plugins_dir = Path("{{Path(__file__).parent}}/plugins")
if plugins_dir.exists():
    for plugin_file in plugins_dir.glob("*.py"):
        if plugin_file.name != "__init__.py":
            try:
                bot.load_extension(f"plugins.{{plugin_file.stem}}")
                print(f"Loaded plugin: {{plugin_file.stem}}")
            except Exception as e:
                print(f"Failed to load plugin {{plugin_file.stem}}: {{e}}")

if __name__ == "__main__":
    bot.run("{token}")
'''
    
    with open(bot_file, 'w') as f:
        f.write(bot_code)
    
    print(f"{Colors.GREEN}Bot file created: {bot_file}{Colors.RESET}")


def list_bots():
    """List all configured bots"""
    config = get_config()
    
    if not config['bots']:
        print(f"{Colors.YELLOW}No bots configured yet.{Colors.RESET}")
        print(f"{Colors.CYAN}Use 'discode create' to create a new bot.{Colors.RESET}")
        return
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}Configured Bots:{Colors.RESET}\n")
    
    default_bot = config.get('default_bot', '')
    
    for name, bot_data in config['bots'].items():
        status_color = Colors.GREEN if bot_data['status'] == 'online' else Colors.RED
        default_marker = f"{Colors.YELLOW} [DEFAULT]{Colors.RESET}" if name == default_bot else ""
        
        print(f"{Colors.BOLD}{name}{Colors.RESET}{default_marker}")
        print(f"  Token: {'*' * len(bot_data['token'])}")
        print(f"  Prefix: {Colors.CYAN}{bot_data['prefix']}{Colors.RESET}")
        print(f"  Status: {status_color}{bot_data['status']}{Colors.RESET}")
        print(f"  Commands: {len(bot_data['commands'])}")
        print(f"  Created: {bot_data['created_at']}")
        print()


def delete_bot(bot_name):
    """Delete a bot configuration"""
    config = get_config()
    
    if bot_name not in config['bots']:
        print(f"{Colors.RED}Error: Bot '{bot_name}' not found!{Colors.RESET}")
        return False
    
    # Remove bot directory
    bot_dir = BOTS_DIR / bot_name
    if bot_dir.exists():
        import shutil
        shutil.rmtree(bot_dir)
    
    del config['bots'][bot_name]
    
    if config['default_bot'] == bot_name:
        config['default_bot'] = None
    
    save_config(config)
    print(f"{Colors.GREEN}Bot '{bot_name}' deleted successfully!{Colors.RESET}")
    return True


def set_default_bot(bot_name):
    """Set a bot as default"""
    config = get_config()
    
    if bot_name not in config['bots']:
        print(f"{Colors.RED}Error: Bot '{bot_name}' not found!{Colors.RESET}")
        return False
    
    config['default_bot'] = bot_name
    save_config(config)
    print(f"{Colors.GREEN}Default bot set to '{bot_name}'!{Colors.RESET}")
    return True


def add_command(bot_name, cmd_name, response, description=""):
    """Add a custom command to a bot"""
    config = get_config()
    
    if bot_name not in config['bots']:
        print(f"{Colors.RED}Error: Bot '{bot_name}' not found!{Colors.RESET}")
        return False
    
    bot_config = config['bots'][bot_name]
    
    # Check if command already exists
    for cmd in bot_config['commands']:
        if cmd['name'] == cmd_name:
            print(f"{Colors.RED}Error: Command '{cmd_name}' already exists!{Colors.RESET}")
            return False
    
    new_command = {
        "name": cmd_name,
        "response": response,
        "description": description
    }
    
    bot_config['commands'].append(new_command)
    save_config(config)
    
    print(f"{Colors.GREEN}Command '{cmd_name}' added to bot '{bot_name}'!{Colors.RESET}")
    return True


def list_commands(bot_name):
    """List all commands for a bot"""
    config = get_config()
    
    if bot_name not in config['bots']:
        print(f"{Colors.RED}Error: Bot '{bot_name}' not found!{Colors.RESET}")
        return
    
    bot_config = config['bots'][bot_name]
    commands = bot_config['commands']
    
    if not commands:
        print(f"{Colors.YELLOW}No custom commands for bot '{bot_name}'.{Colors.RESET}")
        return
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}Custom Commands for '{bot_name}':{Colors.RESET}\n")
    
    for cmd in commands:
        print(f"{Colors.BOLD}{cmd['name']}{Colors.RESET}")
        print(f"  Description: {cmd.get('description', 'N/A')}")
        print(f"  Response: {cmd['response']}")
        print()


def delete_command(bot_name, cmd_name):
    """Delete a custom command from a bot"""
    config = get_config()
    
    if bot_name not in config['bots']:
        print(f"{Colors.RED}Error: Bot '{bot_name}' not found!{Colors.RESET}")
        return False
    
    bot_config = config['bots'][bot_name]
    
    for i, cmd in enumerate(bot_config['commands']):
        if cmd['name'] == cmd_name:
            del bot_config['commands'][i]
            save_config(config)
            print(f"{Colors.GREEN}Command '{cmd_name}' deleted from bot '{bot_name}'!{Colors.RESET}")
            return True
    
    print(f"{Colors.RED}Error: Command '{cmd_name}' not found!{Colors.RESET}")
    return False


def create_plugin(plugin_name):
    """Create a new plugin file"""
    plugin_file = COMMANDS_DIR / f"{plugin_name}.py"
    
    if plugin_file.exists():
        print(f"{Colors.RED}Error: Plugin '{plugin_name}' already exists!{Colors.RESET}")
        return False
    
    plugin_code = f'''"""
{plugin_name.capitalize()} Plugin for Discode
Custom commands and functionality for Discord bots
"""

import discord
from discord.ext import commands

class {plugin_name.capitalize()}(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{plugin_name.capitalize()} plugin loaded!")
    
    # Add your custom commands here
    # Example:
    # @commands.command()
    # async def hello(self, ctx):
    #     await ctx.send("Hello from {plugin_name} plugin!")

async def setup(bot):
    await bot.add_cog({plugin_name.capitalize()}(bot))
'''
    
    with open(plugin_file, 'w') as f:
        f.write(plugin_code)
    
    print(f"{Colors.GREEN}Plugin '{plugin_name}' created at: {plugin_file}{Colors.RESET}")
    print(f"{Colors.YELLOW}Edit the file to add custom commands!{Colors.RESET}")
    return True


def list_plugins():
    """List all available plugins"""
    plugins = list(COMMANDS_DIR.glob("*.py"))
    
    if not plugins:
        print(f"{Colors.YELLOW}No plugins found.{Colors.RESET}")
        print(f"{Colors.CYAN}Use 'discode plugin create' to create a new plugin.{Colors.RESET}")
        return
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}Available Plugins:{Colors.RESET}\n")
    
    for plugin_file in plugins:
        if plugin_file.name != "__init__.py":
            print(f"{Colors.BOLD}{plugin_file.stem}{Colors.RESET}")
            print(f"  File: {plugin_file}")
            print()


def start_bot(bot_name):
    """Start a Discord bot"""
    config = get_config()
    
    if bot_name not in config['bots']:
        print(f"{Colors.RED}Error: Bot '{bot_name}' not found!{Colors.RESET}")
        return False
    
    bot_dir = BOTS_DIR / bot_name
    bot_file = bot_dir / f"{bot_name}.py"
    
    if not bot_file.exists():
        print(f"{Colors.RED}Error: Bot file not found!{Colors.RESET}")
        return False
    
    print(f"{Colors.GREEN}Starting bot '{bot_name}'...{Colors.RESET}")
    print(f"{Colors.YELLOW}Press Ctrl+C to stop the bot.{Colors.RESET}\n")
    
    # Change to bot directory and run
    os.chdir(bot_dir)
    
    try:
        subprocess.run(['python3', bot_file.name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Error starting bot: {e}{Colors.RESET}")
        return False
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Bot stopped by user.{Colors.RESET}")
    
    return True


def generate_token_guide():
    """Show guide for getting Discord bot token"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}How to Get a Discord Bot Token:{Colors.RESET}\n")
    print("1. Go to https://discord.com/developers/applications")
    print("2. Click on 'New Application' and give it a name")
    print("3. Go to the 'Bot' tab")
    print("4. Click 'Add Bot' and confirm")
    print("5. Under 'Token', click 'Copy' to copy your bot token")
    print(f"\n{Colors.YELLOW}IMPORTANT: Keep your token secret! Never share it!{Colors.RESET}")
    print(f"{Colors.CYAN}Use the token when creating a bot with 'discode create'{Colors.RESET}\n")


def main():
    """Main entry point"""
    print_header()
    
    # Check and install dependencies
    missing = check_dependencies()
    if missing:
        print(f"{Colors.YELLOW}Missing dependencies: {', '.join(missing)}{Colors.RESET}")
        install = input(f"{Colors.YELLOW}Install automatically? (y/N): {Colors.RESET}").strip().lower()
        if install == 'y':
            install_dependencies()
        else:
            print(f"{Colors.RED}Please install dependencies manually.{Colors.RESET}")
            print(f"{Colors.CYAN}Run: pkg install python && pip install discord.py{Colors.RESET}")
            sys.exit(1)
    
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Discode - Termux Discord Bot Manager',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create bot
    create_parser = subparsers.add_parser('create', help='Create a new Discord bot')
    create_parser.add_argument('name', help='Name of the bot')
    create_parser.add_argument('--token', help='Discord bot token')
    create_parser.add_argument('--prefix', default='!', help='Command prefix (default: !)')
    
    # List bots
    subparsers.add_parser('list', help='List all configured bots')
    
    # Delete bot
    delete_parser = subparsers.add_parser('delete', help='Delete a bot')
    delete_parser.add_argument('name', help='Name of the bot to delete')
    
    # Set default bot
    default_parser = subparsers.add_parser('default', help='Set default bot')
    default_parser.add_argument('name', help='Name of the bot to set as default')
    
    # Start bot
    start_parser = subparsers.add_parser('start', help='Start a Discord bot')
    start_parser.add_argument('name', nargs='?', help='Name of the bot to start (default: default bot)')
    
    # Add command
    add_cmd_parser = subparsers.add_parser('add-cmd', help='Add a custom command to a bot')
    add_cmd_parser.add_argument('bot', help='Name of the bot')
    add_cmd_parser.add_argument('name', help='Name of the command')
    add_cmd_parser.add_argument('response', help='Response for the command')
    add_cmd_parser.add_argument('--desc', default='', help='Description of the command')
    
    # List commands
    list_cmd_parser = subparsers.add_parser('list-cmd', help='List custom commands for a bot')
    list_cmd_parser.add_argument('bot', help='Name of the bot')
    
    # Delete command
    del_cmd_parser = subparsers.add_parser('del-cmd', help='Delete a custom command')
    del_cmd_parser.add_argument('bot', help='Name of the bot')
    del_cmd_parser.add_argument('name', help='Name of the command to delete')
    
    # Plugin commands
    plugin_parser = subparsers.add_parser('plugin', help='Manage plugins')
    plugin_subparsers = plugin_parser.add_subparsers(dest='plugin_command')
    
    create_plugin_parser = plugin_subparsers.add_parser('create', help='Create a new plugin')
    create_plugin_parser.add_argument('name', help='Name of the plugin')
    
    plugin_subparsers.add_parser('list', help='List all plugins')
    
    # Token guide
    subparsers.add_parser('token-guide', help='Show how to get a Discord bot token')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    ensure_config()
    
    try:
        if args.command == 'create':
            if not args.token:
                print(f"{Colors.YELLOW}Enter Discord bot token (or use --token flag):{Colors.RESET}")
                token = input("Token: ").strip()
            else:
                token = args.token
            
            if not token:
                print(f"{Colors.RED}Error: Token is required!{Colors.RESET}")
                sys.exit(1)
            
            create_bot(args.name, token, args.prefix)
        
        elif args.command == 'list':
            list_bots()
        
        elif args.command == 'delete':
            confirm = input(f"{Colors.RED}Are you sure you want to delete bot '{args.name}'? (y/N): {Colors.RESET}").strip().lower()
            if confirm == 'y':
                delete_bot(args.name)
            else:
                print(f"{Colors.YELLOW}Deletion cancelled.{Colors.RESET}")
        
        elif args.command == 'default':
            set_default_bot(args.name)
        
        elif args.command == 'start':
            bot_name = args.name or get_config().get('default_bot')
            if not bot_name:
                print(f"{Colors.RED}Error: No default bot set!{Colors.RESET}")
                print(f"{Colors.CYAN}Use 'discode create' or 'discode default' first.{Colors.RESET}")
                sys.exit(1)
            start_bot(bot_name)
        
        elif args.command == 'add-cmd':
            add_command(args.bot, args.name, args.response, args.desc)
        
        elif args.command == 'list-cmd':
            list_commands(args.bot)
        
        elif args.command == 'del-cmd':
            delete_command(args.bot, args.name)
        
        elif args.command == 'plugin':
            if args.plugin_command == 'create':
                create_plugin(args.name)
            elif args.plugin_command == 'list':
                list_plugins()
            else:
                plugin_parser.print_help()
        
        elif args.command == 'token-guide':
            generate_token_guide()
        
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
