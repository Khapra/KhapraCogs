import discord
from redbot.core import commands

class RoleMemberLimit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_limits = {}

        
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def setrolelimit(self, ctx, role: discord.Role, limit: int):
        """Sets the maximum number of members allowed in the specified role."""
        self.role_limits[role.id] = limit
        await ctx.send(f"Maximum limit for {role.name} set to {limit} members.")
        
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Checks if a member has reached the maximum limit for a role."""
        for role in after.roles:
            if role.id in self.role_limits and len(role.members) > self.role_limits[role.id]:
                await after.remove_roles(role)
                await after.send(f"You have been removed from the {role.name} role because the maximum limit of {self.role_limits[role.id]} members has been reached.")

def setup(bot):
    bot.add_cog(RoleMemberLimit(bot))
