from redbot.core.bot import Red
from .rolememberlimit import RoleMemberLimit


async def setup(bot: Red):
    await bot.add_cog(RoleMemberLimit(bot))
