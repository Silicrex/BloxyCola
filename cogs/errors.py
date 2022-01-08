import discord
from discord.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        elif isinstance(error, commands.NotOwner):
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
        # elif isinstance(error, commands.MissingRequiredArgument):
        #     msg = ctx.message.content
        #     command = str(self.bot.get_command(msg[1:]))  # Remove prefix, convert aliases to full command
        #     help_dict = get_help_dict()
        #     embed = get_help_embed(help_dict, command)
        #     await ctx.send(embed=embed)
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


def setup(bot):
    bot.add_cog(Errors(bot))
