import discord
import colour
import discord.guild
import os
import sys

guild_ids = sys.argv[1:]
bot = discord.Bot()

# we need to limit the guilds for testing purposes
# so other users wouldn't see the command that we're testing

@bot.event
async def on_ready():
    print('Palette Bot is up!')
    print(f'We have logged in as {bot.user}')

@bot.slash_command(
    description="Give your name a color",
    guild_ids=guild_ids
)
async def colorme(ctx: discord.ApplicationContext, color: str):
    await color_user(ctx, ctx.user, color)

async def color_user(ctx: discord.ApplicationContext, user, color: str): # a slash command will be created with the name "ping"
    try:
        role_color = colour.Color(color)
    except ValueError:
        await ctx.respond(f"Didn't recognize color: {color} - try something else, or a specific hex code!")
        return
    print(f"Coloring {user.name} the color {role_color.web} ({role_color.get_hex()})")
    color_roles: list[discord.Role] = list(filter(lambda role: role.name.startswith('#'), ctx.guild.roles))
    current_role = next(filter(lambda role: role.name == role_color.get_hex(), color_roles), None)
    if not current_role: current_role = await new_role(ctx.guild, role_color)
    
    await user.remove_roles(*color_roles)
    await user.add_roles(current_role)
    await ctx.respond(f"Colored you {role_color.web}!")

async def new_role(guild: discord.Guild, color: colour.Color):
    new_role = await guild.create_role(
        name = color.get_hex(),
        color = discord.Color.from_rgb(
            int(color.get_red() * 255),
            int(color.get_green() * 255),
            int(color.get_blue() * 255)),
    )
    return await new_role.edit(position=max(map(lambda rule: rule.position, guild.me.roles))-2)

@bot.slash_command(
    description="Clean unused colors",
    guild_ids=guild_ids
)
async def cleanbrushes(ctx: discord.ApplicationContext):
    empty_color_roles = filter(
        lambda role: role.name.startswith('#') and len(role.members) == 0,
        ctx.guild.roles)
    for role in empty_color_roles:
        try:
            await role.delete()
        except:
            pass
    await ctx.respond("Cleaned up all empty color roles!")

bot.run(os.environ.get("DISCORD_TOKEN", "DISCORDTOKENNOTFOUND"))
