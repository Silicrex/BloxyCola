import discord


def get_general_help_embed(bot):
    embed = discord.Embed(
        color=0x00AD25
    )
    embed.set_author(name='Bot Commands', icon_url=bot.user.avatar_url)
    embed_body = [
        "**Hint: use `help <command/subcommand>` for more info!**",
        "**For mod commands: `modhelp`**",
        "**Don't forget the prefix!** `.`\n",
        "**\\> General**",
        "`help`, `modhelp`, `ping`\n",
        "**\\> Coin Flipping**",
        "`flip`, `stats`, `heads`, `tails`, `leaderboard`, `global`, `skins`, `equip`\n",
        "**\\> Colors**",
        "`color`, `setcolor`, `colors`, `modcolors`, `permacolors`, `boostredeem`\n",
    ]
    embed.description = ('\n'.join(embed_body))
    return embed


def get_general_mod_help_embed(bot):
    embed = discord.Embed(
        color=0xFF4747
    )
    embed.set_author(name='Bot Commands (Moderators)', icon_url=bot.user.avatar_url)
    embed_body = [
        "**Hint: use `modhelp <command/subcommand>` for more info!**",
        "**For user commands: `help`**",
        "**Don't forget the prefix!** `.`\n",
        "**\\> Colors**",
        "`color`, `createmod`, `createperm`, `boostredeem`\n",
        "**\\> Reactions**",
        "`logstatus`, `logstats`, `addlog`, `removelog`, `blacklist`\n",
    ]
    embed.description = ('\n'.join(embed_body))
    return embed


def get_help_embed(arg):
    help_dict = get_help_dict()
    if arg not in help_dict:
        embed = discord.Embed(
            title='Invalid command/subcommand',
            color=0xFFE900
        )
        return embed
    value = help_dict[arg]
    aliases_text = f"\n**Aliases:** {', '.join(value['alias'])}" if value['alias'] else ''
    embed = discord.Embed(
        title=value['title'],
        description=f"{value['description']}\n\n"
                    f"**Example:** {value['example']}"
                    f"{aliases_text}",
        color=0x00AD25
    )
    return embed


def get_modhelp_embed(arg):
    help_dict = get_help_dict()  # If command exists but has no mod functionality, display normally
    modhelp_dict = get_modhelp_dict()
    if arg not in modhelp_dict and arg not in help_dict:
        embed = discord.Embed(
            title='Invalid command/subcommand',
            color=0xFFE900
        )
        return embed
    if arg in modhelp_dict:
        value = modhelp_dict[arg]
    else:
        value = help_dict[arg]
    aliases_text = f"\n**Aliases:** {', '.join(value['alias'])}" if value['alias'] else ''
    embed = discord.Embed(
        title=value['title'],
        description=f"{value['description']}\n\n"
                    f"**Example:** {value['example']}"
                    f"{aliases_text}",
        color=0xFF4747
    )
    return embed


