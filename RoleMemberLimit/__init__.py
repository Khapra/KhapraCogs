from .rolememberlimit import RoleMemberLimit


async def setup(bot):
    bot.add_cog(RoleMemberLimit(bot))
