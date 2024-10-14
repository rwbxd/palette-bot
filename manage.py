import discord
from util import delete_role, error_and_respond, log_and_respond


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
        deleted_roles: list[str] = [
            role.name for role in empty_color_roles if await delete_role(role)
        ]

        return await log_and_respond(
            ctx,
            f"Cleaned up {len(deleted_roles)} empty color roles"
            + (":\n" + "\n".join(deleted_roles) if len(deleted_roles) != 0 else "."),
        )
    except AssertionError as errorMessage:
        return await error_and_respond(ctx, errorMessage)
