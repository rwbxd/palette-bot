import discord
import colour


async def create_new_role(
    guild: discord.Guild, color: colour.Color
) -> discord.Role | None:
    try:
        new_role = await guild.create_role(
            name=color.get_hex(),
            color=discord.Color.from_rgb(
                int(color.get_red() * 255),
                int(color.get_green() * 255),
                int(color.get_blue() * 255),
            ),
        )
        log_info(f"Successfully created new role {color.get_hex()}")
    except (discord.Forbidden, discord.HTTPException, discord.InvalidArgument) as e:
        log_error(f"Failed to create role {color.get_hex()} with {e.text}")
        return None

    try:
        return await new_role.edit(
            position=max([role.position for role in guild.me.roles]) - 2
        )
    except (discord.Forbidden, discord.HTTPException, discord.InvalidArgument) as e:
        log_error(f"Failed to move role {color.get_hex()} with {e.text}")
        return new_role


async def delete_role(role: discord.Role) -> bool:
    try:
        await role.delete()
        return True
    except:
        log_error(f"Failed to delete role {role.name}")
        return False


async def update_role(
    role: discord.Role, name: str = None, color: discord.Colour = None
) -> bool:
    try:
        log_info(
            f"Editing role {role.name} with name: {name or role.name} and color: {color or role.color}"
        )
        await role.edit(name=name or role.name, color=color or role.color)
        return True
    except:
        log_error(
            f"Failed to update role {role.name} with name: {name or role.name} and color: {color or role.color}"
        )
        return False


async def error_and_respond(ctx: discord.ApplicationContext, message: str):
    log_error(message)
    return await ctx.respond(f"{message}, please try again in a few seconds")


async def log_and_respond(ctx: discord.ApplicationContext, message: str):
    log_info(message)
    return await ctx.respond(message)


def log_error(message: str):
    print(f"ERROR: {message}")


def log_info(message: str):
    print(f"INFO: {message}")


def get_current_color(user: discord.Member | discord.User) -> discord.Role | None:
    return next((role for role in user.roles if role.name.startswith("#")), None)
