import disnake
import sqlite3
from disnake import ButtonStyle
from disnake.ext import commands
from disnake.ui import View, Button
from cogs.InteractionDatabase import natame_guild

with sqlite3.connect("database (Miky).db") as db:
    cursor = db.cursor()

    class StaffModule(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.command(name="kit-moder")
        async def kitmoder(self, ctx):
            guild_na = self.bot.get_guild(natame_guild)

            if ctx.guild == guild_na:
                channel_nabor = self.bot.get_channel(1006515016175980547)

                if ctx.author.guild_permissions.administrator:
                    await ctx.message.delete()
                    nabor_button = View()
                    nabor_button.add_item(
                        Button(
                            style=ButtonStyle.grey,
                            label="Подать заявку",
                            custom_id="helper_md_button"))

                    nabor = disnake.Embed(
                        color=0x2f3136, description="<@&1006622598748188834> - Модерация сервера. Отвечают за порядок на сервере, модерируют чаты/войсы.\n\n"
                        "<a:beloe_serdze:985883774220894238> **Что от вас потребуется:**\n<:eto_che:985881657854808154><a:tochka_anim1:978740315676631092> Адекватность и стрессоустойчивость.\n<:eto_che:985881657854808154><a:tochka_anim1:978740315676631092> 14 полных лет.\n<:eto_che:985881657854808154><a:tochka_anim1:978740315676631092> Быть готовым работать в коллективе и помогать друг другу.\n<:eto_che:985881657854808154><a:tochka_anim1:978740315676631092> Знание правил сервера и правил TOS.\n\n"
                        "<a:beloe_serdze:985883774220894238> **Что вас ждёт:**\n<:eto_che:985881657854808154><a:tochka_anim1:978740315676631092> Приятное времяпровождение в дружном коллективе.\n<:eto_che:985881657854808154><a:tochka_anim1:978740315676631092> Личные роли, донат. привилегии и многое другое.\n\n")
                    nabor.set_footer(
                        text="Если ваша заявка зацепит наше сердечко - вам отпишут!")
                    nabor.set_image(
                        url="https://i.pinimg.com/originals/d9/82/8c/d9828c9adaa51dd6e2e66b48787e4023.gif")
                    
                    await channel_nabor.send(embed=nabor, view=nabor_button)
                    return

                await ctx.message.delete(delay=5)
                await ctx.reply(content="Права на использование есть только у Администратора.", delete_after=5)


def setup(bot):
    bot.remove_cog(StaffModule(bot))