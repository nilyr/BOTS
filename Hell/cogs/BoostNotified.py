import disnake
from disnake import ButtonStyle
from disnake.ext import commands
from disnake.ui import View, Button
from datetime import datetime, timezone, timedelta


class BoostNotified(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        guild_tc = self.bot.get_guild(614081676116754465)

        now = datetime.now(timezone(timedelta(hours=+3)))

        if before.guild and after.guild == guild_tc:
            channel_boost_notifications = self.bot.get_channel(1025398653143236709)
            nilyr = self.bot.get_user(483914754478571521)

        if len(before.roles) < len(after.roles):
            boost_role = next(
                role for role in after.roles if role not in before.roles)

            if boost_role == after.guild.premium_subscriber_role:
                emb_boost_user_button = View()
                emb_boost_user_button.add_item(
                    Button(
                        style=ButtonStyle.grey,
                        emoji="📨",
                        label=f"Отправлено с {after.guild}",
                        disabled=True))

                embed_boost = disnake.Embed(
                    color=0x2f3136,
                    title="Мы получили буст!",
                    description=f"Привет {after.mention}, спасибо тебе за буст нашего сервера!\n\n**Теперь тебе будут доступны некоторые эксклюзивные фишки. На твой счёт в скором времени поступят 7000 конфеток Discord сервера!**",
                    timestamp=now
                )

                embed_boost.set_image(
                    url="https://media1.tenor.com/images/dbd5f352c80e3445b801d548ca330a6a/tenor.gif?itemid=14214458")
                embed_boost.set_footer(
                    text="Спасибо огромное тебе за буст нашего сервера! Удачи, ищи себе новых друзей.",
                    icon_url="https://cdn.discordapp.com/attachments/838848278858039336/853329457217273866/boost.gif")

                embed_admin = disnake.Embed(
                    color=0x2f3136,
                    title="Сервер забустили!",
                    description=f"**Участнику {after} / {after.mention} необходимо выдать 5000 конфеток за буст сервера!**",
                    timestamp=now)

                embed_nilyr = disnake.Embed(
                    color=0x2f3136,
                    title="Сервер забустили!",
                    description=f"**Участнику {after} / {after.mention} необходимо выдать 5000 конфеток за буст сервера!**",
                    timestamp=now)

                try:
                    await channel_boost_notifications.send(embed=embed_admin)
                    await after.send(embed=embed_boost, view=emb_boost_user_button)
                    await nilyr.send(embed=embed_nilyr)
                except BaseException:
                    pass


def setup(bot):
    bot.add_cog(BoostNotified(bot))
