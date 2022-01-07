import discord
from discord.ext import commands
import time  # For ping command
from datetime import datetime as Datetime
from time_parsing import format_remaining_time


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):  # Message on successful launch
        print(f'{self.bot.user} ready')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.name == 'music-sharing':  # music-sharing thumbs-up reaction
            music_links = ['youtube.com', 'youtu.be', 'spotify.com', 'soundcloud.com']
            for music_link in music_links:
                if music_link in message.content:
                    await message.add_reaction('\N{THUMBS UP SIGN}')
                    break
        elif message.channel.name == 'bee-swarm':  # bee-swarm k/r reaction
            if 'k/r' in message.content.lower():
                await message.add_reaction('keep:917244569136005151')
                await message.add_reaction('replace:917244569182158868')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        mod_channel = self.bot.get_channel(332579851091312641)
        lobby = self.bot.get_channel(278099400285356033)

        # Check account age
        now = Datetime.now()
        created_at = member.created_at
        account_age = now - created_at
        account_age_seconds = account_age.total_seconds()
        if account_age_seconds < 2628000:  # Less than 30.4 days old
            await mod_channel.send(f'{member} joined, account age: `{format_remaining_time(account_age_seconds)}`')

        # Check username
        name_blacklist = {'discord.gg'}
        for word in name_blacklist:
            if word in member.name:
                await mod_channel.send(f'{member} joined, account age: `{format_remaining_time(account_age_seconds)}`. '
                                       f'Name contains {word}, not sending welcome message')
                return

        # Welcome message
        user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE uid = $1", str(member.id))
        if not user:  # User has no Bloxy Cola stats
            welcome_message = (f"Welcome to the server, {member.mention}! "
                               f"Please read our rules in the <#643330454568697858> channel. "
                               f"To unlock chat perms, please verify your Roblox account. "
                               f"Instructions can be found in <#775404743480705105>. "
                               f"If you are ever in need of any assistance, don't hesitate to contact a moderator!")
        else:  # User has Bloxy Cola stats
            welcome_message = (f"Welcome back to Fanmade, {member.mention}! "
                               f"As always; rules in <#643330454568697858>, "
                               f"verify in <#775404743480705105>, "
                               f"and don't hesitate to contact a moderator if you need anything!")
        await lobby.send(welcome_message)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):  # Error handler
        if hasattr(error, 'error_handled'):
            return
        if isinstance(error, commands.CommandNotFound):
            print(f'Invalid command by {ctx.author} in {ctx.channel}: {error.args[0]}')
        elif isinstance(error, commands.NoPrivateMessage):
            print(f'Attempted DM use by {ctx.author}: {error.args[0]}')
        elif isinstance(error, commands.MissingPermissions):
            print(f'{ctx.author} does not have permission:\n'
                  f'Permission: {error.args[0]}\n'
                  f'Message: {ctx.message.content}')
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="'{.command}' has a remaining cooldown of {:.2f} seconds".format(ctx, error.retry_after),
                color=0xC90000
            )
            embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.ChannelNotFound):
            embed = discord.Embed(
                title='Invalid channel',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                title='Invalid user',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.RoleNotFound):
            embed = discord.Embed(
                title='Invalid role',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            msg = ctx.message.content
            command = str(self.bot.get_command(msg[1:]))  # Remove prefix, convert aliases to full command
            help_dict = get_help_dict()
            embed = get_help_embed(help_dict, command)
            await ctx.send(embed=embed)
        else:  # Log to console
            print('- [Error]')
            print('Class:', error.__class__)
            print('Args:', error.args)
            print('- [Context]')
            print('Server:', ctx.guild)
            print('Channel:', ctx.channel)
            print('User:', ctx.author)
            print('Message:', ctx.message.content)
            print('Message ID:', ctx.message.id)
            raise error

    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def ping(self, ctx):  # Check latency
        start_time = time.monotonic()  # Start monotonic clock
        sent_message = await ctx.send('Pong!')  # Send message
        time_difference = time.monotonic() - start_time
        await sent_message.edit(content='Pong! {:.0f} ms'.format(time_difference * 1000))  # Edit time diff in as ms

    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def alias(self, ctx):
        embed = discord.Embed(
            title='Command aliases',
            description="**\\> = subcommand level**\n"
                        "**'yes'/'y', 'no'/'n' interchangeable**"
        )
        embed.add_field(name='help', inline=True, value='- h')
        embed.add_field(name='addlog', inline=True, value='- add\n'
                                                          '- a\n'
                                                          '**\\> set**\n'
                                                          '- s')
        embed.add_field(name='removelog', inline=True, value='- remove\r'
                                                             '- r\n'
                                                             '**\\> set**\n'
                                                             '- s')
        embed.add_field(name='status', inline=True, value='- s')
        embed.add_field(name='blacklist', inline=True, value='- bl\n'
                                                             '- b\n'
                                                             '**\\> add**\n'
                                                             '- a\n'
                                                             '**\\> addrole**\n'
                                                             '- ar\n'
                                                             '**\\> remove**\n'
                                                             '- r\n'
                                                             '**\\> removerole**\n'
                                                             '- rr\n'
                                                             '**\\> list**\n'
                                                             '- l')
        embed.add_field(name='blacklist list', inline=True, value='**\\>> users**\n'
                                                                  '- user\n'
                                                                  '- u\n'
                                                                  '**\\>> userid**\n'
                                                                  '- uid\n'
                                                                  '**\\>> roles**\n'
                                                                  '- role\n'
                                                                  '- r\n'
                                                                  '**\\>> roleid**\n'
                                                                  '- rid')
        embed.add_field(name='blacklist clear', inline=True, value='**\\>> users**\n'
                                                                   '- user\n'
                                                                   '- u\n'
                                                                   '**\\>> roles**\n'
                                                                   '- role\n'
                                                                   '- r\n')
        await ctx.send(embed=embed)

    @commands.command(aliases=['h'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def help(self, ctx):
        embed = discord.Embed(
            color=0x00AD25
        )
        embed.set_author(name='Bot Commands', icon_url=self.bot.user.avatar_url)
        embed.add_field(name='.help', value='Prints commands')
        embed.add_field(name='.ping', value='Pong!', inline=False)
        embed.add_field(name='.flip', value='Flips a coin', inline=False)
        embed.add_field(name='.stats', value='Shows your .flip stats', inline=False)
        embed.add_field(name='.heads', value='More thorough heads stats', inline=False)
        embed.add_field(name='.tails', value='More thorough tails stats', inline=False)
        embed.add_field(name='.lb (tails/current/flips)', value='Shows the corresponding lb.'
                                                                ' Default is best heads streak', inline=False)
        embed.add_field(name='.global', value='Total count of heads/tails rolls for all users', inline=False)
        embed.add_field(name='.color (<user>)', value='- Displays info about your temp color; or another user if given',
                        inline=False)
        embed.add_field(name='.colors', value='Displays all active registered temp colors', inline=False)
        embed.add_field(name='.setcolor <color hex>', value='Used to modify your color role', inline=False)
        embed.add_field(name='.permacolor list',
                        value='- Displays users who have a registered perma color\n- Has alias of \'.pc l\'',
                        inline=False)
        embed.add_field(name='.boostredeem list',
                        value='- Displays users who have redeemed a 7d Nitro color this month\n- Has alias of \'.b l\'',
                        inline=False)
        embed.add_field(name='.skins', value='- Displays all your unlocked skins', inline=False)
        embed.add_field(name='.equip <skin>', value='- Equips the given skin, assuming you\'ve unlocked it',
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['h2'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def help2(self, ctx, *, arg1=None):
        if arg1 is None:  # Then print general help
            embed = get_general_help_embed()
            await ctx.send(embed=embed)
        else:
            arg1 = str(self.bot.get_command(arg1))  # Convert aliases to full command
            help_dict = get_help_dict()
            if arg1 in help_dict:
                embed = get_help_embed(help_dict, arg1)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title='Invalid command/subcommand',
                    color=0xFFE900
                )
                await ctx.send(embed=embed)


def setup(bot):  # For cog loading
    bot.add_cog(Utility(bot))


def get_general_help_embed():
    embed = discord.Embed(
        title='Bot Commands',
        description='**<> = Parameter**\n'
                    '**() = optional**\n'
                    '**/ = pick between**'
    )

    utility_module = get_help_dict('utility')
    utility_fields = []
    for key, value in utility_module.items():  # Create utility text
        utility_fields.append(f"**- {value['title']}**\n"
                              f"{value['description']}")
    utility_text = '\n'.join(utility_fields)

    reactions_module = get_help_dict('reactions')
    reactions_fields = []
    for key, value in reactions_module.items():  # Create reactions text
        reactions_fields.append(f"**- {value['title']}**\n"
                                f"{value['description']}")
    reactions_text = '\n'.join(reactions_fields)

    embed.add_field(name='\\> Utility', value=utility_text, inline=True)
    embed.add_field(name='\\> Reactions', value=reactions_text, inline=True)
    return embed


def get_help_embed(help_dict, arg):
    value = help_dict[arg]
    embed = discord.Embed(
        title=value['title'],
        description=f"{value['description']}\n\n"
                    f"**Example:** {value['example']}\n"
                    f"**Aliases:** {value['alias'] if value['alias'] else 'None'}"
    )
    return embed


def get_help_dict(module=None):
    # <> = parameter value
    # () = optional
    # / = either or
    utility = {
        'help':
            {
                'title': 'help (<command or subcommand>)',
                'description': 'Displays general command info; or specific info if command is supplied',
                'example': 'help addlog set',
                'alias': []
            },
        'alias':
            {
                'title': 'alias',
                'description': 'Displays command/subcommand aliases',
                'example': 'alias',
                'alias': []
            },
        'ping':
            {
                'title': 'ping',
                'description': 'Pong! Pings the bot',
                'example': 'ping',
                'alias': []
            },
    }
    reactions = {
        'status':
            {
                'title': 'status',
                'description': 'Shows current reaction log settings',
                'example': 'status',
                'alias': ['s']
            },
        'logstats':
            {
                'title': 'logstats (on/off/clear)',
                'description': 'Shows reaction add/remove stats; or manages stat tracking. Bypasses log toggles',
                'example': 'logstats',
                'alias': []
            },
        'addlog':
            {
                'title': 'addlog (set/on/off/clear)',
                'description': 'Shows add log help/settings; or manages add log',
                'example': 'addlog',
                'alias': ['add', 'a']
            },
        'removelog':
            {
                'title': 'removelog (set/on/off/clear)',
                'description': 'Shows remove log help/settings; or manages remove log',
                'example': 'removelog',
                'alias': ['remove', 'r']
            },
        'blacklist':
            {
                'title': 'blacklist (add/addrole/remove/removerole/clear/list)',
                'description': 'Shows blacklist (reaction log ignore list) help/settings; or manages blacklist',
                'example': 'blacklist',
                'alias': ['bl', 'b']
            },
    }
    # Subcommands --------------------------------
    addlog = {
        'addlog set':
            {
                'title': 'addlog set <channel id/mention>',
                'description': 'Sets the add log to the given channel; takes ID or mention',
                'example': 'addlog set #reaction-log',
                'alias': ['s']
            },
        'addlog on':
            {
                'title': 'addlog on',
                'description': 'Enables add log',
                'example': 'addlog on',
                'alias': []
            },
        'addlog off':
            {
                'title': 'addlog off',
                'description': 'Disables add log',
                'example': 'addlog off',
                'alias': []
            },
        'addlog clear':
            {
                'title': 'addlog clear',
                'description': 'Removes channel set to add log',
                'example': 'addlog clear',
                'alias': []
            },
    }
    removelog = {
        'removelog set':
            {
                'title': 'removelog set <channel id/mention>',
                'description': 'Sets the remove log to the given channel; takes ID or mention',
                'example': 'removelog set #reaction-log',
                'alias': ['s']
            },
        'removelog on':
            {
                'title': 'removelog on',
                'description': 'Enables remove log',
                'example': 'removelog on',
                'alias': []
            },
        'removelog off':
            {
                'title': 'removelog off',
                'description': 'Disables remove log',
                'example': 'removelog off',
                'alias': []
            },
        'removelog clear':
            {
                'title': 'removelog clear',
                'description': 'Removes channel set to remove log',
                'example': 'removelog clear',
                'alias': []
            },
    }
    blacklist = {
        'blacklist add':
            {
                'title': 'blacklist add <user ID/mention>',
                'description': 'Adds user to reaction log ignore list; takes ID or mention',
                'example': 'blacklist add @Somebody',
                'alias': ['a']
            },
        'blacklist addrole':
            {
                'title': 'blacklist addrole <role ID/mention>',
                'description': 'Adds role to reaction log ignore list; takes ID or mention',
                'example': 'blacklist addrole @Moderator',
                'alias': ['ar']
            },
        'blacklist remove':
            {
                'title': 'blacklist remove <user ID/mention>',
                'description': 'Removes user from reaction log ignore list; takes ID or mention',
                'example': 'blacklist remove @Somebody',
                'alias': ['r']
            },
        'blacklist removerole':
            {
                'title': 'blacklist removerole <role ID/mention>',
                'description': 'Removes role from reaction log ignore list; takes ID or mention',
                'example': 'blacklist removerole @Member',
                'alias': ['rr']
            },
        'blacklist list':
            {
                'title': 'blacklist list <users/userid/roles/roleid>',
                'description': 'Displays embed blacklist of user mentions/user ids/role mentions/role ids',
                'example': 'blacklist list users',
                'alias': ['l']
            },
        'blacklist clear':
            {
                'title': 'blacklist clear <users/roles/all>',
                'description': 'Clears corresponding reaction log ignore list',
                'example': 'blacklist clear all',
                'alias': []
            },
    }
    logstats = {
        'logstats on':
            {
                'title': 'logstats on',
                'description': 'Enables reaction add/remove stat tracking. Bypasses log toggles',
                'example': 'logstats on',
                'alias': []
            },
        'logstats off':
            {
                'title': 'logstats off',
                'description': 'Disables reaction add/remove stat tracking. Bypasses log toggles',
                'example': 'logstats off',
                'alias': []
            },
        'logstats clear':
            {
                'title': 'logstats clear',
                'description': 'Resets tracked stats on total reactions added/removed (has timed confirmation prompt; '
                               'resets from time of confirmation)',
                'example': 'logstats clear',
                'alias': []
            },
    }
    locals_copy = locals()
    if module:  # If a specific module has been given
        return locals_copy[module]  # Return that specific dictionary
    else:  # No module specified, return dict of all commands
        full_help_dict = {}
        for symbol in locals_copy:  # Combine all the dictionaries in the function scope
            obj = locals_copy[symbol]  # Object associated to the symbol
            if isinstance(obj, dict):  # If it's a dictionary, append it in
                full_help_dict.update(obj)
        return full_help_dict
