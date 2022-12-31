import disnake
from disnake.ext import commands
from datetime import datetime, timezone, timedelta


class UsersJoin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_tc = self.bot.get_guild(614081676116754465)

        nilyr = self.bot.get_user(483914754478571521)
        now = datetime.now(timezone(timedelta(hours=+3)))

        bots_info = disnake.Embed(
            title=f"Внимание, на сервер {member.guild} был добавлен бот!",
            color=0x2f3136,
            description=f"**Был добавлен Бот {member} / {member.mention}!**",
            timestamp=now)
        bots_info.set_footer(
            text="Если не вы добавляли его, то быстрее проверяйте сервер!")

        if member.guild == guild_tc:
            verify_role = disnake.utils.get(member.guild.roles, id=813363063398203393)
            player_role = disnake.utils.get(member.guild.roles, id=1025490054551982161)

            if member.bot:
                await nilyr.send(embed=bots_info)
                return

            await member.add_roles(verify_role, reason="Участник присоединился к серверу")
            await member.add_roles(player_role, reason="Участник присоединился к серверу")


def setup(bot):
    bot.add_cog(UsersJoin(bot))
