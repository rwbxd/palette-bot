import discord
from util import errorAndRespond, logAndRespond, logError


async def clean_empty_color_roles(ctx: discord.ApplicationContext):
    try:
        assert (
            type(ctx.guild) is discord.Guild
        ), "Encountered an issue accessing the Discord guild"
        empty_color_roles = [
            role
            for role in ctx.guild.roles
            if role.name.startswith("#") and len(role.members) == 0
        ]
        counter = 0
        for role in empty_color_roles:
            try:
                await role.delete()
                counter += 1
            except:
                logError(f"Failed to delete role {role.name}")
        return await logAndRespond(ctx, f"Cleaned up {counter} empty color roles!")
    except AssertionError as errorMessage:
        return await errorAndRespond(ctx, errorMessage)
