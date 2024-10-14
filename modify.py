import colour
import colorsys
import discord
from util import get_current_color, log_and_respond, update_role
from create import color_user


async def modify_rgb(
    ctx: discord.ApplicationContext,
    r: int = None,
    g: int = None,
    b: int = None,
):
    user: discord.User | discord.Member = ctx.user
    role = get_current_color(user)
    new_color = discord.Colour.from_rgb(
        int(constrain(0, r if r is not None else role.color.r, 255)),
        int(constrain(0, g if g is not None else role.color.g, 255)),
        int(constrain(0, b if b is not None else role.color.b, 255)),
    )

    return await modify_color(ctx, role, new_color)


async def modify_hsv(
    ctx: discord.ApplicationContext,
    hue: float | None = None,
    saturation: float | None = None,
    value: float | None = None,
):
    user: discord.User | discord.Member = ctx.user
    role = get_current_color(user)
    r, g, b = role.color.to_rgb()
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    new_color = discord.Colour.from_hsv(
        constrain(0, hue if hue is not None else h, 1),
        constrain(0, saturation if saturation is not None else s, 1),
        constrain(0, value if value is not None else v, 1),
    )

    return await modify_color(ctx, role, new_color)


async def modify_color(
    ctx: discord.ApplicationContext, role: discord.Role, new_color: discord.Colour
):
    user: discord.User | discord.Member = ctx.user
    role = get_current_color(user)

    if len(role.members) > 1:
        return await color_user(ctx, ctx.user, str(new_color))
    else:
        await update_role(role, name=str(new_color), color=new_color)
        return await log_and_respond(
            ctx, f"Modified {user.name}'s current color to {str(new_color)}"
        )


def constrain(min_value, value, max_value):
    return min(max(value, min_value), max_value)
