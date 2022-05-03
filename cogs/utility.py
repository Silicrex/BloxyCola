import discord
from discord.ext import commands
import time  # For ping command
from datetime import datetime as Datetime
from time_parsing import format_remaining_time
from help import get_help_embed, get_modhelp_embed, get_general_help_embed, get_general_mod_help_embed


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
        welcome_channel = self.bot.get_channel(971157537338576927)

        # Check account age
        now = Datetime.utcnow()
        created_at = member.created_at
        print(f'created_at = {created_at}')
        account_age = now - created_at
        account_age_seconds = account_age.total_seconds()
        print(f'{member}: {account_age_seconds} seconds')
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
                               f"If you are ever in need of any assistance, don't hesitate to contact a moderator! "
                               f"In the meantime, meet our <@&971156512766574642>!")
        else:  # User has Bloxy Cola stats
            welcome_message = (f"Welcome back to Fanmade, {member.mention}! "
                               f"As always; rules in <#643330454568697858>, "
                               f"verify in <#775404743480705105>, "
                               f"and don't hesitate to contact a moderator if you need anything! "
                               f"Say hello to the <@&971156512766574642>!")
        await welcome_channel.send(welcome_message)

    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def ping(self, ctx):  # Check latency
        start_time = time.monotonic()  # Start monotonic clock
        sent_message = await ctx.send('Pong!')  # Send message
        time_difference = time.monotonic() - start_time
        await sent_message.edit(content='Pong! {:.0f} ms'.format(time_difference * 1000))  # Edit time diff in as ms

    @commands.command(aliases=['h'])
    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    async def help(self, ctx, *, arg1=None):
        if arg1 is None:  # Then print general help
            embed = get_general_help_embed(self.bot)
            await ctx.send(embed=embed)
        else:
            arg1 = str(self.bot.get_command(arg1))  # Convert aliases to full command
            embed = get_help_embed(arg1)
            await ctx.send(embed=embed)

    @commands.command(aliases=['mh'])
    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    async def modhelp(self, ctx, *, arg1=None):
        if arg1 is None:  # Then print general modhelp
            embed = get_general_mod_help_embed(self.bot)
            await ctx.send(embed=embed)
        else:
            arg1 = str(self.bot.get_command(arg1))  # Convert aliases to full command
            embed = get_modhelp_embed(arg1)
            await ctx.send(embed=embed)


def setup(bot):  # For cog loading
    bot.add_cog(Utility(bot))
