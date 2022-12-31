import disnake
from disnake import ButtonStyle
from disnake.ext import commands
from disnake.ui import View, Button
from disnake.ext.commands import has_permissions
from datetime import datetime, timezone, timedelta


class BoostAward(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="boost-money-yes")
    @has_permissions(administrator=True)
    async def boostmoneynotification(self, ctx, member: disnake.Member):
        guild_tc = self.bot.get_guild(614081676116754465)

        now = datetime.now(timezone(timedelta(hours=+3)))

        if ctx.guild == guild_tc:
            boost_notification_user_button = View()
            boost_notification_user_button.add_item(
                Button(
                    style=ButtonStyle.grey,
                    emoji="📨",
                    label=f"Отправлено с {ctx.guild}",
                    disabled=True))

        boost_notification = disnake.Embed(
            color=0x2f3136,
            title="Вам были выданы конфетки Discord сервера!",
            description=f"**{member.mention}, за ваш буст, вам были выданы конфетки Discord сервера, проверьте свой баланс.**\n\n"
            "Проверить баланс можно командой **`-bal`** (Писать во **『📮』・флуд**).",
            timestamp=now)
        boost_notification.set_footer(
            text="Удачной времяпровождение на нашем Discord сервере!")

        otvet = disnake.Embed(
            color=0x2f3136,
            description="**```yaml\nСообщение о выдаче конфеток за буст успешно отправлено!\n```**",
            timestamp=now)
        otvet.set_author(
            name=f"Выдал конфетки: {ctx.author} | {ctx.author.id}",
            icon_url=ctx.author.display_avatar)
        otvet.set_footer(
            text=f"Кому выдали конфетки: {member} | {member.id}",
            icon_url=member.display_avatar)

        try:
            await member.send(embed=boost_notification, view=boost_notification_user_button)
        except BaseException:
            pass
        await ctx.reply(embed=otvet)


def setup(bot):
    bot.add_cog(BoostAward(bot))
