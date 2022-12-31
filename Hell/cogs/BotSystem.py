import disnake
import sqlite3
from disnake.ext import commands

with sqlite3.connect("database (Hell).db") as db:
    cursor = db.cursor()

    class BotSystem(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.slash_command(name="ping", description="Узнать пинг бота")
        async def status_discord(self, ctx):
            embed = disnake.Embed(
                color=0x2f3136,
                title=f"<:ping:919166899076599849> Пинг бота {ctx.guild.me.name}",
                description=f"<a:RightArrow1:919166915048517712> **{round(self.bot.latency * 1000)} ms**")

            await ctx.send(embed=embed, delete_after=20)

        @commands.Cog.listener()
        async def on_modal_submit(self, inter):
            channel_logs = self.bot.get_channel(1025833720420253737)

            modal_info = disnake.Embed(
                    title=f"Модальное окно было использовано",
                    color=0x2f3136)
            modal_info.add_field(
                name="Автор:",
                value=inter.author.mention,
                inline=False)
            modal_info.add_field(
                name="Модальное окно:",
                value=f"**```yaml\n{inter.custom_id}\n```**",
                inline=False)
            modal_info.add_field(
                name="Содержание:",
                value=f"**```yaml\n{inter.text_values}\n```**",
                inline=False)
            modal_info.set_footer(
                text=f"{inter.guild} (ID: {inter.guild_id})",
                icon_url=inter.guild.icon)

            await channel_logs.send(embed=modal_info)

        @commands.command(name="bot-leave")
        async def botleave(self, ctx):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            if perms_owner is not None or perms_dev is not None:
                embed_kick = disnake.Embed(
                    title=f"Бот {self.bot.user.name} вышел с сервера",
                    description=f"Бот кикнут администратором {ctx.author}.",
                    color=0x2f3136)

                await ctx.message.delete()
                await ctx.send(embed=embed_kick)
                await ctx.guild.leave()
                return

        @commands.command(name="bot-nick-edit")
        async def botnickedit(self, ctx, *, nick: str):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            if perms_owner is not None or perms_dev is not None:
                await ctx.message.delete()

                await ctx.guild.me.edit(nick=nick)
                await ctx.send(content=f"Ник бота был успешно отредактирован. Теперь он: `{nick}`.", delete_after=20)

        @commands.Cog.listener()
        async def on_dropdown(self, inter: disnake.MessageInteraction):
            if "default_option" in inter.values:
                await inter.response.defer()


def setup(bot):
    bot.add_cog(BotSystem(bot))
