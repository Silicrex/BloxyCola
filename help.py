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
        "`help`, `alias`, `ping`\n",
        "**\\> Coin Flipping**",
        "`flip`, `stats`, `heads`, `tails`, `leaderboard`, `global`, `skins`, `equip`\n",
        "**\\> Colors**",
        "`color`, `setcolor`, `colors`, `modcolors`, `permacolors`, `boostredeem`\n",
    ]
    embed.description = ('\n'.join(embed_body))
    return embed


def get_general_mod_help_embed(bot):
    embed = discord.Embed(
        color=0x00AD25
    )
    embed.set_author(name='Bot Commands (Moderators)', icon_url=bot.user.avatar_url)
    embed_body = [
        "**Hint: use `help <command/subcommand>` for more info!**",
        "**For user commands: `help`**",
        "**Don't forget the prefix!** `.`\n",
        "**\\> Colors**",
        "`color`, `createmod`, `createperm`, `boostredeem`\n",
        "**\\> Reactions**",
        "`status`, `logstats`, `addlog`, `removelog`, `blacklist`\n",
    ]
    embed.description = ('\n'.join(embed_body))
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