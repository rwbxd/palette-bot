import discord
import os
import sys
from create import color_user
from manage import clean_empty_color_roles
from modify import modify_hsv, modify_rgb

intents = discord.Intents.default()
intents.members = True

guild_ids = sys.argv[1:]
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    print("Palette Bot is up!")
    print(f"We have logged in as {bot.user}")


@bot.slash_command(description="Give your name a random color", guild_ids=guild_ids)
async def colormerandom(ctx: discord.ApplicationContext):
    await ctx.defer(ephemeral=True, invisible=False)
    await color_user(ctx, ctx.user, os.urandom(3).hex())


@bot.slash_command(description="Give your name a color", guild_ids=guild_ids)
async def colorme(ctx: discord.ApplicationContext, color: str):
    await ctx.defer(ephemeral=True, invisible=False)
    await color_user(ctx, ctx.user, color)


@bot.slash_command(description="Clean unused colors", guild_ids=guild_ids)
async def cleanbrushes(ctx: discord.ApplicationContext):
    await ctx.defer(ephemeral=True, invisible=False)
    await clean_empty_color_roles(ctx)


@bot.slash_command(description="Modify your current color", guild_ids=guild_ids)
async def set_hsv(
    ctx: discord.ApplicationContext,
    hue: float = None,
    saturation: float = None,
    value: float = None,
):
    await ctx.defer(ephemeral=True, invisible=False)
    await modify_hsv(ctx, hue, saturation, value)


@bot.slash_command(description="Modify your current color", guild_ids=guild_ids)
async def set_rgb(
    ctx: discord.ApplicationContext,
    r: float = None,
    g: float = None,
    b: float = None,
):
    await ctx.defer(ephemeral=True, invisible=False)
    await modify_rgb(ctx, r, g, b)


bot.run(
    os.environ.get(
        "DISCORD_TOKEN",
        "DISCORD_TOKEN_NOT_FOUND",
    )
)
