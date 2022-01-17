import discord
from discord.ext import commands
import os
import calendar
import json
from datetime import datetime as Datetime
import pytz

if not os.path.isfile('month.json'):  # Json for keeping track of current month
    est = pytz.timezone('America/New_York')
    est_date = Datetime.now(est)
    with open('month.json', 'w') as file:
        json.dump(calendar.month_name[est_date.month], file)
if not os.path.isfile('boost_redeems.json'):  # Json for keeping track of who's redeemed this month
    with open('boost_redeems.json', 'w') as file:
        json.dump([], file)


class BoostRedeems(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['br'], invoke_without_command=False)
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    async def boostredeem(self, ctx):
        est = pytz.timezone('America/New_York')
        est_date = Datetime.now(est)
        current_month = calendar.month_name[est_date.month]

        with open('month.json') as file:  # To check if stored month is still accurate
            calendar_month = json.load(file)

        if calendar_month != current_month:  # Month ticked over
            with open('month.json', 'w') as file:
                json.dump(current_month, file)
            with open('boost_redeems.json', 'w') as file:
                json.dump([], file)  # Reset
            await ctx.send('Month has changed, resetting list..')
        else:
            print(f'Still in {calendar_month} :)')

        if ctx.invoked_subcommand is None:
            with open('boost_redeems.json') as file:
                boost_redeems = json.load(file)
            uid_string = str(ctx.author.id)
            if uid_string not in boost_redeems:
                nitro_booster = ctx.guild.get_role(585530835957186560)
                if nitro_booster in ctx.author.roles:
                    title = 'You are eligible to redeem a 7d custom coloration! Ask a moderator!'
                else:
                    title = 'Boost Redeems are for Nitro Boosters of the server!'
            else:
                title = 'You have redeemed your monthly Nitro Booster coloration already!'
            embed = discord.Embed(
                title=title,
                color=0x00AD25
            )
            embed.set_author(name=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @boostredeem.command(name='list', aliases=['l'])
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    async def boostredeem_list(self, ctx):
        with open('month.json') as file:
            calendar_month = json.load(file)
        with open('boost_redeems.json') as file:
            boost_redeems = json.load(file)
        uid_string = str(ctx.author.id)
        embed = discord.Embed(
            title=f'[{calendar_month}] Redeemed Booster Colorations',
            color=0x00AD25
        )
        if not boost_redeems:
            embed.description = 'No redeems yet!'
        else:
            embed.description = '\n'.join([f'<@{x}>' for x in boost_redeems])
        if uid_string not in boost_redeems:
            nitro_booster = ctx.guild.get_role(585530835957186560)
            if nitro_booster in ctx.author.roles:
                embed.set_footer(text='You are eligible to redeem a 7d custom coloration! Ask a moderator!',
                                 icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @boostredeem.command(name='add', aliases=['a'])
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    async def boostredeem_add(self, ctx, member: discord.Member):
        with open('boost_redeems.json') as file:
            boost_redeems = json.load(file)
        uid_string = str(member.id)
        if uid_string in boost_redeems:
            embed = discord.Embed(
                title='User has already redeemed this month',
                color=0xC90000
            )
            await ctx.send(embed=embed)
            return
        # User has not redeemed this month
        boost_redeems.append(uid_string)
        with open('boost_redeems.json', 'w') as file:
            json.dump(boost_redeems, file)
        embed = discord.Embed(
            title='Successfully registered redeem',
            description=f'{member.mention}',
            color=0x00AD25
        )
        await ctx.send(embed=embed)

    @boostredeem.command(name='remove', aliases=['r'])
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    async def boostredeem_remove(self, ctx, member: discord.Member):
        with open('boost_redeems.json') as file:
            boost_redeems = json.load(file)
        uid_string = str(member.id)
        if uid_string not in boost_redeems:
            embed = discord.Embed(
                title='User already not in list',
                color=0xC90000
            )
            await ctx.send(embed=embed)
            return
        boost_redeems.remove(uid_string)
        with open('boost_redeems.json', 'w') as file:
            json.dump(boost_redeems, file)
        embed = discord.Embed(
            title='Successfully removed user',
            description=f'{member.mention}',
            color=0x00AD25
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BoostRedeems(bot))
