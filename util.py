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
        logInfo(f"Successfully created new role {color.get_hex()}")
    except (discord.Forbidden, discord.HTTPException, discord.InvalidArgument) as e:
        logError(f"Failed to create role {color.get_hex()} with {e.text}")
        return None

    try:
        return await new_role.edit(
            position=max([role.position for role in guild.me.roles]) - 2
        )
    except (discord.Forbidden, discord.HTTPException, discord.InvalidArgument) as e:
        logError(f"Failed to move role {color.get_hex()} with {e.text}")
        return new_role


async def delete_role(role: discord.Role) -> bool:
    try:
        await role.delete()
        return True
    except:
        logError(f"Failed to delete role {role.name}")
        return False


async def errorAndRespond(ctx: discord.ApplicationContext, message: str):
    logError(message)
    return await ctx.respond(f"{message}, please try again in a few seconds")


async def logAndRespond(ctx: discord.ApplicationContext, message: str):
    logInfo(message)
    return await ctx.respond(message)


def logError(message: str):
    print(f"ERROR: {message}")


def logInfo(message: str):
    print(f"INFO: {message}")
