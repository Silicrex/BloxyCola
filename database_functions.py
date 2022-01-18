async def get_user(bot, uid_string):  # Returns user data, creates entry if not in database
    user_fetch = await bot.pg_con.fetchrow("SELECT * FROM users WHERE uid = $1", uid_string)  # Returns record
    member = bot.get_user(int(uid_string))
    if not user_fetch:  # User is not in db
        await bot.pg_con.execute("INSERT INTO users (uid) VALUES ($1)", uid_string)  # Create entry
        user_fetch = await bot.pg_con.fetchrow("SELECT * FROM users WHERE uid = $1", uid_string)
        print(f'Generated record for {member.name}#{member.discriminator}')
    return user_fetch


async def get_color(bot, rid_string):  # Returns color data
    color_fetch = await bot.pg_con.fetchrow("SELECT * FROM colors WHERE rid = $1", rid_string)  # Returns record
    if color_fetch:
        return color_fetch
    else:  # Color is not in db
        print(f'{rid_string} does not exist')
        return None