def get_help_dict():
    # Dictionary names are just for organization, they're all merged for the return

    # <> = parameter value
    # () = optional
    # / = either or
    utility = {
        'help':
            {
                'title': 'help (<command or subcommand>)',
                'description': '- Displays general command info (no arg)\n'
                               '- Can provide a specific command/subcommand to check\n'
                               '- Defaults to user version of command if there is also a mod version (use `modhelp` '
                               'for mod version)',
                'example': 'help addlog set',
                'alias': []
            },
        'modhelp':
            {
                'title': 'modhelp',
                'description': '- Displays commands with moderator functionality\n'
                               '- If a command is passed, will show moderator version, if one exists',
                'example': 'modhelp',
                'alias': ['mh']
            },
        'ping':
            {
                'title': 'ping',
                'description': '- Pong! Pings the bot\n'
                               '- Has nothing to do with your own ping',
                'example': 'ping',
                'alias': []
            },
        'logstatus':
            {
                'title': 'logstatus',
                'description': '- Shows current reaction log settings',
                'example': 'status',
                'alias': ['ls']
            },
    }
    logstats = {
        'logstats':
            {
                'title': 'logstats',
                'description': '- Shows stats on reactions added and removed',
                'example': 'logstats',
                'alias': []
            },
        'logstats on':
            {
                'title': 'logstats on',
                'description': '- Enables reaction add/remove stat tracking',
                'example': 'logstats on',
                'alias': []
            },
        'logstats off':
            {
                'title': 'logstats off',
                'description': '- Disables reaction add/remove stat tracking',
                'example': 'logstats off',
                'alias': []
            },
        'logstats clear':
            {
                'title': 'logstats clear',
                'description': '- Resets tracked stats on total reactions added/removed',
                'example': 'logstats clear',
                'alias': []
            },
    }
    add_log = {
        'addlog':
            {
                'title': 'addlog (set/on/off/clear)',
                'description': '- Shows add log help/settings (no arg), or manages add log\n',
                'example': 'addlog',
                'alias': ['add', 'a']
            },
        'addlog set':
            {
                'title': 'addlog set <channel id/mention>',
                'description': '- Sets the add log to the given channel',
                'example': 'addlog set #reaction-log',
                'alias': ['s']
            },
        'addlog on':
            {
                'title': 'addlog on',
                'description': '- Enables add log',
                'example': 'addlog on',
                'alias': []
            },
        'addlog off':
            {
                'title': 'addlog off',
                'description': '- Disables add log',
                'example': 'addlog off',
                'alias': []
            },
        'addlog clear':
            {
                'title': 'addlog clear',
                'description': '- Removes current channel set for add log',
                'example': 'addlog clear',
                'alias': []
            },
    }
    remove_log = {
        'removelog':
            {
                'title': 'removelog (set/on/off/clear)',
                'description': '- Shows remove log help/settings (no arg), or manages remove log',
                'example': 'removelog',
                'alias': ['remove', 'r']
            },
        'removelog set':
            {
                'title': 'removelog set <channel id/mention>',
                'description': '- Sets the remove log to the given channel',
                'example': 'removelog set #reaction-log',
                'alias': ['s']
            },
        'removelog on':
            {
                'title': 'removelog on',
                'description': '- Enables remove log',
                'example': 'removelog on',
                'alias': []
            },
        'removelog off':
            {
                'title': 'removelog off',
                'description': '- Disables remove log',
                'example': 'removelog off',
                'alias': []
            },
        'removelog clear':
            {
                'title': 'removelog clear',
                'description': '- Removes channel currently set for remove log',
                'example': 'removelog clear',
                'alias': []
            },
    }
    blacklist = {
        'blacklist':
            {
                'title': 'blacklist (add/addrole/remove/removerole/clear/list)',
                'description': '- Shows blacklist (reaction log ignore list) help/settings (no arg), '
                               'or manages blacklist',
                'example': 'blacklist',
                'alias': ['bl', 'b']
            },
        'blacklist add':
            {
                'title': 'blacklist add <user ID/mention>',
                'description': '- Adds user to reaction log ignore list',
                'example': 'blacklist add @User',
                'alias': ['a']
            },
        'blacklist addrole':
            {
                'title': 'blacklist addrole <role ID/mention>',
                'description': '- Adds role to reaction log ignore list',
                'example': 'blacklist addrole @Role',
                'alias': ['ar']
            },
        'blacklist remove':
            {
                'title': 'blacklist remove <user ID/mention>',
                'description': '- Removes user from reaction log ignore list',
                'example': 'blacklist remove @User',
                'alias': ['r']
            },
        'blacklist removerole':
            {
                'title': 'blacklist removerole <role ID/mention>',
                'description': '- Removes role from reaction log ignore list',
                'example': 'blacklist removerole @Member',
                'alias': ['rr']
            },
        'blacklist list':
            {
                'title': 'blacklist list <users/userid/roles/roleid>',
                'description': '- Displays corresponding blacklist information',
                'example': 'blacklist list users',
                'alias': ['l']
            },
        'blacklist clear':
            {
                'title': 'blacklist clear <users/roles/all>',
                'description': '- Clears corresponding reaction log blacklist',
                'example': 'blacklist clear all',
                'alias': []
            },
    }
    color = {
        'color':
            {
                'title': 'color (<user id/mention>)',
                'description': '- Shows info on your custom coloration, or one of a specified user\n'
                               '**- Moderators: use `.color help` or `.modhelp color`**',
                'example': 'color',
                'alias': ['cc', 'c']
            },
        'color help':
            {
                'title': 'color help',
                'description': '- Displays in-depth color guide',
                'example': 'color help',
                'alias': ['h']
            },
        'color create':
            {
                'title': 'color create <user id/mention> <color hex> <duration>',
                'description': '- Hash symbol in color hex is optional\n'
                               '- Duration can be left blank and defaults to 1 week\n'
                               '- Duration format is like `1m`, `2h`, `3d`, `4w`',
                'example': 'color create @User 7FF4FF 1w',
                'alias': ['c']
            },
        'color createmod':
            {
                'title': 'color createmod <user id/mention> <color hex>',
                'description': '- Hash symbol in color hex is optional\n'
                               '- Duration format is like `1m`, `2h`, `3d`, `4w`',
                'example': 'color createmod @User 7FF4FF',
                'alias': ['cmod']
            },
        'color createperm':
            {
                'title': 'color createperm <user id/mention> <color hex>',
                'description': '- Hash symbol in color hex is optional\n'
                               '- Duration format is like `1m`, `2h`, `3d`, `4w`',
                'example': 'color createperm @User 7FF4FF',
                'alias': ['cperm']
            },
        'color registertemp':
            {
                'title': 'color registertemp <user id/mention> <role id/mention> <duration>',
                'description': "- If the role exists but isn't registered, adds to database\n"
                               "- If the role is registered but as a different type, will switch the type to temp\n"
                               "- Duration can be left blank and defaults to 1 week\n"
                               "- Duration format is like `1m`, `2h`, `3d`, `4w`",
                'example': 'color registertemp @User @Role 1w',
                'alias': ['rt']
            },
        'color registermod':
            {
                'title': 'color registermod <user id/mention> <role id/mention>',
                'description': "- If the role exists but isn't registered, adds to database\n"
                               "- If the role is registered but as a different type, will switch the type to mod\n"
                               "- If the role is registered already, don't need to provide role (user is enough)",
                'example': 'color registermod @User',
                'alias': ['rm']
            },
        'color registerperm':
            {
                'title': 'color registerperm <user id/mention> <role id/mention>',
                'description': "- If the role exists but isn't registered, adds to database\n"
                               "- If the role is registered but as a different type, will switch the type to perm\n"
                               "- If the role is registered already, don't need to provide role (user is enough)",
                'example': 'color registerperm @User',
                'alias': ['rp']
            },
        'color remove':
            {
                'title': 'color remove <user id/mention>',
                'description': '- Removes given user coloration, deletes role',
                'example': 'color remove @User',
                'alias': ['delete', 'd', 'r']
            },
        'color softremove':
            {
                'title': 'color softremove <user id/mention>',
                'description': '- Removes given user coloration from database but does not delete the role',
                'example': 'color softremove @User',
                'alias': ['sr']
            },
        'color extend':
            {
                'title': 'color extend <user id/mention> <duration>',
                'description': '- Extends user coloration by given duration\n'
                               '- Duration can be left blank and defaults to 1 week',
                'example': 'color extend @User 1w',
                'alias': ['e']
            },
        'color reduce':
            {
                'title': 'color reduce <user id/mention> <duration>',
                'description': '- Reduces user coloration by given duration\n'
                               '- Duration can be left blank and defaults to 1 week',
                'example': 'color reduce @User 1w',
                'alias': ['rprime', 'lower', 'red', 'l']
            },
        'setcolor':
            {
                'title': 'setcolor <hex>',
                'description': '- Change your custom color! Takes a color hex (hash symbol optional)\n'
                               '- Requires a registered color (shows up with `color`)',
                'example': 'color 7FF4FF',
                'alias': ['sc']
            },
        'colors':
            {
                'title': 'colors',
                'description': '- View a list of active temp colorations and their remaining durations',
                'example': 'colors',
                'alias': ['cl']
            },
        'modcolors':
            {
                'title': 'modcolors',
                'description': '- View a list of mod colorations and their color hexes',
                'example': 'modcolors',
                'alias': ['mc']
            },
        'permacolors':
            {
                'title': 'permacolors',
                'description': '- View a list of permanent colorations and their color hexes',
                'example': 'permacolors',
                'alias': ['pc']
            },
    }
    boost_redeem = {
        'boostredeem':
            {
                'title': 'boostredeem',
                'description': "- Check if you're eligible for a Nitro Booster custom coloration\n"
                               "- See pins in boost channel for more info on how the system works",
                'example': 'boostredeem',
                'alias': ['br']
            },
        'boostredeem add':
            {
                'title': 'boostredeem add',
                'description': "- Adds user to the list of Nitro Boosters who have redeemed their color this month",
                'example': 'boostredeem add @User',
                'alias': ['a']
            },
        'boostredeem remove':
            {
                'title': 'boostredeem remove',
                'description': "- Removes user from the list of Nitro Boosters who have redeemed their color this "
                               "month\n"
                               "- Command generally exists for corrections. Bot automatically clears list monthly",
                'example': 'boostredeem remove @User',
                'alias': ['r']
            },
        'boostredeem list':
            {
                'title': 'boostredeem list',
                'description': "- Displays list of Nitro Boosters who have redeemed their color this month",
                'example': 'boostredeem list',
                'alias': ['l']
            },
    }
    coin_flipping = {
        'flip':
            {
                'title': 'flip',
                'description': '- Flips a coin!',
                'example': 'flip',
                'alias': ['f']
            },
        'stats':
            {
                'title': 'stats (<user id/mention>)',
                'description': '- Shows your coin flip stats, or those of a specified user!',
                'example': 'stats',
                'alias': ['s']
            },
        'heads':
            {
                'title': 'heads (<user id/mention>)',
                'description': '- Shows your detailed coin flip heads stats, or those of a specified user!',
                'example': 'heads',
                'alias': ['h']
            },
        'tails':
            {
                'title': 'tails (<user id/mention>)',
                'description': '- Shows your detailed coin flip tails stats, or those of a specified user!',
                'example': 'tails',
                'alias': ['t']
            },
        'global':
            {
                'title': 'global',
                'description': '- Shows global coin flip stats!',
                'example': 'global',
                'alias': ['g']
            },
        'skins':
            {
                'title': 'skins (<user id/mention>)',
                'description': '- Shows your unlocked coin flip skins, or those of a specified user!',
                'example': 'skins',
                'alias': ['sk']
            },
        'equip':
            {
                'title': 'equip <skin>',
                'description': '- Equips the specified unlocked skin!',
                'example': 'equip default',
                'alias': ['e']
            },
    }
    leaderboard = {
        'leaderboard':
            {
                'title': 'leaderboard (<category>) (<page #>)',
                'description': '- Use command without args to view available categories and their aliases\n'
                               '- (heads, tails, currentheads, currenttails, flips, allskins)\n'
                               '- Default page shown for a category is #1. Can also specify page number',
                'example': 'leaderboard heads 2',
                'alias': ['lb']
            },
        'leaderboard heads':
            {
                'title': 'leaderboard heads (<page #>)',
                'description': '- Shows the global leaderboard for best heads streak!\n'
                               '- In the case of ties, goes by time streak was achieved\n'
                               '- Defaults to page #1. Can also specify page',
                'example': 'leaderboard heads',
                'alias': ['h']
            },
        'leaderboard tails':
            {
                'title': 'leaderboard tails (<page #>)',
                'description': '- Shows the global leaderboard for best tails streak!\n'
                               '- In the case of ties, goes by time streak was achieved\n'
                               '- Defaults to page #1. Can also specify page',
                'example': 'leaderboard tails',
                'alias': ['t']
            },
        'leaderboard currentheads':
            {
                'title': 'leaderboard currentheads (<page #>)',
                'description': '- Shows the global leaderboard for best live heads streak!\n'
                               '- In the case of ties, goes by uid\n'
                               '- Defaults to page #1. Can also specify page',
                'example': 'leaderboard currentheads',
                'alias': ['ch']
            },
        'leaderboard currenttails':
            {
                'title': 'leaderboard currenttails (<page #>)',
                'description': '- Shows the global leaderboard for best live tails streak!\n'
                               '- In the case of ties, goes by uid\n'
                               '- Defaults to page #1. Can also specify page',
                'example': 'leaderboard currenttails',
                'alias': ['ct']
            },
        'leaderboard flips':
            {
                'title': 'leaderboard flips (<page #>)',
                'description': '- Shows the global leaderboard for total flips!\n'
                               '- Defaults to page #1. Can also specify page',
                'example': 'leaderboard flips',
                'alias': ['f']
            },
        'leaderboard allskins':
            {
                'title': 'leaderboard allskins (<page #>)',
                'description': '- Users are added onto the board once they have unlocked each skin\n'
                               '- Order is by time achieved',
                'example': 'leaderboard allskins',
                'alias': ['skins', 's']
            },
    }
    # Return dict of all commands
    locals_copy = locals()
    full_help_dict = {}
    for symbol in locals_copy:  # Combine all the dictionaries in the function scope
        obj = locals_copy[symbol]  # Object associated to the symbol
        if isinstance(obj, dict):  # If it's a dictionary, append it in
            full_help_dict.update(obj)
    return full_help_dict


