#!/usr/bin/env python3
import os
import sys
import json
import time
import subprocess
import argparse
from pathlib import Path

CONFIG_DIR = Path.home() / ".discode"
BOTS_DIR = CONFIG_DIR / "bots"
COMMANDS_DIR = CONFIG_DIR / "commands"
CONFIG_FILE = CONFIG_DIR / "config.json"

def ensure_config():
    CONFIG_DIR.mkdir(exist_ok=True)
    BOTS_DIR.mkdir(exist_ok=True)
    COMMANDS_DIR.mkdir(exist_ok=True)
    if not CONFIG_FILE.exists():
        default_config = {"bots": {}, "commands": {}, "default_bot": None}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(default_config, f, indent=2)

def get_config():
    ensure_config()
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def check_dependencies():
    required = ['python3', 'pip']
    missing = []
    for dep in required:
        try:
            subprocess.run([dep, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except FileNotFoundError:
            missing.append(dep)
    try:
        import discord
    except ImportError:
        missing.append('discord.py')
    return missing

def install_dependencies():
    subprocess.run(['pip', 'install', '--upgrade', 'pip'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(['pip', 'install', 'discord.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def create_bot(bot_name, token, prefix="!"):
    config = get_config()
    if bot_name in config['bots']:
        print(f"Error: Bot '{bot_name}' already exists!")
        return False
    bot_config = {"token": token, "prefix": prefix, "commands": [], "status": "offline", "created_at": time.strftime("%Y-%m-%d %H:%M:%S")}
    config['bots'][bot_name] = bot_config
    if not config['default_bot']:
        config['default_bot'] = bot_name
    save_config(config)
    bot_dir = BOTS_DIR / bot_name
    bot_dir.mkdir(exist_ok=True)
    bot_file = bot_dir / f"{bot_name}.py"
    create_bot_file(bot_name, token, prefix, bot_file)
    print(f"Bot '{bot_name}' created!")
    return True

def create_bot_file(bot_name, token, prefix, bot_file):
    bot_code = f'''import discord
from discord.ext import commands

class {bot_name.capitalize()}Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="{prefix}", intents=discord.Intents.all())
    async def on_ready(self):
        print(f"Logged in as {{self.user}}")
        await self.change_presence(activity=discord.Game(name="{prefix}help"))

bot = {bot_name.capitalize()}Bot()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith("{prefix}"):
        cmd = message.content[len("{prefix}"):].split()[0].lower()
        try:
            import json
            from pathlib import Path
            config_dir = Path.home() / ".discode"
            config_file = config_dir / "config.json"
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                if "{bot_name}" in config["bots"]:
                    for cmd_data in config["bots"]["{bot_name}"]["commands"]:
                        if cmd_data["name"] == cmd:
                            await message.channel.send(cmd_data["response"])
                            return
        except:
            pass
    await bot.process_commands(message)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help", description="Commands:", color=discord.Color.blue())
    embed.add_field(name="{prefix}help", value="Show help", inline=False)
    embed.add_field(name="{prefix}ping", value="Check latency", inline=False)
    try:
        import json
        from pathlib import Path
        config_dir = Path.home() / ".discode"
        config_file = config_dir / "config.json"
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
            if "{bot_name}" in config["bots"]:
                for cmd_data in config["bots"]["{bot_name}"]["commands"]:
                    embed.add_field(name=f"{prefix}{{cmd_data['name']}}", value=cmd_data.get("description", "Custom"), inline=False)
    except:
        pass
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! {{latency}}ms")

if __name__ == "__main__":
    bot.run("{token}")
'''
    with open(bot_file, 'w') as f:
        f.write(bot_code)

def list_bots():
    config = get_config()
    if not config['bots']:
        print("No bots configured. Use 'discode create <name>'")
        return
    print("\nBots:")
    default_bot = config.get('default_bot', '')
    for name, bot_data in config['bots'].items():
        default_marker = " [DEFAULT]" if name == default_bot else ""
        print(f"  {name}{default_marker}")
        print(f"    Prefix: {bot_data['prefix']}")
        print(f"    Commands: {len(bot_data['commands'])}")

def delete_bot(bot_name):
    config = get_config()
    if bot_name not in config['bots']:
        print(f"Error: Bot '{bot_name}' not found!")
        return False
    bot_dir = BOTS_DIR / bot_name
    if bot_dir.exists():
        import shutil
        shutil.rmtree(bot_dir)
    del config['bots'][bot_name]
    if config['default_bot'] == bot_name:
        config['default_bot'] = None
    save_config(config)
    print(f"Bot '{bot_name}' deleted!")
    return True

def set_default_bot(bot_name):
    config = get_config()
    if bot_name not in config['bots']:
        print(f"Error: Bot '{bot_name}' not found!")
        return False
    config['default_bot'] = bot_name
    save_config(config)
    print(f"Default bot set to '{bot_name}'!")
    return True

def add_command(bot_name, cmd_name, response, description=""):
    config = get_config()
    if bot_name not in config['bots']:
        print(f"Error: Bot '{bot_name}' not found!")
        return False
    bot_config = config['bots'][bot_name]
    for cmd in bot_config['commands']:
        if cmd['name'] == cmd_name:
            print(f"Error: Command '{cmd_name}' already exists!")
            return False
    bot_config['commands'].append({"name": cmd_name, "response": response, "description": description})
    save_config(config)
    print(f"Command '{cmd_name}' added!")
    return True

def list_commands(bot_name):
    config = get_config()
    if bot_name not in config['bots']:
        print(f"Error: Bot '{bot_name}' not found!")
        return
    bot_config = config['bots'][bot_name]
    commands = bot_config['commands']
    if not commands:
        print(f"No commands for bot '{bot_name}'")
        return
    print(f"\nCommands for '{bot_name}':")
    for cmd in commands:
        print(f"  {cmd['name']}: {cmd.get('description', 'N/A')}")
        print(f"    -> {cmd['response']}")

def delete_command(bot_name, cmd_name):
    config = get_config()
    if bot_name not in config['bots']:
        print(f"Error: Bot '{bot_name}' not found!")
        return False
    bot_config = config['bots'][bot_name]
    for i, cmd in enumerate(bot_config['commands']):
        if cmd['name'] == cmd_name:
            del bot_config['commands'][i]
            save_config(config)
            print(f"Command '{cmd_name}' deleted!")
            return True
    print(f"Error: Command '{cmd_name}' not found!")
    return False

def create_plugin(plugin_name):
    plugin_file = COMMANDS_DIR / f"{plugin_name}.py"
    if plugin_file.exists():
        print(f"Error: Plugin '{plugin_name}' already exists!")
        return False
    plugin_code = f'''import discord
from discord.ext import commands

class {plugin_name.capitalize()}(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog({plugin_name.capitalize()}(bot))
'''
    with open(plugin_file, 'w') as f:
        f.write(plugin_code)
    print(f"Plugin '{plugin_name}' created at: {plugin_file}")
    return True

def list_plugins():
    plugins = list(COMMANDS_DIR.glob("*.py"))
    if not plugins:
        print("No plugins found. Use 'discode plugin create <name>'")
        return
    print("\nPlugins:")
    for plugin_file in plugins:
        if plugin_file.name != "__init__.py":
            print(f"  {plugin_file.stem}")

def start_bot(bot_name):
    config = get_config()
    if bot_name not in config['bots']:
        print(f"Error: Bot '{bot_name}' not found!")
        return False
    bot_dir = BOTS_DIR / bot_name
    bot_file = bot_dir / f"{bot_name}.py"
    if not bot_file.exists():
        print(f"Error: Bot file not found!")
        return False
    print(f"Starting bot '{bot_name}'... (Ctrl+C to stop)")
    os.chdir(bot_dir)
    try:
        subprocess.run(['python3', bot_file.name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False
    except KeyboardInterrupt:
        print("\nBot stopped")
    return True

def generate_token_guide():
    print("\nHow to Get Discord Bot Token:")
    print("1. Go to https://discord.com/developers/applications")
    print("2. New Application > name it")
    print("3. Go to Bot tab > Add Bot")
    print("4. Copy the Token")
    print("5. Use it with: discode create <name> --token YOUR_TOKEN")

def main():
    parser = argparse.ArgumentParser(description='Discode - Discord Bot Manager')
    subparsers = parser.add_subparsers(dest='command')

    create_parser = subparsers.add_parser('create', help='Create bot')
    create_parser.add_argument('name')
    create_parser.add_argument('--token')
    create_parser.add_argument('--prefix', default='!')

    subparsers.add_parser('list', help='List bots')

    delete_parser = subparsers.add_parser('delete', help='Delete bot')
    delete_parser.add_argument('name')

    default_parser = subparsers.add_parser('default', help='Set default bot')
    default_parser.add_argument('name')

    start_parser = subparsers.add_parser('start', help='Start bot')
    start_parser.add_argument('name', nargs='?')

    add_cmd_parser = subparsers.add_parser('add-cmd', help='Add command')
    add_cmd_parser.add_argument('bot')
    add_cmd_parser.add_argument('name')
    add_cmd_parser.add_argument('response')
    add_cmd_parser.add_argument('--desc', default='')

    list_cmd_parser = subparsers.add_parser('list-cmd', help='List commands')
    list_cmd_parser.add_argument('bot')

    del_cmd_parser = subparsers.add_parser('del-cmd', help='Delete command')
    del_cmd_parser.add_argument('bot')
    del_cmd_parser.add_argument('name')

    plugin_parser = subparsers.add_parser('plugin', help='Plugin commands')
    plugin_subparsers = plugin_parser.add_subparsers(dest='plugin_command')
    create_plugin_parser = plugin_subparsers.add_parser('create', help='Create plugin')
    create_plugin_parser.add_argument('name')
    plugin_subparsers.add_parser('list', help='List plugins')

    subparsers.add_parser('token-guide', help='Token guide')

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    ensure_config()
    missing = check_dependencies()
    if missing:
        print(f"Missing: {', '.join(missing)}")
        install = input("Install? (y/N): ").strip().lower()
        if install == 'y':
            install_dependencies()
        else:
            print("Install manually: pkg install python && pip install discord.py")
            sys.exit(1)

    try:
        if args.command == 'create':
            token = args.token or input("Token: ").strip()
            if not token:
                print("Error: Token required!")
                sys.exit(1)
            create_bot(args.name, token, args.prefix)
        elif args.command == 'list':
            list_bots()
        elif args.command == 'delete':
            if input(f"Delete '{args.name}'? (y/N): ").strip().lower() == 'y':
                delete_bot(args.name)
        elif args.command == 'default':
            set_default_bot(args.name)
        elif args.command == 'start':
            bot_name = args.name or get_config().get('default_bot')
            if not bot_name:
                print("Error: No default bot! Use 'discode create' first")
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
        elif args.command == 'token-guide':
            generate_token_guide()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
