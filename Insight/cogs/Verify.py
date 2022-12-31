import disnake
import sqlite3
from disnake import ButtonStyle
from disnake.ext import commands
from disnake.ui import View, Button


with sqlite3.connect("database (Insight).db") as db:
    cursor = db.cursor()

    class Verification(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.command(name="verify")
        async def verifyinformation(self, ctx):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            guild_kp = self.bot.get_guild(387409949442965506)

            if perms_owner is not None or perms_dev is not None:
                if ctx.guild == guild_kp:
                    channel_verify = self.bot.get_channel(989205089593991168)

                    embed = disnake.Embed(
                        color=0x2f3136,
                        title="Верификация",
                        description=f"Приветствую тебя на дискорд сервере `{ctx.guild}`.\n**Ты находишься в начальном канале верификации.**\n\nЧтобы пройти верификацию, тебе нужно нажать на кнопку внизу этого сообщения.\n\nЕсли вам пишет ошибку: `Channel verification level is too high`, то просто подождите 10 минут."
                    )

                    embed.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/992086461581119658/Verify.gif")
                    embed.set_footer(
                        text="После прохождения верификации ты свободно сможешь общаться на этом сервере.")

                    verify_button = View()
                    verify_button.add_item(
                        Button(
                            style=ButtonStyle.grey,
                            label="Верификация",
                            custom_id="verify_button"))

                    await ctx.message.delete()
                    await channel_verify.purge()
                    await channel_verify.send(embed=embed, view=verify_button)
                    return

            await ctx.message.delete(delay=5)
            await ctx.reply(content="Права на использование есть только у разработчика бота.", delete_after=5)

        @commands.Cog.listener()
        async def on_button_click(self, inter):
            guild_kp = self.bot.get_guild(387409949442965506)

            if inter.guild == guild_kp:
                verify_role = disnake.utils.get(inter.guild.roles, id=1029037374434463815)
                user_role = disnake.utils.get(inter.guild.roles, id=610184544418791426)
                
                if inter.channel.id == 989205089593991168:
                    if inter.component.custom_id == "verify_button":
                        if verify_role in inter.author.roles:
                            if user_role in inter.author.roles:
                                await inter.send(content="**Верификация прошла успешно!**\nПриятного времяпровождения на нашем сервере!", ephemeral=True)
                                await inter.author.remove_roles(verify_role, reason="Прохождение верификации")
                                return

                            await inter.send(content="**Верификация прошла успешно!**\nПриятного времяпровождения на нашем сервере!", ephemeral=True)
                            await inter.author.add_roles(user_role, reason="Прохождение верификации")
                            await inter.author.remove_roles(verify_role, reason="Прохождение верификации")
                            return

                        await inter.send(content="Вы уже верифицированы.", ephemeral=True)

def setup(bot):
    bot.add_cog(Verification(bot))
