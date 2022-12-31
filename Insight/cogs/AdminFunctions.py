import disnake
import sqlite3
from disnake.ext import commands
from disnake.ui import View, Button
from disnake import TextInputStyle, ButtonStyle


class SayMessage(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Сообщение",
                placeholder="Текст сообщения",
                custom_id="message",
                style=TextInputStyle.paragraph
            )
        ]

        super().__init__(
            title="Создание сообщения",
            custom_id="create_message",
            components=components
        )

    async def callback(self, inter: disnake.ModalInteraction):
        text = inter.text_values

        try:
            await inter.channel.send(content=text["message"])
            await inter.send(content="Cообщение отправлено.", ephemeral=True)
        except BaseException:
            await inter.send(content="Внутренняя ошибка. Обратитесь к разработчику бота.", ephemeral=True)


class SayEmbed(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Название",
                placeholder="Текст названия",
                custom_id="title",
                style=TextInputStyle.paragraph,
                required=False
            ),

            disnake.ui.TextInput(
                label="Текст",
                placeholder="Текст текста?!?!?",
                custom_id="description",
                style=TextInputStyle.paragraph,
                required=False
            ),

            disnake.ui.TextInput(
                label="Картинка",
                placeholder="URL картинки",
                custom_id="image",
                style=TextInputStyle.short,
                required=False
            ),

            disnake.ui.TextInput(
                label="Футер",
                placeholder="Футер текста",
                custom_id="footer",
                style=TextInputStyle.paragraph,
                required=False
            ),

            disnake.ui.TextInput(
                label="Иконка футера",
                placeholder="URL иконки футера",
                custom_id="footer_icon",
                style=TextInputStyle.short,
                required=False
            )
        ]

        super().__init__(
            title="Создание Embed сообщения",
            custom_id="create_embed",
            components=components
        )

    async def callback(self, inter: disnake.ModalInteraction):
        text = inter.text_values

        embed = disnake.Embed(
            color=0x2f3136,
            title=text["title"],
            description=text["description"]
        )

        embed.set_image(url=text["image"])

        if text["footer_icon"] is None:
            embed.set_footer(text=text["footer"])
        else:
            embed.set_footer(text=text["footer"], icon_url=text["footer_icon"])

        try:
            await inter.channel.send(embed=embed)
            await inter.send(content="Embed Cообщение отправлено.", ephemeral=True)
        except BaseException:
            await inter.send(content="Внутренняя ошибка. Обратитесь к разработчику бота.", ephemeral=True)


