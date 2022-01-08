import discord
from discord.ext import commands
import os  # For cog loading
import asyncpg  # For database
import json
import console_interaction

# Process of adding new commands:
# 1. Create in cog
# 2. Document in utility.py
# 3. Document aliases in utility.py alias command
# Can alternatively go by discord.py's built-in commands for description/aliases/etc.


intents = discord.Intents.default()  # For API permissions
intents.members = True
intents.dm_messages = False
bot = commands.Bot(command_prefix='.', case_insensitive=True, intents=intents, help_command=None)

with open('pg_config.json') as file:
    pg_config = json.load(file)


async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(database=pg_config['database'], user=pg_config['user'],
                                           password=pg_config['password'])


#@bot.check
#async def require_manage_guild(ctx):  # All commands require Manage Server permission
#    if not ctx.author.guild_permissions.manage_guild:
#        raise commands.MissingPermissions(['manage_guild'])
#    else:
#        return True


@bot.command()
@commands.is_owner()  # Owner-only command
async def load(ctx, extension):  # Loads an extensions; input is file name without file extension
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'Loaded {extension}')


@bot.command()
@commands.is_owner()  # Owner-only command
async def unload(ctx, extension):  # Unloads an extension; input is file name without file extension
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Unloaded {extension}')


@bot.command()
@commands.is_owner()  # Owner-only command
async def reload(ctx, extension):  # Reloads an extension; easy update without restarting
    bot.reload_extension(f'cogs.{extension}')
    await ctx.send(f'Reloaded {extension}')


@reload.error
async def reload_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        # CommandInvokeError bundles exceptions, original stored in error.original, not all errors have this attr
        inner_error = error.original
        if isinstance(inner_error, commands.ExtensionNotLoaded):
            extension = ctx.message.content.split()[1]
            bot.load_extension(f'cogs.{extension}')
            await ctx.send(f'Loaded {extension}')
            error.error_handled = True  # Monkey-patch attr for global event handler, which exception is passed to next


for filename in os.listdir('./cogs'):  # Load all cogs
    if filename.endswith('.py') and not filename.startswith('_'):  # If file starts with _ then ignore
        bot.load_extension(f'cogs.{filename[:-3]}')  # File extension not needed, remove ".py"

token = console_interaction.get_bot_token()  # Load bot token

bot.loop.run_until_complete(create_db_pool())
try:
    bot.run(token)
except discord.LoginFailure:
    print('Login failed. Is the token valid?', end='\n\n')
    if console_interaction.get_console_confirmation('Should I overwrite the token?'):
        print()  # Newline
        console_interaction.write_token()
        print('Token updated. Restart application to retry')
        input()  # Pause to show message
    else:
        quit()
