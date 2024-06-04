import discord
from redbot.core import commands, Config


class RoleMemberLimit(commands.Cog):
    """
    Cog for limiting max members per role.
    """

    __author__ = ["Khapra"]
    __version__ = "0.0.5"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=534216890234)
        self.config.register_guild(role_limits={})

    @commands.group()
    async def rolelimit(self, ctx):
        """Group command for setting and retrieving role limits."""
        pass

    @rolelimit.command(name="set")
    @commands.has_permissions(administrator=True)
    async def set_role_limit(self, ctx, role: discord.Role, limit: int):
        """Sets the maximum number of members allowed in the specified role."""
        async with self.config.guild(ctx.guild).role_limits() as role_limits:
            role_limits[str(role.id)] = limit
        await ctx.send(f"Maximum limit for {role.name} set to {limit} members.")

    @rolelimit.command(name="list")
    async def list_role_limits(self, ctx):
        """Retrieves the maximum member limits set for each role in the server."""
        role_limits = await self.config.guild(ctx.guild).role_limits()
        if not role_limits:
            await ctx.send("No limits set.")
        else:
            msg = "Role limits set in this server:\n"
            for role_id, limit in role_limits.items():
                role = ctx.guild.get_role(int(role_id))
                if role:
                    msg += f"{role.name}: {limit}\n"
            await ctx.send(msg)

    @rolelimit.command(name="remove")
    @commands.has_permissions(administrator=True)
    async def remove_role_limit(self, ctx, role: discord.Role):
        """Removes the maximum number of members allowed in the specified role."""
        async with self.config.guild(ctx.guild).role_limits() as role_limits:
            if str(role.id) in role_limits:
                del role_limits[str(role.id)]
                await ctx.send(f"Maximum limit for {role.name} removed.")
            else:
                await ctx.send("No limit set for this role.")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Checks if a member has reached the maximum limit for a role."""
        role_limits = await self.config.guild(after.guild).role_limits()
        for role in after.roles:
            if str(role.id) in role_limits and len(role.members) > role_limits[str(role.id)]:
                await after.remove_roles(role)
                await after.send(f"You have been removed from the {role.name} role because the maximum limit of {role_limits[str(role.id)]} members has been reached.")
