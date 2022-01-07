async def get_user(bot, uid_string):  # Returns user data, creates entry if not in database
    user_fetch = await bot.pg_con.fetch("SELECT * FROM users WHERE uid = $1", uid_string)  # Returns list
    member = bot.get_user(int(uid_string))
    if user_fetch:
        user = user_fetch[0]
    else:  # User is not in db
        await bot.pg_con.execute("INSERT INTO users (uid) VALUES ($1)", uid_string)  # Create entry
        user = await bot.pg_con.fetchrow("SELECT * FROM users WHERE uid = $1", uid_string)
        print(f'Generated record for {member.name}#{member.discriminator}')
    return user


async def get_color(bot, rid_string):  # Returns color data
    color_fetch = await bot.pg_con.fetch("SELECT * FROM colors WHERE rid = $1", rid_string)  # Returns list
    if color_fetch:
        color = color_fetch[0]
        return color
    else:  # Color is not in db
        print(f'{rid_string} does not exist')
        return None
