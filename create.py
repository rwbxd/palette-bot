import discord
import re
import colour
from util import create_new_role, error_and_respond, log_info


async def color_user(
    ctx: discord.ApplicationContext,
    user: discord.Member | discord.User,
    color_string: str,
):
    try:
        assert (
            type(ctx.guild) is discord.Guild
        ), "Encountered an issue accessing the Discord guild"

        color_string = color_string.strip().replace(" ", "")
        if re.search("^[a-f0-9]{3}$|^[a-f0-9]{6}$", color_string, re.IGNORECASE):
            color_string = "#" + color_string

        try:
            role_color = colour.Color(color_string)
        except ValueError:
            return await ctx.respond(
                f"Didn't recognize color: {color_string} - try something else, or a specific hex code!"
            )

        log_info(
            f"Coloring {user.name} the color {role_color.web} ({role_color.get_hex()})"
        )

        all_color_roles: list[discord.Role] = [
            role for role in ctx.guild.roles if role.name.startswith("#")
        ]
        desired_color_role = next(
            (role for role in all_color_roles if role.name == role_color.get_hex()),
            None,
        ) or await create_new_role(ctx.guild, role_color)
        if desired_color_role is None:
            return await error_and_respond(
                ctx, f"Failed to create new role for color: {color_string}"
            )

        await user.remove_roles(*all_color_roles)
        await user.add_roles(desired_color_role)
        return await ctx.respond(f"Colored you {role_color.web}!")

    except AssertionError as errorMessage:
        return await error_and_respond(ctx, errorMessage)