with sqlite3.connect("database (Insight).db") as db:
    cursor = db.cursor()
    
    class AdminFunctions(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.slash_command(name="say-messages",
                                description="Создание сообщений через бота",
                                guild_ids=[387409949442965506])
        async def saymessages(self, ctx):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            say_button = View()
            say_button.add_item(
                Button(
                    style=ButtonStyle.grey,
                    label="Текстовое сообщение",
                    custom_id="text_message_button"))
            say_button.add_item(
                Button(
                    style=ButtonStyle.grey,
                    label="Embed сообщение",
                    custom_id="embed_message_button"))

            if ctx.author.guild_permissions.administrator or perms_owner is not None or perms_dev is not None:
                await ctx.send(content="Какое сообщение вы хотите написать?", view=say_button, ephemeral=True)
                return
                
            await ctx.send(content="У вас нет прав Администратора.", ephemeral=True)

        @commands.Cog.listener()
        async def on_button_click(self, inter):
            if inter.component.custom_id == "text_message_button":
                if inter.author.guild_permissions.administrator:
                    await inter.response.send_modal(modal=SayMessage())
                    return

                await inter.send(content="У вас нет прав Администратора.", ephemeral=True)

            if inter.component.custom_id == "embed_message_button":
                if inter.author.guild_permissions.administrator:
                    await inter.response.send_modal(modal=SayEmbed())
                    return

                await inter.send(content="У вас нет прав Администратора.", ephemeral=True)

        @commands.command(name="add-reaction")
        async def addreaction(self, ctx, msg: disnake.Message, emoji):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            if perms_owner is not None or perms_dev is not None:
                await ctx.message.delete()
                await msg.add_reaction(emoji)
                return

            await ctx.message.delete(delay=5)
            await ctx.reply(content="Права на использование есть только у разработчика бота.", delete_after=5)


        @commands.command(name="me-unban")
        async def meunban(self, ctx, guild: disnake.Guild):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            if perms_owner is not None or perms_dev is not None:
                banned_users = await guild.bans()

                for member in banned_users:
                    member = ctx.author

                    embed_unban = disnake.Embed(
                        title=guild,
                        description=f"Cэр, вы были разбанены.",
                        color=0x2f3136)
                    
                    try:
                        await guild.unban(member)
                        await ctx.message.delete(delay=5)
                        await ctx.reply(embed=embed_unban, delete_after=5)
                        return
                    except BaseException:
                        await ctx.message.delete(delay=5)
                        await ctx.reply(content="Вы не находитесь в бане.", delete_after=5)
                        return

        @commands.command(name="me-unmute")
        async def meunmute(self, ctx, guild: disnake.Guild):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            if perms_owner is not None or perms_dev is not None:
                embed_unmute = disnake.Embed(
                    title=guild,
                    description=f"Cэр, вы были разглушены.",
                    color=0x2f3136)

                try:   
                    await guild.timeout(ctx.author, duration=None)
                    await ctx.message.delete(delay=5)
                    await ctx.reply(embed=embed_unmute, delete_after=5)
                    return
                except BaseException:
                    await ctx.message.delete(delay=5)
                    await ctx.reply(content="Вы не находитесь в муте.", delete_after=5)
                    return

        @commands.command(name="add-role")
        async def addrole(self, ctx, member: disnake.Member, role: disnake.Role):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()

            if perms_owner is not None:
                await ctx.message.delete(delay=5)
                await member.add_roles(role)
                await ctx.reply(embed=disnake.Embed(description=f"{role.mention} была успешно выдана пользователю {member.mention}.", color=0x2f3136), delete_after=5)

        @commands.command(name="remove-role")
        async def removerole(self, ctx, member: disnake.Member, role: disnake.Role):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()

            if perms_owner is not None:
                await ctx.message.delete(delay=5)
                await member.remove_roles(role)
                await ctx.reply(embed=disnake.Embed(description=f"{role.mention} была успешно убрана у пользователя {member.mention}.", color=0x2f3136), delete_after=5)

        @commands.command(name="edit-name-role")
        async def editnamerole(self, ctx, role: disnake.Role, *, name: str):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()

            if perms_owner is not None:
                embed = disnake.Embed(
                    description=f"Название роли {role.mention} было успешно отредактировано. Название роли теперь: `{name}`.",
                    color=0x2f3136)

                await ctx.message.delete(delay=5)
                await ctx.reply(embed=embed, delete_after=5)
                await role.edit(name=name)

        @commands.command(name="edit-icon-role")
        async def editiconrole(self, ctx, role: disnake.Role):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()

            if perms_owner is not None:
                for icon in ctx.message.attachments:
                    embed = disnake.Embed(
                        description=f"Иконка роли {role.mention} была успешно отредактирована.",
                        color=0x2f3136)
                    embed.set_author(name="Новая иконка роли", icon_url=icon)

                    await role.edit(icon=icon)
                    await ctx.message.delete(delay=5)
                    await ctx.reply(embed=embed, delete_after=5)
                    return

                await ctx.message.delete(delay=5)
                await ctx.reply(content="Вы не прикрепили изображение к сообщению.", delete_after=5)

        @commands.command(name="edit-color-role")
        async def editcolorrole(self, ctx, role: disnake.Role, color: disnake.Color):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()

            if perms_owner is not None:
                embed = disnake.Embed(
                    description=f"Цвет роли {role.mention} был успешно отредактирован.",
                    color=0x2f3136)

                await role.edit(color=color)
                await ctx.message.delete(delay=5)
                await ctx.reply(embed=embed, delete_after=5)

        @commands.command(name="server-description")
        async def serverdescription(self, ctx, *, desc: str):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            if perms_owner is not None or perms_dev is not None:
                await ctx.guild.edit(description=desc)
                await ctx.message.delete()
                await ctx.send(content=f"Описание сервера **{ctx.guild.name}** было успешно изменено.\n\nОписание сервера теперь:\n**{desc}**.", delete_after=5)

        @commands.command(name="admin-kick")
        async def adminkick(self, ctx, member: disnake.Member):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            if perms_owner is not None or perms_dev is not None:
                await member.kick(reason="Кикнут спец. командой")
                await ctx.message.delete(delay=5)
                await ctx.reply(embed=disnake.Embed(description=f"Пользователь {member} был успешно кикнут.", color=0x2f3136), delete_after=5)
        
        @commands.command(name="admin-ban")
        async def adminban(self, ctx, member: disnake.User, delete_messages=None):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            if perms_owner is not None or perms_dev is not None:
                if delete_messages == "all":
                    await ctx.guild.ban(member, reason="Забанен спец. командой", delete_message_days=7)
                if delete_messages == None:
                    await ctx.guild.ban(member, reason="Забанен спец. командой", delete_message_days=0)

                await ctx.message.delete(delay=5)
                await ctx.reply(embed=disnake.Embed(description=f"Пользователь {member} был успешно забанен.", color=0x2f3136), delete_after=5)

        @commands.command(name="admin-unban")
        async def adminunban(self, ctx, user: disnake.User):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            if perms_owner is not None or perms_dev is not None:
                banned_users = await ctx.guild.bans()

                for member in banned_users:
                    member = user
                    
                    try:
                        await ctx.guild.unban(member, reason="Разбанен спец. командой")
                        await ctx.message.delete(delay=5)
                        await ctx.reply(embed=disnake.Embed(description=f"Пользователь {member} был успешно разбанен.", color=0x2f3136), delete_after=5)
                        return
                    except BaseException:
                        await ctx.message.delete(delay=5)
                        await ctx.reply(content="Данный пользователь не находится в пермаментном бане.")
                        return

        @commands.command(name="admin-all-unban")
        async def adminallunban(self, ctx):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            if perms_owner is not None or perms_dev is not None:
                banned_users = await ctx.guild.bans()
                delc = 0

                await ctx.message.delete()
                msg = await ctx.send(content="Процесс пошёл...")

                for ban_entry in banned_users:
                    user = ban_entry.user
                    await ctx.guild.unban(user)
                    delc = delc + 1

                await msg.edit(content=f"{ctx.author.mention}\nРазбанено **{delc}** пользователей.")

        @commands.command(name="admin-all-addrole")
        async def adminalladdroles(self, ctx, role: disnake.Role):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()

            if perms_owner is not None:
                delc = 0

                await ctx.message.delete()
                msg = await ctx.send(content="Процесс пошёл...")

                for user in ctx.guild.members:
                    await user.add_roles(role)
                    delc = delc + 1

                await msg.edit(content=f"{ctx.author.mention}\nРоль выдана **{delc}** пользователям.")

        @commands.command(name="admin-all-removerole")
        async def adminallremoveroles(self, ctx, role: disnake.Role):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()

            if perms_owner is not None:
                delc = 0

                await ctx.message.delete()
                msg = await ctx.send(content="Процесс пошёл...")

                for user in ctx.guild.members:
                    await user.remove_roles(role)
                    delc = delc + 1

                await msg.edit(content=f"{ctx.author.mention}\nРоль удалена у **{delc}** пользователей.")

        @commands.command(name="inrole_cmd")
        async def inrolecmd(self, ctx, *, role: disnake.Role):
            members_role = []

            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            if perms_owner is not None or perms_dev is not None:
                for member in role.members:
                    members_role.append(f"{member.mention}")

                members_role_list = f'{str(members_role)}'.replace('[','').replace(']','').replace(',','\n').replace("'","").replace('"','')

                embed = disnake.Embed(
                    title=f"Список пользователей [{len(members_role)}]",
                    description=f"Пользователи с ролью {role.mention}:\n{members_role_list}",
                    color=0x2f3136)
                embed_0 = disnake.Embed(
                    title=f"Список пользователей",
                    description=f"Пользователи с ролью {role.mention}:\nПользователей с данной ролью не найдено.",
                    color=0x2f3136)

                if len(members_role) != 0:
                    try:
                        await ctx.reply(embed=embed)
                        return
                    except BaseException:
                        await ctx.message.delete(delay=5)
                        await ctx.reply(content="Список пользователей не помещается в сообщение.", delete_after=5)
                        return

                await ctx.reply(embed=embed_0)

        @commands.command(name="inbots_cmd")
        async def inbotscmd(self, ctx):
            members_bot = []

            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            if perms_owner is not None or perms_dev is not None:
                for member in ctx.guild.members:
                    if member.bot:
                        members_bot.append(f"{member.mention}")

                members_bot_list = f'{str(members_bot)}'.replace('[','').replace(']','').replace(',','\n').replace("'","").replace('"','')

                embed = disnake.Embed(
                    title=f"Список пользователей [{len(members_bot)}]",
                    description=f"Пользователи-боты:\n{members_bot_list}",
                    color=0x2f3136)
                embed_0 = disnake.Embed(
                    title=f"Список пользователей",
                    description=f"Пользователи-боты:\nПользователи-боты не найдены.",
                    color=0x2f3136)

                if len(members_bot) != 0:
                    try:
                        await ctx.reply(embed=embed)
                        return
                    except BaseException:
                        await ctx.message.delete(delay=5)
                        await ctx.reply(content="Список пользователей не помещается в сообщение.", delete_after=5)
                        return

                await ctx.reply(embed=embed_0)

        @commands.command(name="inboosters_cmd")
        async def inboostboosterscmd(self, ctx):
            members_boosters = []

            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            if perms_owner is not None or perms_dev is not None:
                for member in ctx.guild.premium_subscribers:
                    members_boosters.append(f"{member.mention} {member.premium_since}")

                members_boosters_list = f'{str(members_boosters)}'.replace('[','').replace(']','').replace(',','\n').replace("'","").replace('"','')

                embed = disnake.Embed(
                    title=f"Список пользователей [{len(members_boosters)}]",
                    description=f"Пользователи-бустеры:\n{members_boosters_list}",
                    color=0x2f3136)
                embed_0 = disnake.Embed(
                    title=f"Список пользователей",
                    description=f"Пользователи-бустеры:\nПользователи-бустеры не найдены.",
                    color=0x2f3136)

                if len(members_boosters) != 0:
                    try:
                        await ctx.reply(embed=embed)
                        return
                    except BaseException:
                        await ctx.message.delete(delay=5)
                        await ctx.reply(content="Список пользователей не помещается в сообщение.", delete_after=5)
                        return

                await ctx.reply(embed=embed_0)


def setup(bot):
    bot.add_cog(AdminFunctions(bot))