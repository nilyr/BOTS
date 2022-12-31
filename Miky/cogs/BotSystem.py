import disnake
import sqlite3
from disnake.ext import commands
from cogs.InteractionDatabase import module_ping

with sqlite3.connect("database (Miky).db") as db:
    cursor = db.cursor()

    class BotSystem(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.slash_command(name="ping", description="Узнать пинг бота", guild_ids=module_ping)
        async def status_discord(self, ctx):
            embed = disnake.Embed(
                color=0x2f3136,
                title=f"<:ping:919166899076599849> Пинг бота {ctx.guild.me.name}",
                description=f"<a:RightArrow1:919166915048517712> **{round(self.bot.latency * 1000)} ms**")

            await ctx.send(embed=embed, delete_after=20)

        @commands.Cog.listener()
        async def on_button_click(self, inter):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {inter.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {inter.author.id} AND lvl_rights = 'DEV'""").fetchone()

            if inter.component.custom_id == "delete_button_proles":
                if perms_owner is not None or perms_dev is not None:
                    await inter.message.delete()
                    return

                await inter.send(content="Права на использование есть только у разработчика бота.", ephemeral=True)

        @commands.Cog.listener()
        async def on_modal_submit(self, inter):
            channel_logs = self.bot.get_channel(992891923704590386)

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

        @commands.Cog.listener()
        async def on_guild_join(self, guild):
            channel_send = self.bot.get_channel(960472957250076702)

            bots_info = disnake.Embed(
                title=f"Бот {guild.me.name} был приглашён на ваш сервер!",
                color=0x2f3136,
                description=f"**Спасибо, что пригласили бота {guild.me.mention} на ваш сервер!**\n\nК превеликому сожалению бот является приватным. Данный бот существует только для определённых серверов.\n\nПолный потенциал бота может раскрыть только его создатель.\nПрефикс: `/`"
            )

            bots_info.set_thumbnail(url=guild.me.display_avatar)
            bots_info.set_image(url="https://cdn.discordapp.com/attachments/834837020056616992/948224416846848122/3bf732b75f4a6c3c.gif")
            bots_info.set_footer(text="Creator and Dev: lantoy#0750")

            guild_info = disnake.Embed(
                title="Добавление на сервер",
                color=0x2f3136
            )

            guild_info.add_field(
                name="Сервер",
                value=f"**{guild}** `({guild.id})`",
                inline=False)
            guild_info.add_field(
                name="Владелец сервера",
                value=f"**{guild.owner}** `({guild.owner.id})`",
                inline=False)
            guild_info.add_field(
                name="Участников",
                value=f"**{guild.member_count}**",
                inline=False)
            guild_info.add_field(
                name="Серверов у бота",
                value=f"**{len(self.bot.guilds)}**",
                inline=False)

            await channel_send.send(embed=guild_info)

            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    await channel.send(embed=bots_info)
                    return

        @commands.command(name="bot-guilds")
        async def botguilds(self, ctx):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            if perms_owner is not None or perms_dev is not None:
                await ctx.message.delete()
                try:
                    await ctx.send(content=self.bot.guilds)
                except BaseException:
                    await ctx.send(content="Данные о гильдиях не уместились в сообщение.\nИнформация о них отправлена вам в консоль.", delete_after=5)
                    print(self.bot.guilds)

        @commands.command(name="bot-guilds-count")
        async def botguildscount(self, ctx):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            if perms_owner is not None or perms_dev is not None:
                await ctx.message.delete()
                await ctx.send(content=f"Количество серверов {ctx.guild.me.name}: {len(self.bot.guilds)}")

        @commands.command(name="bot-leave")
        async def botleave(self, ctx, guild: disnake.Guild=None):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            if perms_owner is not None or perms_dev is not None:
                if guild is None:
                    embed_kick = disnake.Embed(
                        title=f"Бот {self.bot.user.name} вышел с сервера",
                        description=f"Бот кикнут администратором {ctx.author}.",
                        color=0x2f3136)

                    await ctx.message.delete()
                    await ctx.send(embed=embed_kick)
                    await ctx.guild.leave()
                    return

                if guild is not None:
                    embed_kick_guild = disnake.Embed(
                        title=f"Бот {self.bot.user.name} вышел с сервера {guild.name}",
                        description=f"Бот кикнут администратором {ctx.author}.",
                        color=0x2f3136)

                    await ctx.message.delete()
                    await guild.leave()
                    await ctx.send(embed=embed_kick_guild)

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
