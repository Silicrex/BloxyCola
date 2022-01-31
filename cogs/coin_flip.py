import discord
from discord.ext import commands
import json
import random
import time
from database_functions import get_user

with open('coin_assets.json', 'r') as file:  # Load coin images
    coin_assets = json.load(file)


class CoinFlip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---------------------------------------- FLIP ----------------------------------------
    @commands.command(aliases=['f'])
    @commands.cooldown(rate=1, per=0.5, type=commands.BucketType.user)
    async def flip(self, ctx):
        uid_string = str(ctx.author.id)
        user = await get_user(self.bot, uid_string)

        equipped_skin = user['equipped_skin']

        flip_result = random.randint(0, 1)

        if flip_result == 0:  # Heads
            # Increment stats ---------------------------------
            current_heads_streak = user['current_heads_streak'] + 1
            await self.bot.pg_con.execute("UPDATE users SET heads = $1 WHERE uid = $2", user['heads'] + 1, uid_string)
            await self.bot.pg_con.execute("UPDATE users SET current_heads_streak = $1 WHERE uid = $2",
                                          current_heads_streak, uid_string)
            # Check for best heads streak ---------------------------------
            best_heads_streak = user['best_heads_streak']
            if current_heads_streak > best_heads_streak:
                best_heads_streak = current_heads_streak
                await self.bot.pg_con.execute("UPDATE users SET best_heads_streak = $1 WHERE uid = $2",
                                              best_heads_streak, uid_string)
                await self.bot.pg_con.execute("UPDATE users SET last_best_heads_streak = $1 WHERE uid = $2",
                                              time.time(), uid_string)
            # End tails streak ---------------------------------
            current_tails_streak = user['current_tails_streak']
            tails_streaks = eval(user['tails_streaks'])  # Dict of # of times a certain streak was reached
            if current_tails_streak > 0:  # Update # of times
                tails_streaks[current_tails_streak] = tails_streaks.get(current_tails_streak, 0) + 1
                await self.bot.pg_con.execute("UPDATE users SET tails_streaks = $1 WHERE uid = $2",
                                              str(tails_streaks), uid_string)
                current_tails_streak = 0
                await self.bot.pg_con.execute("UPDATE users SET current_tails_streak = $1 WHERE uid = $2",
                                              current_tails_streak, uid_string)
            best_tails_streak = user['best_tails_streak']  # For printing
            # Send message ---------------------------------
            embed = discord.Embed(
                title=f'Flipped a coin..',
                description='..and got `heads`!',
                color=0x00AD25
            )
            embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=coin_assets[equipped_skin]['heads'])
            embed.add_field(name='Heads Streak', value=f'{current_heads_streak}')
            embed.add_field(name='\u200b', value='\u200b', inline=True)  # Blank line for formatting
            embed.add_field(name='Best Heads Streak', value=f'{best_heads_streak}')
            embed.add_field(name='Tails Streak', value=f'{current_tails_streak}')
            embed.add_field(name='\u200b', value='\u200b', inline=True)  # Blank line for formatting
            embed.add_field(name='Best Tails Streak', value=f'{best_tails_streak}')
            await ctx.send(embed=embed)

        elif flip_result == 1:  # Tails
            # Increment stats ---------------------------------
            current_tails_streak = user['current_tails_streak'] + 1
            await self.bot.pg_con.execute("UPDATE users SET tails = $1 WHERE uid = $2", user['tails'] + 1, uid_string)
            await self.bot.pg_con.execute("UPDATE users SET current_tails_streak = $1 WHERE uid = $2",
                                          current_tails_streak, uid_string)
            # Check for best tails streak ---------------------------------
            best_tails_streak = user['best_tails_streak']
            if current_tails_streak > best_tails_streak:
                best_tails_streak = current_tails_streak
                await self.bot.pg_con.execute("UPDATE users SET best_tails_streak = $1 WHERE uid = $2",
                                              best_tails_streak, uid_string)
                await self.bot.pg_con.execute("UPDATE users SET last_best_tails_streak = $1 WHERE uid = $2",
                                              time.time(), uid_string)
            # End heads streak ---------------------------------
            current_heads_streak = user['current_heads_streak']
            heads_streaks = eval(user['heads_streaks'])  # Dict of # of times a certain streak was reached
            if current_heads_streak > 0:  # Update # of times
                heads_streaks[current_heads_streak] = heads_streaks.get(current_heads_streak, 0) + 1
                await self.bot.pg_con.execute("UPDATE users SET heads_streaks = $1 WHERE uid = $2",
                                              str(heads_streaks), uid_string)
                current_heads_streak = 0
                await self.bot.pg_con.execute("UPDATE users SET current_heads_streak = $1 WHERE uid = $2",
                                              current_heads_streak, uid_string)
            best_heads_streak = user['best_heads_streak']  # For printing
            # Send message ---------------------------------
            embed = discord.Embed(
                title=f'Flipped a coin..',
                description='..and got `tails`!',
                color=0x00AD25
            )
            embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=coin_assets[equipped_skin]['tails'])
            embed.add_field(name='Heads Streak', value=f'{current_heads_streak}')
            embed.add_field(name='\u200b', value='\u200b', inline=True)  # Blank line for formatting
            embed.add_field(name='Best Heads Streak', value=f'{best_heads_streak}')
            embed.add_field(name='Tails Streak', value=f'{current_tails_streak}')
            embed.add_field(name='\u200b', value='\u200b', inline=True)  # Blank line for formatting
            embed.add_field(name='Best Tails Streak', value=f'{best_tails_streak}')
            await ctx.send(embed=embed)
        # Post-flip
        skin_inv = eval(user['skin_inv'])  # List of skin names
        if len(skin_inv) < len(coin_assets):  # Not all unlocked
            skin_unlock_roll = random.randint(1, 50)  # 2% chance
            if skin_unlock_roll == 1:
                locked_skins = [x for x in coin_assets if x not in skin_inv]
                unlocked_skin = random.choice(locked_skins)
                skin_inv.append(unlocked_skin)
                await self.bot.pg_con.execute("UPDATE users SET skin_inv = $1 WHERE uid = $2",
                                              str(skin_inv), uid_string)
                await self.bot.pg_con.execute("UPDATE users SET last_skin_unlock = $1 WHERE uid = $2",
                                              time.time(), uid_string)
                embed = discord.Embed(
                    description=f'**{ctx.author.mention} unlocked the {unlocked_skin.capitalize()} skin! Congrats!**',
                    color=0x00AD25
                )
                embed.set_author(name='New Skin Unlocked!!',
                                  icon_url='https://cdn.discordapp.com/attachments/411087880933343232/862129774758199347/popper.png')
                embed.set_footer(
                    text=f"Hint: Equip with '.equip {unlocked_skin}'! Check your unlocked skins with '.skins'")
                await ctx.send(embed=embed)
                print(f'{ctx.author} unlocked {unlocked_skin} in {ctx.channel}')

    # ---------------------------------------- STATS ----------------------------------------
    @commands.command(aliases=['s'])
    @commands.cooldown(rate=1, per=1.2, type=commands.BucketType.user)
    async def stats(self, ctx, member: discord.Member = None):
        embed = discord.Embed(
            color=0x00AD25
        )
        if not member:  # Member not specified, default to command user
            uid_string = str(ctx.author.id)
            user = await get_user(self.bot, uid_string)
            embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        else:
            uid_string = str(member.id)
            user = await get_user(self.bot, uid_string)
            embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=member.avatar_url)
        embed.add_field(name='Current Heads Streak', value=user['current_heads_streak'], inline=True)
        embed.add_field(name='Best Heads Streak', value=user['best_heads_streak'], inline=True)
        embed.add_field(name='Total Heads', value=user['heads'], inline=True)
        embed.add_field(name='Current Tails Streak', value=user['current_tails_streak'], inline=True)
        embed.add_field(name='Best Tails Streak', value=user['best_tails_streak'])
        embed.add_field(name='Total Tails', value=user['tails'], inline=True)
        embed.add_field(name='Unlocked Skins', value=f'{len(eval(user["skin_inv"]))}/{len(coin_assets)}', inline=True)
        embed.add_field(name='Equipped Skin', value=user['equipped_skin'].capitalize(), inline=True)
        embed.add_field(name='Total Flips', value=user['heads'] + user['tails'], inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=1.2, type=commands.BucketType.user)
    async def heads(self, ctx, member: discord.Member = None):
        embed = discord.Embed(
            title='Heads Stats',
            color=0x00AD25
        )
        if not member:  # Member not specified, default to command user
            uid_string = str(ctx.author.id)
            user = await get_user(self.bot, uid_string)
            embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        else:
            uid_string = str(member.id)
            user = await get_user(self.bot, uid_string)
            embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=member.avatar_url)
        embed.add_field(name='Current Heads Streak', value=user['current_heads_streak'], inline=True)
        embed.add_field(name='Best Heads Streak', value=user['best_heads_streak'], inline=True)
        embed.add_field(name='Total Heads', value=user['heads'], inline=True)
        heads_streaks = eval(user['heads_streaks'])
        sorted_list = sorted(list(heads_streaks.items()), key=lambda x: int(x[0]))
        for streak, count in dict(sorted_list).items():
            embed.add_field(name=f'{streak} streaks:', value=f'{count}', inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=1.2, type=commands.BucketType.user)
    async def tails(self, ctx, member: discord.Member = None):
        embed = discord.Embed(
            title='Tails Stats',
            color=0x00AD25
        )
        if not member:  # Member not specified, default to command user
            uid_string = str(ctx.author.id)
            user = await get_user(self.bot, uid_string)
            embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        else:
            uid_string = str(member.id)
            user = await get_user(self.bot, uid_string)
            embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=member.avatar_url)
        embed.add_field(name='Current Tails Streak', value=user['current_tails_streak'], inline=True)
        embed.add_field(name='Best Tails Streak', value=user['best_tails_streak'], inline=True)
        embed.add_field(name='Total Tails', value=user['tails'], inline=True)
        tails_streaks = eval(user['tails_streaks'])
        sorted_list = sorted(list(tails_streaks.items()), key=lambda x: int(x[0]))
        for streak, count in dict(sorted_list).items():
            embed.add_field(name=f'{streak} streaks:', value=f'{count}', inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='global', aliases=['g'])
    @commands.cooldown(rate=1, per=1.2, type=commands.BucketType.user)
    async def _global(self, ctx):
        embed = discord.Embed(
            color=0x00AD25
        )
        global_heads = await self.bot.pg_con.fetch("SELECT SUM(heads) from users")  # Returns list of records
        global_heads = global_heads[0][0]
        global_tails = await self.bot.pg_con.fetch("SELECT SUM(tails) from users")  # Returns list of records
        global_tails = global_tails[0][0]
        embed.set_author(name='Global Flip Stats', icon_url=self.bot.user.avatar_url)
        embed.add_field(name='Global Heads', value=f'{global_heads}')
        embed.add_field(name='Global Tails', value=f'{global_tails}')
        embed.add_field(name='Global Total', value=f'{global_heads + global_tails}')
        await ctx.send(embed=embed)

    @commands.group(aliases=['lb'], invoke_without_command=True)
    @commands.cooldown(rate=1, per=1.2, type=commands.BucketType.user)
    async def leaderboard(self, ctx):
        embed = discord.Embed(
            title='Valid leaderboards',
            description="heads (h)\ntails (t)\ncurrent heads (ch)\ncurrent tails (ct)\nflips (f)\n"
                        "allskins (s)\n\nex: .lb heads 2"
        )
        await ctx.send(embed=embed)

    @leaderboard.command(name='heads', aliases=['h'])
    async def leaderboard_heads(self, ctx, page='1'):
        if page.isnumeric():
            page = eval(page)
        if not isinstance(page, int):
            embed = discord.Embed(
                title=f'Invalid argument, 3rd parameter is for page number',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        keys_per_page = 10
        stats_fetch = await self.bot.pg_con.fetch("SELECT * FROM users ORDER BY best_heads_streak DESC, "
                                                  "last_best_heads_streak ASC")
        starting_index = (page - 1) * keys_per_page
        length = len(stats_fetch)
        max_pages = (length - 1)//keys_per_page + 1
        if page > max_pages or page <= 0:
            embed = discord.Embed(
                title=f'Invalid page, there are {max_pages} page(s)',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(
            title=f'Best Heads Streak Leaderboard (Page {page}/{max_pages})',
            color=0x00AD25
        )
        displayed_count = 0  # Number displayed
        skipped_count = 0  # Number of users that have left, used to correct pos #
        index = starting_index
        while displayed_count < keys_per_page and index < length - 1:  # Don't index error on last page
            user = stats_fetch[index]
            member = self.bot.get_user(int(user['uid']))
            if member is not None:  # Ignore users that have left
                embed.add_field(name=f'[{index + 1 - skipped_count}] {member.name}#{member.discriminator}:',
                                value=f'{user["best_heads_streak"]} streak', inline=False)
                displayed_count += 1
            else:
                skipped_count += 1
            index += 1
        await ctx.send(embed=embed)

    @leaderboard.command(name='tails', aliases=['t'])
    async def leaderboard_tails(self, ctx, page='1'):
        if page.isnumeric():
            page = eval(page)
        if not isinstance(page, int):
            embed = discord.Embed(
                title=f'Invalid argument, 3rd parameter is for page number',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        keys_per_page = 10
        stats_fetch = await self.bot.pg_con.fetch("SELECT * FROM users ORDER BY best_tails_streak DESC, "
                                                  "last_best_tails_streak ASC")
        starting_index = (page - 1) * keys_per_page
        length = len(stats_fetch)
        max_pages = (length - 1) // keys_per_page + 1
        if page > max_pages or page <= 0:
            embed = discord.Embed(
                title=f'Invalid page, there are {max_pages} page(s)',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(
            title=f'Best Tails Streak Leaderboard (Page {page}/{max_pages})',
            color=0x00AD25
        )
        displayed_count = 0  # Number displayed
        skipped_count = 0  # Number of users that have left, used to correct pos #
        index = starting_index
        while displayed_count < keys_per_page and index < length - 1:  # Don't index error on last page
            user = stats_fetch[index]
            member = self.bot.get_user(int(user['uid']))
            if member is not None:  # Ignore users that have left
                embed.add_field(name=f'[{index + 1 - skipped_count}] {member.name}#{member.discriminator}:',
                                value=f'{user["best_tails_streak"]} streak', inline=False)
                displayed_count += 1
            else:
                skipped_count += 1
            index += 1
        await ctx.send(embed=embed)

    @leaderboard.command(name='currentheads', aliases=['ch'])
    async def leaderboard_currentheads(self, ctx, page='1'):
        if page.isnumeric():
            page = eval(page)
        if not isinstance(page, int):
            embed = discord.Embed(
                title=f'Invalid argument, 3rd parameter is for page number',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        keys_per_page = 10
        stats_fetch = await self.bot.pg_con.fetch("SELECT * FROM users ORDER BY current_heads_streak DESC, uid ASC")
        starting_index = (page - 1) * keys_per_page
        length = len(stats_fetch)
        max_pages = (length - 1) // keys_per_page + 1
        if page > max_pages or page <= 0:
            embed = discord.Embed(
                title=f'Invalid page, there are {max_pages} page(s)',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(
            title=f'Best Current Heads Streak Leaderboard (Page {page}/{max_pages})',
            color=0x00AD25
        )
        displayed_count = 0  # Number displayed
        skipped_count = 0  # Number of users that have left, used to correct pos #
        index = starting_index
        while displayed_count < keys_per_page and index < length - 1:  # Don't index error on last page
            user = stats_fetch[index]
            member = self.bot.get_user(int(user['uid']))
            if member is not None:  # Ignore users that have left
                embed.add_field(name=f'[{index + 1 - skipped_count}] {member.name}#{member.discriminator}:',
                                value=f'{user["current_heads_streak"]} streak', inline=False)
                displayed_count += 1
            else:
                skipped_count += 1
            index += 1
        await ctx.send(embed=embed)

    @leaderboard.command(name='currenttails', aliases=['ct'])
    async def leaderboard_currenttails(self, ctx, page='1'):
        if page.isnumeric():
            page = eval(page)
        if not isinstance(page, int):
            embed = discord.Embed(
                title=f'Invalid argument, 3rd parameter is for page number',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        keys_per_page = 10
        stats_fetch = await self.bot.pg_con.fetch("SELECT * FROM users ORDER BY current_tails_streak DESC, uid ASC")
        starting_index = (page - 1) * keys_per_page
        length = len(stats_fetch)
        max_pages = (length - 1) // keys_per_page + 1
        if page > max_pages or page <= 0:
            embed = discord.Embed(
                title=f'Invalid page, there are {max_pages} page(s)',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(
            title=f'Best Current Tails Streak Leaderboard (Page {page}/{max_pages})',
            color=0x00AD25
        )
        displayed_count = 0  # Number displayed
        skipped_count = 0  # Number of users that have left, used to correct pos #
        index = starting_index
        while displayed_count < keys_per_page and index < length - 1:  # Don't index error on last page
            user = stats_fetch[index]
            member = self.bot.get_user(int(user['uid']))
            if member is not None:  # Ignore users that have left
                embed.add_field(name=f'[{index + 1 - skipped_count}] {member.name}#{member.discriminator}:',
                                value=f'{user["current_tails_streak"]} streak', inline=False)
                displayed_count += 1
            else:
                skipped_count += 1
            index += 1
        await ctx.send(embed=embed)

    @leaderboard.command(name='flips', aliases=['f'])
    async def leaderboard_flips(self, ctx, page='1'):
        if page.isnumeric():
            page = eval(page)
        if not isinstance(page, int):
            embed = discord.Embed(
                title=f'Invalid argument, 3rd parameter is for page number',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        keys_per_page = 10
        stats_fetch = await self.bot.pg_con.fetch("SELECT * FROM users ORDER BY heads + tails DESC, uid ASC")
        starting_index = (page - 1) * keys_per_page
        length = len(stats_fetch)
        max_pages = (length - 1) // keys_per_page + 1
        if page > max_pages or page <= 0:
            embed = discord.Embed(
                title=f'Invalid page, there are {max_pages} page(s)',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(
            title=f'Best Total Flips Leaderboard (Page {page}/{max_pages})',
            color=0x00AD25
        )
        displayed_count = 0  # Number displayed
        skipped_count = 0  # Number of users that have left, used to correct pos #
        index = starting_index
        while displayed_count < keys_per_page and index < length - 1:  # Don't index error on last page
            user = stats_fetch[index]
            member = self.bot.get_user(int(user['uid']))
            if member is not None:  # Ignore users that have left
                embed.add_field(name=f'[{index + 1 - skipped_count}] {member.name}#{member.discriminator}:',
                                value=f'{user["heads"] + user["tails"]} flips', inline=False)
                displayed_count += 1
            else:
                skipped_count += 1
            index += 1
        await ctx.send(embed=embed)

    @leaderboard.command(name='allskins', aliases=['skins', 's'])
    async def leaderboard_allskins(self, ctx, page='1'):
        if page.isnumeric():
            page = eval(page)
        if not isinstance(page, int):
            embed = discord.Embed(
                title=f'Invalid argument, 3rd parameter is for page number',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        # 2 brackets, name chars, 2 quotes + 1 comma per name - no end comma
        max_skin_inv_length = 2 + sum([len(x) for x in coin_assets]) + 3 * len(coin_assets) - 1
        keys_per_page = 10
        stats_fetch = await self.bot.pg_con.fetch("SELECT * FROM users WHERE LENGTH(skin_inv) > $1 "
                                                  "ORDER BY last_skin_unlock ASC", max_skin_inv_length)
        starting_index = (page - 1) * keys_per_page
        length = len(stats_fetch)
        max_pages = (length - 1) // keys_per_page + 1
        if page > max_pages or page <= 0:
            embed = discord.Embed(
                title=f'Invalid page, there are {max_pages} page(s)',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(
            title=f'All Skins Leaderboard (Page {page}/{max_pages})',
            color=0x00AD25
        )
        displayed_count = 0  # Number displayed
        skipped_count = 0  # Number of users that have left, used to correct pos #
        index = starting_index
        while displayed_count < keys_per_page and index < length - 1:  # Don't index error on last page
            user = stats_fetch[index]
            member = self.bot.get_user(int(user['uid']))
            if member is not None:  # Ignore users that have left
                embed.add_field(name=f'[{index + 1 - skipped_count}] {member.name}#{member.discriminator}:',
                                value=f'{len(eval(user["skin_inv"]))} skins', inline=False)
                displayed_count += 1
            else:
                skipped_count += 1
            index += 1
        await ctx.send(embed=embed)

    # ---------------------------------------- SKINS ----------------------------------------
    @commands.command(aliases=['skin', 'sk'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def skins(self, ctx, member: discord.Member = None):
        embed = discord.Embed(
            color=0x00AD25
        )
        if not member:  # Member not specified, default to command user
            uid_string = str(ctx.author.id)
            user = await get_user(self.bot, uid_string)
            embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        else:
            uid_string = str(member.id)
            user = await get_user(self.bot, uid_string)
            embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=member.avatar_url)
        skin_inv = sorted(eval(user['skin_inv']))  # List of skins)
        skin_inv.remove('default')
        skin_inv.insert(0, 'default')  # Reposition default to the top
        embed.title = f'Skins ({len(skin_inv)}/{len(coin_assets)})'
        embed.description = '\n'.join([x.capitalize() for x in skin_inv])
        await ctx.send(embed=embed)

    @commands.command(aliases=['e'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def equip(self, ctx, skin=None):
        if skin is None:
            embed = discord.Embed(
                title="Specify a skin to equip",
                color=0xC90000
            )
            await ctx.send(embed=embed)
            return
        skin = skin.lower()
        uid_string = str(ctx.author.id)
        user = await get_user(self.bot, uid_string)
        skin_inv = user['skin_inv']
        currently_equipped = user['equipped_skin']
        if skin not in coin_assets:
            embed = discord.Embed(
                title="Invalid skin. Use '.skins' to see your unlocked skins",
                color=0xC90000
            )
            await ctx.send(embed=embed)
            return
        elif skin not in skin_inv:
            embed = discord.Embed(
                title="You haven't unlocked this skin! Use '.skins' to see your unlocked skins",
                color=0xC90000
            )
            await ctx.send(embed=embed)
            return
        elif skin == currently_equipped:
            embed = discord.Embed(
                title="That skin is already equipped!",
                color=0xC90000
            )
            await ctx.send(embed=embed)
            return
        await self.bot.pg_con.execute("UPDATE users SET equipped_skin = $1 WHERE uid = $2",
                                      skin, uid_string)
        embed = discord.Embed(
            title=f'Equipped {skin.capitalize()}!',
            color=0x00AD25
        )
        await ctx.send(embed=embed)


def setup(bot):  # For cog loading
    bot.add_cog(CoinFlip(bot))
