import discord
from discord.ext import commands
import os
import json


class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def servers(self, ctx):
        active_servers = self.bot.guilds
        embed = discord.Embed(
            title='I am currently in..'
        )
        server_list = []
        for guild in active_servers:
            server_list.append(f'{guild.name}: {guild.id}')
        server_list = '\n'.join(server_list)
        embed.description = server_list
        await ctx.send(embed=embed)

    @commands.command(aliases=['ext'])
    @commands.is_owner()
    async def extensions(self, ctx):
        all_extensions = []
        for filename in os.listdir('./cogs'):  # Get list of all extensions
            if filename.endswith('.py'):
                all_extensions.append(f'{filename[:-3]}')

        # Get list of loaded extensions; unloaded extensions is the difference between all/loaded
        loaded_extensions = [x[5:] for x in self.bot.extensions]  # [5:] because string starts with cogs.
        unloaded_extensions = list(set(all_extensions) - set(loaded_extensions))

        # Setting up in list first is cleaner than repeatedly appending onto a string
        extensions_status = ['**Loaded extensions:**']
        extensions_status.extend(loaded_extensions)
        extensions_status.append('\n**Unloaded extensions:**')
        extensions_status.extend(unloaded_extensions)

        embed = discord.Embed(description='\n'.join(extensions_status))
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def test(self, ctx):
        pass

    # @commands.group(invoke_without_command=True)
    # @commands.has_permissions(manage_guild=True)
    # async def migrate_colorations(self, ctx):
    #     with open('color_data.json') as file:
    #         color_data = json.load(file)
    #     print(type(color_data))
    #     print(color_data)
    #     print('GO!')
    #     print('pls print r u rdy this time')
    #     for key, value in color_data.items():
    #         uid_string = key
    #         end_time = value['end_time']
    #         color_rid = str(value['role_id'])
    #         await self.bot.pg_con.execute("INSERT INTO colors (rid, end_time, uid) VALUES ($1, $2, $3)",
    #                                       color_rid, end_time, uid_string)  # Create entry
    #         await self.bot.pg_con.execute("UPDATE users SET color_rid = $1 WHERE uid = $2", color_rid, uid_string)
    #     print('DONE!')

    # @commands.group(invoke_without_command=True)
    # @commands.has_permissions(manage_guild=True)
    # async def migrate_user_data(self, ctx):
    #     with open('user_data.json') as file:
    #         user_data = json.load(file)
    #     print(type(user_data))
    #     print('GO USERS!')
    #     print('r u ready....')
    #     for key, value in user_data.items():
    #         uid_string = key
    #         await self.bot.pg_con.execute("INSERT INTO users (uid, heads, current_heads_streak, best_heads_streak, "
    #                                       "last_best_heads_streak, heads_streaks, tails, current_tails_streak, "
    #                                       "best_tails_streak, last_best_tails_streak, tails_streaks, skin_inv, "
    #                                       "equipped_skin, last_skin_unlock) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, "
    #                                       "$9, $10, $11, $12, $13, $14)",
    #                                       uid_string, value['heads'], value['current_heads_streak'], value['best_heads_streak'],
    #                                       value['last_best_heads_streak'], str(value['heads_streaks']), value['tails'],
    #                                       value['current_tails_streak'], value['best_tails_streaks'], value['last_best_tails_streak'],
    #                                       str(value['tails_streaks']), value['skin_inv'], value['equipped_skin'], value['last_skin_unlock'])
    #
    #     print('DONE!')
    
    # @commands.group(invoke_without_command=True)
    # @commands.has_permissions(manage_guild=True)
    # async def hot_fix(self, ctx):
    #     stats_fetch = await self.bot.pg_con.fetch("SELECT * FROM users")
    #     for user in stats_fetch:
    #         heads_streaks = eval(user['heads_streaks'])  # Dict
    #         tails_streaks = eval(user['tails_streaks'])  # Dict
    #         new_heads = {}
    #         for key, value in heads_streaks.items():  # Key could be int or str
    #             int_key = int(key)
    #             new_heads[int_key] = new_heads.get(int_key, 0) + value
    #         new_tails = {}
    #         for key, value in tails_streaks.items():  # Key could be int or str
    #             int_key = int(key)
    #             new_tails[int_key] = new_tails.get(int_key, 0) + value
    #         new_heads = str(new_heads)
    #         new_tails = str(new_tails)
    #         await self.bot.pg_con.execute("UPDATE users SET heads_streaks = $1, tails_streaks = $2 WHERE uid = $3",
    #                                 new_heads, new_tails, user['uid'])
    #     print('doneeeeeezoooo')


def setup(bot):
    bot.add_cog(Testing(bot))
