import disnake
import random
from disnake.ext import commands
from datetime import datetime, timezone, timedelta


class UsersJoin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    hello_gifs = [
        "https://cdn.discordapp.com/attachments/834837020056616992/960930927696031744/higurashi-gou.gif",
        "https://cdn.discordapp.com/attachments/834837020056616992/960930928019009628/yamato-anime.gif",
        "https://cdn.discordapp.com/attachments/834837020056616992/960930928379699350/anime-hi.gif",
        "https://cdn.discordapp.com/attachments/834837020056616992/960930928874635324/hi-anime.gif",
        "https://cdn.discordapp.com/attachments/834837020056616992/960930929222750238/yuuki-princess-connect.gif",
        "https://cdn.discordapp.com/attachments/834837020056616992/960930929524768819/yuigahama-yahallo.gif",
        "https://cdn.discordapp.com/attachments/834837020056616992/960930929965138070/hello-anime1.gif",
        "https://cdn.discordapp.com/attachments/834837020056616992/960930930262945892/anime-hi1.gif",
        "https://cdn.discordapp.com/attachments/834837020056616992/960930930523009035/hello-anime.gif",
        "https://cdn.discordapp.com/attachments/834837020056616992/960930930778857532/hi-hello2.gif",
        "https://cdn.discordapp.com/attachments/834837020056616992/960930961732821052/image_860312191831466546815.gif",
        "https://cdn.discordapp.com/attachments/834837020056616992/960930962236129300/school-live-cute.gif"]

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_kp = self.bot.get_guild(387409949442965506)

        nilyr = self.bot.get_user(483914754478571521)
        now = datetime.now(timezone(timedelta(hours=+3)))

        bots_info = disnake.Embed(
            title=f"Внимание, на сервер {member.guild} был добавлен бот!",
            color=0x2f3136,
            description=f"**Был добавлен Бот {member} / {member.mention}!**",
            timestamp=now)
        bots_info.set_footer(
            text="Если не вы добавляли его, то быстрее проверяйте сервер!")

        if member.guild == guild_kp:
            verify_role = disnake.utils.get(member.guild.roles, id=1029037374434463815)

            member_join_info = disnake.Embed(
                title=member.guild,
                color=0x2f3136,
                description=f"**{member.mention}, добро пожаловать на Дискорд сервер {member.guild}**\n\nСейчас ты не имеешь полный доступ к серверу, чтобы его получить верифицируй себя в канале верификации.\n\nМы надеемся что тебе тут понравится, что тут ты найдёшь себе верных и добрых друзей, а может и тиммейтов для совместной игры)\n\nС твоим приходом участников стало больше!\nНас теперь **{member.guild.member_count}** участников.",
                timestamp=now)
            member_join_info.set_image(url=random.choice(self.hello_gifs))

            if member.bot:
                await nilyr.send(embed=bots_info)
                return

            await member.add_roles(verify_role, reason="Участник присоединился на сервер")
            try:
                await member.send(member.mention, embed=member_join_info)
            except BaseException:
                pass


def setup(bot):
    bot.add_cog(UsersJoin(bot))
