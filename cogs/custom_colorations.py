import discord
from discord.ext import commands
from database_functions import get_user, get_color
from time_parsing import format_remaining_time, parse_duration
import time
import arrow


class CustomColorations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='color', aliases=['c', 'cc'], invoke_without_command=True)
    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    async def _color(self, ctx, member: discord.Member = None):
        embed = discord.Embed()
        if not member:  # Member not specified, default to command user
            uid_string = str(ctx.author.id)
            user = await get_user(self.bot, uid_string)
            embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        else:
            uid_string = str(member.id)
            user = await get_user(self.bot, uid_string)
            embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=member.avatar_url)
        # User exists in db, proceed
        color_rid = user['color_rid']
        if color_rid is None:
            embed = discord.Embed(
                    title='You do not have a registered color',
                    color=0xFFE900
                    )
            if member is not None:  # User other than self was specified
                embed.title = 'User does not have a registered color'
            await ctx.send(embed=embed)
            return
        # User has color in db, proceed
        color = await get_color(self.bot, color_rid)
        color_type = color['type']
        role = ctx.guild.get_role(int(color_rid))
        role_color = role.color
        embed.colour = role_color
        embed.add_field(name='Color Hex', value=f'{role_color}')
        embed.set_footer(text=f'Type: {color_type.capitalize()}')
        if color_type == 'temp':
            end_time = int(color['end_time'])
            # Format time for when color expires
            end_time_string = arrow.Arrow.fromtimestamp(end_time)
            end_time_string = end_time_string.to('America/New_York')
            end_time_string = end_time_string.format("MMM D, YYYY h:mm:ss A ") + end_time_string.tzname()
            # Format time for time remaining
            remaining_time = int(end_time - time.time())
            formatted_remaining_time = format_remaining_time(remaining_time)
            # Create embed
            embed.add_field(name=f'Expires In', value=f'{formatted_remaining_time}')
            embed.add_field(name=f'Expires On', value=f'{end_time_string}')
        elif color_type == 'perm':
            embed.add_field(name=f'Expires On', value='Never')
        elif color_type == 'mod':
            embed.add_field(name=f'Expires On', value='Indefinite')
        await ctx.send(embed=embed)

    @_color.command(name='create', aliases=['c'])
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    async def color_create(self, ctx, member: discord.Member, color='000000', duration='1w'):
        guild = ctx.guild
        color = color.replace('#', '')
        try:
            color_hex = eval('0x' + color)
        except SyntaxError:
            embed = discord.Embed(
                title="Invalid hex",
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        # 'Valid' hex established
        uid_string = str(member.id)
        user = await get_user(self.bot, uid_string)
        color_rid = user['color_rid']
        if color_rid is not None:
            embed = discord.Embed(
                title=f'User already has a color!',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        # User does not have a color
        duration = parse_duration(duration)
        if not duration:  # Check for valid duration, returns False if fail
            embed = discord.Embed(
                title=f'Invalid time. Format like 7d. Supports minutes-weeks',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        # Valid duration given, create the role
        end_time = int(time.time() + duration)
        created_role = await guild.create_role(name=f"{member.name}'s Custom Coloration", color=color_hex)
        color_rid = str(created_role.id)
        await member.add_roles(created_role)  # Assign role to the user
        await self.bot.pg_con.execute("INSERT INTO colors (rid, end_time, uid) VALUES ($1, $2, $3)",
                                      color_rid, end_time, uid_string)  # Create entry
        # Update foreign key
        await self.bot.pg_con.execute("UPDATE users SET color_rid = $1 WHERE uid = $2", color_rid, uid_string)
        # Sort role into right position
        role_floor = guild.get_role(565349351933607937)  # For sorting
        await created_role.edit(position=role_floor.position)
        embed = discord.Embed(
            description=f'Successfully generated color role for {member.mention}',
            color=color_hex
        )
        await ctx.send(embed=embed)

    @_color.command(name='createmod', aliases=['cmod'])
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    async def color_createmod(self, ctx, member: discord.Member, color='000000'):
        guild = ctx.guild
        color = color.replace('#', '')
        try:
            color_hex = eval('0x' + color)
        except SyntaxError:
            embed = discord.Embed(
                title="Invalid hex",
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        # 'Valid' hex established
        uid_string = str(member.id)
        user = await get_user(self.bot, uid_string)
        color_rid = user['color_rid']
        if color_rid is not None:
            embed = discord.Embed(
                title=f'User already has a color!',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        # User does not have a color, create the role
        created_role = await guild.create_role(name=f"{member.name}'s Custom Coloration", color=color_hex)
        color_rid = str(created_role.id)
        await member.add_roles(created_role)  # Assign role to the user
        await self.bot.pg_con.execute("INSERT INTO colors (rid, type, uid) VALUES ($1, $2, $3)", color_rid, 'mod',
                                      uid_string)
        # Update foreign key
        await self.bot.pg_con.execute("UPDATE users SET color_rid = $1 WHERE uid = $2", color_rid, uid_string)
        # Sort role into right position
        role_floor = guild.get_role(332577965424640000)  # For sorting
        await created_role.edit(position=role_floor.position)
        embed = discord.Embed(
            description=f'Successfully generated color role for {member.mention}',
            color=color_hex
        )
        await ctx.send(embed=embed)

    @_color.command(name='createperm', aliases=['cperm'])
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    async def color_createperm(self, ctx, member: discord.Member, color='000000'):
        guild = ctx.guild
        color = color.replace('#', '')
        try:
            color_hex = eval('0x' + color)
        except SyntaxError:
            embed = discord.Embed(
                title="Invalid hex",
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        # 'Valid' hex established
        uid_string = str(member.id)
        user = await get_user(self.bot, uid_string)
        color_rid = user['color_rid']
        if color_rid is not None:
            embed = discord.Embed(
                title=f'User already has a color!',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        # User does not have a color, create the role
        created_role = await guild.create_role(name=f"{member.name}'s Permanent Custom Coloration", color=color_hex)
        color_rid = str(created_role.id)
        await member.add_roles(created_role)  # Assign role to the user
        await self.bot.pg_con.execute("INSERT INTO colors (rid, type, uid) VALUES ($1, $2, $3)", color_rid, 'perm',
                                      uid_string)
        # Update foreign key
        await self.bot.pg_con.execute("UPDATE users SET color_rid = $1 WHERE uid = $2", color_rid, uid_string)
        # Sort role into right position
        role_floor = guild.get_role(565349351933607937)  # For sorting
        await created_role.edit(position=role_floor.position)
        embed = discord.Embed(
            description=f'Successfully generated color role for {member.mention}',
            color=color_hex
        )
        await ctx.send(embed=embed)

    @_color.command(name='registertemp', aliases=['rt'])
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    async def color_registertemp(self, ctx, member: discord.Member, role: discord.Role, duration='1w'):
        uid_string = str(member.id)
        rid_string = str(role.id)  # Actual role id, don't confuse with current_rid, which is id associated with user
        user = await get_user(self.bot, uid_string)
        color = await self.bot.pg_con.fetchrow("SELECT * FROM colors WHERE rid = $1", rid_string)
        duration = parse_duration(duration)
        if not duration:  # Check for valid duration, returns False if fail
            embed = discord.Embed(
                title=f'Invalid time. Format like `1w`. Supports minutes-weeks',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        end_time = int(time.time() + duration)
        # Valid duration, check if they have a color already and update database
        current_rid = user['color_rid']  # ID associated with the user
        if current_rid is None:  # No color registered but role exists
            # Check if role is already registered under another user
            if color:
                embed = discord.Embed(
                    description=f'Role is already registered to <@{color["uid"]}>',
                    color=0xFFE900
                )
                await ctx.send(embed=embed)
                return
            # Role exists and not registered anywhere, user has no registered color. Safe to add
            await self.bot.pg_con.execute("INSERT INTO colors (rid, end_time, uid) VALUES ($1, $2, $3)",
                                          rid_string, end_time, uid_string)  # Create entry
            # Update foreign key
            await self.bot.pg_con.execute("UPDATE users SET color_rid = $1 WHERE uid = $2", rid_string, uid_string)
            embed = discord.Embed(
                description=f'Successfully registered temp color for {member.mention}',
                color=role.color
            )
            await ctx.send(embed=embed)
        else:  # User has color registered
            if rid_string != current_rid:  # User has registered role other than one provided
                embed = discord.Embed(
                    title=f'User already has registered color not matching the one provided',
                    color=0xFFE900
                )
                await ctx.send(embed=embed)
                return
            color_type = color['type']
            if color_type == 'temp':
                embed = discord.Embed(
                    title=f'Coloration is already registered as a temp color',
                    color=0xFFE900
                )
                await ctx.send(embed=embed)
                return
            # User has a non-temp color registered. Change the type
            await self.bot.pg_con.execute("UPDATE colors SET type = $1, end_time = $2 WHERE rid = $3",
                                          'temp', end_time, rid_string)
            embed = discord.Embed(
                description=f'Successfully switched color type from **{color_type}** to **temp** for {member.mention}',
                color=role.color
            )
            await ctx.send(embed=embed)

    @_color.command(name='registermod', aliases=['rm'])
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    async def color_registermod(self, ctx, member: discord.Member, role: discord.Role = None):
        uid_string = str(member.id)
        user = await get_user(self.bot, uid_string)
        current_rid = user['color_rid']
        if not current_rid:  # User has no registered coloration
            if role is None:
                embed = discord.Embed(
                    title=f'User does not have a registered color to update. Provide role as an arg if it exists',
                    color=0xFFE900
                )
                await ctx.send(embed=embed)
                return
            # Role provided
            rid_string = str(role.id)
            color_fetch = await self.bot.pg_con.fetchrow("SELECT * FROM colors WHERE rid = $1", rid_string)
            if color_fetch:
                embed = discord.Embed(
                    description=f'Role is already registered to <@{color_fetch["uid"]}>',
                    color=0xFFE900
                )
                await ctx.send(embed=embed)
                return
            # Role is not registered anywhere, user has no registered color. Safe to add
            await self.bot.pg_con.execute("INSERT INTO colors (rid, type, uid) VALUES ($1, $2, $3)",
                                          rid_string, 'mod', uid_string)  # Create entry
            # Update foreign key
            await self.bot.pg_con.execute("UPDATE users SET color_rid = $1 WHERE uid = $2", rid_string, uid_string)
            embed = discord.Embed(
                description=f'Successfully registered mod color for {member.mention}',
                color=role.color
            )
            await ctx.send(embed=embed)
            return
        else:  # User has a registered coloration
            if role:  # If a role was provided (though unnecessarily), make sure it's the right one
                rid_string = str(role.id)
                if rid_string != current_rid:  # User has registered role other than one provided
                    embed = discord.Embed(
                        title=f'User already has registered color not matching the one provided',
                        color=0xFFE900
                    )
                    await ctx.send(embed=embed)
                    return
            color = await get_color(self.bot, current_rid)
            color_type = color['type']
            if color_type == 'mod':
                embed = discord.Embed(
                    title=f'Coloration is already registered as a mod color',
                    color=0xFFE900
                )
                await ctx.send(embed=embed)
                return
            # User has a non-mod color registered. Change the type
            await self.bot.pg_con.execute("UPDATE colors SET type = $1, end_time = null WHERE rid = $2",
                                          'mod', current_rid)
            role = ctx.guild.get_role(int(current_rid))
            embed = discord.Embed(
                description=f'Successfully switched color type from **{color_type}** to **mod** for {member.mention}',
                color=role.color
            )
            await ctx.send(embed=embed)

    @_color.command(name='registerperm', aliases=['rp'])
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    async def color_registerperm(self, ctx, member: discord.Member, role: discord.Role = None):
        uid_string = str(member.id)
        user = await get_user(self.bot, uid_string)
        current_rid = user['color_rid']
        if not current_rid:  # User has no registered coloration
            if role is None:
                embed = discord.Embed(
                    title=f'User does not have a registered color to update. Provide role as an arg if it exists',
                    color=0xFFE900
                )
                await ctx.send(embed=embed)
                return
            # Role provided
            rid_string = str(role.id)
            color_fetch = await self.bot.pg_con.fetchrow("SELECT * FROM colors WHERE rid = $1", rid_string)
            if color_fetch:
                embed = discord.Embed(
                    description=f'Role is already registered to <@{color_fetch["uid"]}>',
                    color=0xFFE900
                )
                await ctx.send(embed=embed)
                return
            # Role is not registered anywhere, user has no registered color. Safe to add
            await self.bot.pg_con.execute("INSERT INTO colors (rid, type, uid) VALUES ($1, $2, $3)",
                                          rid_string, 'perm', uid_string)  # Create entry
            # Update foreign key
            await self.bot.pg_con.execute("UPDATE users SET color_rid = $1 WHERE uid = $2", rid_string, uid_string)
            embed = discord.Embed(
                description=f'Successfully registered perm color for {member.mention}',
                color=role.color
            )
            await ctx.send(embed=embed)
            return
        else:  # User has a registered coloration
            if role:  # If a role was provided (though unnecessarily), make sure it's the right one
                rid_string = str(role.id)
                if rid_string != current_rid:  # User has registered role other than one provided
                    embed = discord.Embed(
                        title=f'User already has registered color not matching the one provided',
                        color=0xFFE900
                    )
                    await ctx.send(embed=embed)
                    return
            color = await get_color(self.bot, current_rid)
            color_type = color['type']
            if color_type == 'perm':
                embed = discord.Embed(
                    title=f'Coloration is already registered as a perm color',
                    color=0xFFE900
                )
                await ctx.send(embed=embed)
                return
            # User has a non-perm color registered. Change the type
            await self.bot.pg_con.execute("UPDATE colors SET type = $1, end_time = null WHERE rid = $2",
                                          'perm', current_rid)
            role = ctx.guild.get_role(int(current_rid))
            embed = discord.Embed(
                description=f'Successfully switched color type from **{color_type}** to **perm** for {member.mention}',
                color=role.color
            )
            await ctx.send(embed=embed)

    @_color.command(name='remove', aliases=['delete', 'd', 'r'])
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    async def color_remove(self, ctx, member: discord.Member):
        uid_string = str(member.id)
        user = await get_user(self.bot, uid_string)
        color_rid = user['color_rid']
        if color_rid is None:
            embed = discord.Embed(
                title="User does not have a coloration",
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        # They do have a coloration
        await self.bot.pg_con.execute("UPDATE users SET color_rid = null WHERE uid = $1", uid_string)
        await self.bot.pg_con.execute("DELETE FROM colors WHERE rid = $1", color_rid)
        role = ctx.guild.get_role(int(color_rid))
        if role is not None:
            await role.delete()
            embed = discord.Embed(
                title="Successfully deleted color role",
                color=0x00AD25
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Role not found, but cleared database entry",
                color=0x00AD25
            )
            await ctx.send(embed=embed)

    @color_remove.error
    async def color_remove_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            uid_string = ctx.message.content.split()[2]  # Get the member id
            if not uid_string.isnumeric():
                embed = discord.Embed(
                    title="If user is not in the server, uid must be used",
                    color=0xFFE900
                )
                await ctx.send(embed=embed)
                return
            user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE uid = $1", uid_string)  # Returns record
            if not user:  # User not in database
                embed = discord.Embed(
                    title="User not found",
                    color=0xFFE900
                )
                await ctx.send(embed=embed)
                return
            # User exists in database
            color_rid = user['color_rid']
            if color_rid is None:  # User does not have a coloration in db
                embed = discord.Embed(
                    title="User does not have a coloration",
                    color=0xFFE900
                )
                await ctx.send(embed=embed)
                return
            # At this point, we know it's a user that left the server but has a db entry and a coloration
            await self.bot.pg_con.execute("UPDATE users SET color_rid = null WHERE uid = $1", uid_string)
            await self.bot.pg_con.execute("DELETE FROM colors WHERE rid = $1", color_rid)
            role = ctx.guild.get_role(int(color_rid))
            if role is not None:
                await role.delete()
                embed = discord.Embed(
                    title="Successfully deleted color role",
                    color=0x00AD25
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Role not found, but cleared database entry",
                    color=0x00AD25
                )
                await ctx.send(embed=embed)
            error.error_handled = True

    @_color.command(name='softremove', aliases=['sr'])
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    async def color_softremove(self, ctx, member: discord.Member):
        uid_string = str(member.id)
        user = await get_user(self.bot, uid_string)
        color_rid = user['color_rid']
        if color_rid is None:
            embed = discord.Embed(
                title="User does not have a coloration",
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        # They do have a coloration
        await self.bot.pg_con.execute("UPDATE users SET color_rid = null WHERE uid = $1", uid_string)
        await self.bot.pg_con.execute("DELETE FROM colors WHERE rid = $1", color_rid)
        embed = discord.Embed(
            title="Successfully deleted database entry for coloration",
            color=0x00AD25
        )
        await ctx.send(embed=embed)

    @color_softremove.error
    async def color_softremove_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            uid_string = ctx.message.content.split()[2]  # Get the member id
            if not uid_string.isnumeric():
                embed = discord.Embed(
                    title="If user is not in the server, uid must be used",
                    color=0xFFE900
                )
                await ctx.send(embed=embed)
                return
            user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE uid = $1", uid_string)  # Returns record
            if not user:  # Empty
                embed = discord.Embed(
                    title="User not found",
                    color=0xFFE900
                )
                await ctx.send(embed=embed)
                return
            # User exists in database
            color_rid = user['color_rid']
            if color_rid is None:  # User does not have a coloration in db
                embed = discord.Embed(
                    title="User does not have a coloration",
                    color=0xFFE900
                )
                await ctx.send(embed=embed)
                return
            # At this point, we know it's a user that left the server but has a db entry and a coloration
            await self.bot.pg_con.execute("UPDATE users SET color_rid = null WHERE uid = $1", uid_string)
            await self.bot.pg_con.execute("DELETE FROM colors WHERE rid = $1", color_rid)
            embed = discord.Embed(
                title="Successfully deleted database entry for coloration",
                color=0x00AD25
            )
            await ctx.send(embed=embed)
            error.error_handled = True

    @_color.command(name='extend', aliases=['e'])
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    async def color_extend(self, ctx, member: discord.Member, duration='1w'):
        uid_string = str(member.id)
        user = await get_user(self.bot, uid_string)
        color_rid = user['color_rid']
        if color_rid is None:
            embed = discord.Embed(
                title="User does not have a coloration",
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        # User has coloration
        color = await get_color(self.bot, color_rid)
        duration = parse_duration(duration)
        if not duration:  # Check for valid duration, returns False if fail
            embed = discord.Embed(
                title=f'Invalid time. Format like 7d. Supports minutes-weeks',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        # Valid duration given
        end_time = int(color['end_time'])
        await self.bot.pg_con.execute("UPDATE colors SET end_time = $1 WHERE rid = $2", end_time + duration, color_rid)
        embed = discord.Embed(
            title=f'Successfully edited color duration!',
            color=0x00AD25
        )
        await ctx.send(embed=embed)

    @_color.command(name='reduce')
    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    async def color_reduce(self, ctx, member: discord.Member, duration='1w'):
        uid_string = str(member.id)
        user = await get_user(self.bot, uid_string)
        color_rid = user['color_rid']
        if color_rid is None:
            embed = discord.Embed(
                title="User does not have a coloration",
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        # User has coloration
        color = await get_color(self.bot, color_rid)
        duration = parse_duration(duration)
        if not duration:  # Check for valid duration, returns False if fail
            embed = discord.Embed(
                title=f'Invalid time. Format like 7d. Supports minutes-weeks',
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        # Valid duration given
        end_time = int(color['end_time'])
        await self.bot.pg_con.execute("UPDATE colors SET end_time = $1 WHERE rid = $2", end_time - duration, color_rid)
        embed = discord.Embed(
            title=f'Successfully edited color duration!',
            color=0x00AD25
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['cl'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def colors(self, ctx):
        color_fetch = await self.bot.pg_con.fetch("SELECT * FROM colors WHERE type = 'temp' ORDER BY end_time")
        if not color_fetch:  # There are none
            embed = discord.Embed(
                description="No active temp colors recorded",
                color=0xC90000
            )
            await ctx.send(embed=embed)
            return
        # At least 1 color exists
        embed = discord.Embed(
            title='Active Temp Colors',
            color=0x00AD25
        )
        color_role_display = []
        for color in color_fetch:
            uid_string = color['uid']
            user = ctx.guild.get_member(int(uid_string))
            end_time = int(color['end_time'])
            end_time_string = arrow.Arrow.fromtimestamp(int(color['end_time']))
            end_time_string = end_time_string.to('America/New_York')
            end_time_string = end_time_string.format("MMM D, YYYY h:mm:ss A ") + end_time_string.tzname()
            remaining_time = int(end_time - time.time())
            formatted_remaining_time = format_remaining_time(remaining_time)
            if user is not None:
                color_role_display.append(f'**{user.mention}**: `{end_time_string}` [{formatted_remaining_time}]')
            else:
                color_role_display.append(f'**[User left: {uid_string}]**: `{end_time_string}` '
                                          f'[{formatted_remaining_time}]')
        display = '\n'.join(color_role_display)
        embed.description = f'{display}'
        await ctx.send(embed=embed)
        return

    @commands.command(aliases=['mc'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def modcolors(self, ctx):
        color_fetch = await self.bot.pg_con.fetch("SELECT * FROM colors WHERE type = 'mod'")
        if not color_fetch:  # There are none
            embed = discord.Embed(
                description="No mod colors recorded",
                color=0xC90000
            )
            await ctx.send(embed=embed)
            return
        # At least 1 color exists
        embed = discord.Embed(
            title='Moderator Colorations',
            color=0x00AD25
        )
        color_role_display = []
        for color in color_fetch:
            uid_string = color['uid']
            rid_string = color['rid']
            user = ctx.guild.get_member(int(uid_string))
            user_string = f'{user.mention}' if user else f'**[User left: {uid_string}]**'
            role = ctx.guild.get_role(int(rid_string))
            color_string = f'**[{role.color}]**' if role else '**[Role not found]**'
            color_role_display.append(f'{color_string} {user_string}')
        display = '\n'.join(color_role_display)
        embed.description = f'{display}'
        await ctx.send(embed=embed)
        return

    @commands.command(aliases=['pc'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def permacolors(self, ctx):
        color_fetch = await self.bot.pg_con.fetch("SELECT * FROM colors WHERE type = 'perm'")
        if not color_fetch:  # There are none
            embed = discord.Embed(
                description="No perma colors recorded",
                color=0xC90000
            )
            await ctx.send(embed=embed)
            return
        # At least 1 color exists
        embed = discord.Embed(
            title='Permanent Colorations',
            color=0x00AD25
        )
        color_role_display = []
        for color in color_fetch:
            uid_string = color['uid']
            rid_string = color['rid']
            user = ctx.guild.get_member(int(uid_string))
            user_string = f'{user.mention}' if user else f'**[User left: {uid_string}]**'
            role = ctx.guild.get_role(int(rid_string))
            color_string = f'**[{role.color}]**' if role else '**[Role not found]**'
            color_role_display.append(f'{color_string} {user_string}')
        display = '\n'.join(color_role_display)
        embed.description = f'{display}'
        await ctx.send(embed=embed)
        return

    @commands.command(aliases=['sc'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def setcolor(self, ctx, color):
        color = color.replace('#', '')
        try:
            color_hex = eval('0x' + color)
        except SyntaxError:
            embed = discord.Embed(
                title="Invalid hex",
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        # 'Valid' hex established
        uid_string = str(ctx.author.id)
        user = await get_user(self.bot, uid_string)
        color_rid = user['color_rid']
        if color_rid is None:
            embed = discord.Embed(
                title=f"You don't have a coloration",
                color=0xFFE900
            )
            await ctx.send(embed=embed)
            return
        # User has a color
        role = ctx.guild.get_role(int(color_rid))
        if role is None:
            embed = discord.Embed(
                title="Role not found (Error code 1)",
                color=0x00AD25
            )
        await role.edit(color=color_hex)
        embed = discord.Embed(
            title="Successfully changed role color",
            color=0x00AD25
        )
        await ctx.send(embed=embed)

    @_color.command(name='help', aliases=['h'])
    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    async def color_help(self, ctx):
        embed = discord.Embed(
            color=0x00AD25
        )
        embed.add_field(name='.color help', value='Prints help for command')
        embed.add_field(name='.color create <user id/mention> <color hex> <duration>', value=
                             '**- Example: .color create @Silicrex c21a1a 1w**\n'
                             '- Duration defaults to 1w\n'
                             '- Creates role and sorts it above event host\n'
                             '- Assigns role automatically\n'
                             '- Alias of `.c c <user id/mention> <color hex> <duration>`\n'
                             '- For perm/mod colors, use `createperm`/`createmod` (same but no duration)', inline=False)
        embed.add_field(name='.color registertemp <user id/mention> <role id/mention> <duration>',
                        value='- Registers already-existing role to database\n'
                              '- If role is already registered to them, will switch type to temp\n'
                              '- Duration can be left blank and defaults to 1w\n'
                              '- Has alias `.c rt <user id/mention>`', inline=False)
        embed.add_field(name='.color registerperm <user id/mention> <role id/mention>',
                        value='- Registers already-existing role to database\n'
                              '- If role is already registered to them, will switch type to perm\n'
                              '- `registermod` for mod colors\n'
                              '- Has alias `.c rp <user id/mention>`', inline=False)
        embed.add_field(name='.color remove <user id/mention>',
                        value='- Deletes color role\n'
                              '- Has alias `.c r <user id/mention>`', inline=False)
        embed.add_field(name='.color softremove <user id/mention>',
                        value='- Deletes database entry\n'
                              '- Has alias `.c sr <user id/mention>`', inline=False)
        embed.add_field(name='.color extend <user id/mention> <duration>',
                        value="- Extends user's coloration by given duration\n"
                              "- Defaults to 1w\n"
                              "- Has alias `.c e <user id/mention> <duration>`", inline=False)
        embed.add_field(name='.color reduce <user id/mention> <duration>',
                        value="- Reduces user's coloration by given duration", inline=False)
        embed.add_field(name='.color (<user>)',
                        value='- Shows info about your color role; or another user if given\n'
                              '- Has alias `c`',
                        inline=False)
        embed.add_field(name='.colors',
                        value='- Displays active temp color roles and their remaining durations\n'
                              '- Has alias `cl`\n'
                              '- Use `permacolors`/`modcolors` for the other types',
                        inline=False)
        await ctx.send(embed=embed)
        return


def setup(bot):
    bot.add_cog(CustomColorations(bot))