def get_modhelp_dict():
    # Dictionary names are just for organization, they're all merged for the return

    # <> = parameter value
    # () = optional
    # / = either or
    logstats = {
        'logstats':
            {
                'title': 'logstats (on/off/clear)',
                'description': '- Shows stats on reactions added and removed (no arg), or manages tracking\n',
                'example': 'logstats',
                'alias': []
            },
    }
    color = {
        'color':
            {
                'title': 'color (<user id/mention>)/(help/create/remove/extend)',
                'description': '- Non-mod usage is checking your own color or that of a specified person\n'
                               '- `color help` to view more in-depth color guide\n',
                'example': 'color create @User 7FF4FF 1w',
                'alias': ['c']
            },
    }
    boost_redeem = {
        'boostredeem':
            {
                'title': 'boostredeem (<add/remove/list>)',
                'description': "- Check if you're eligible for a Nitro Booster custom coloration (no arg), "
                               "or manages the list\n"
                               "- This command is just for tracking, creating the color is separate\n"
                               "- Make sure to add Nitro Boosters who have redeemed their 1w color for the month\n"
                               "- Don't worry about clearing it; bot automatically does that each month",
                'example': 'boostredeem add @User',
                'alias': ['br']
            },
    }
    # Return dict of all commands
    locals_copy = locals()
    full_help_dict = {}
    for symbol in locals_copy:  # Combine all the dictionaries in the function scope
        obj = locals_copy[symbol]  # Object associated to the symbol
        if isinstance(obj, dict):  # If it's a dictionary, append it in
            full_help_dict.update(obj)
    return full_help_dict
