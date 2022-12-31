import disnake
import asyncio
from disnake import ButtonStyle
from disnake.ext import commands
from disnake.ui import View, Button
from datetime import datetime, timezone, timedelta


class MinecraftDonateSystem(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        guild_um = self.bot.get_guild(1)
        now = datetime.now(timezone(timedelta(hours=+3)))

        if inter.guild == guild_um:
            channel_logs = self.bot.get_channel(986934852064509952)
            channel_donate_roles = self.bot.get_channel(986718704643477564)
            category_donate_roles = disnake.utils.get(guild_um.categories, id=986931229532225607)

            player_role = disnake.utils.get(guild_um.roles, id=986928604334141480)

            ender_role = disnake.utils.get(guild_um.roles, id=986923867601772565)
            phantom_role = disnake.utils.get(guild_um.roles, id=986923875470290954)
            guardian_role = disnake.utils.get(guild_um.roles, id=986923881635917844)
            shulker_role = disnake.utils.get(guild_um.roles, id=986923878305640468)

            buttons = View(timeout=None)
            buttons.add_item(
                Button(
                    style=ButtonStyle.green,
                    label="Одобрена",
                    custom_id="button_donate_role_approved"))
            buttons.add_item(
                Button(
                    style=ButtonStyle.red,
                    label="Отклонена",
                    custom_id="button_donate_role_rejected"))

            buttons_issuance_withdrawal = View(timeout=None)
            buttons_issuance_withdrawal.add_item(
                Button(
                    style=ButtonStyle.blurple,
                    label="Выдать роль",
                    custom_id="add_role_button"))
            buttons_issuance_withdrawal.add_item(
                Button(
                    style=ButtonStyle.blurple,
                    label="Снять роль",
                    custom_id="remove_role_button"))
            buttons_issuance_withdrawal.add_item(
                Button(
                    style=ButtonStyle.red,
                    label="Отклонена",
                    custom_id="button_donate_role_rejected"))

            buttons_waiting_closure = View(timeout=None)
            buttons_waiting_closure.add_item(
                Button(
                    style=ButtonStyle.red,
                    label="Полное закрытие заявки",
                    custom_id="buttons_closure"))
            buttons_waiting_closure.add_item(
                Button(
                    style=ButtonStyle.blurple,
                    label="Вернуться в меню выдачи и снятия",
                    custom_id="button_return"))

            buttons_issuing = View(timeout=None)
            buttons_issuing.add_item(
                Button(
                    style=ButtonStyle.grey,
                    label="ENDER",
                    custom_id="add_ender_button"))
            buttons_issuing.add_item(
                Button(
                    style=ButtonStyle.grey,
                    label="PHANTOM",
                    custom_id="add_phantom_button"))
            buttons_issuing.add_item(
                Button(
                    style=ButtonStyle.grey,
                    label="GUARDIAN",
                    custom_id="add_guardian_button"))
            buttons_issuing.add_item(
                Button(
                    style=ButtonStyle.grey,
                    label="SHULKER",
                    custom_id="add_shulker_button"))
            buttons_issuing.add_item(
                Button(
                    style=ButtonStyle.blurple,
                    label="→",
                    custom_id="add_next_button"))

            buttons_issuing1 = View(timeout=None)
            buttons_issuing1.add_item(
                Button(
                    style=ButtonStyle.blurple,
                    label="←",
                    custom_id="add_next1_button"))
            buttons_issuing1.add_item(
                Button(
                    style=ButtonStyle.red,
                    label="Отклонена",
                    custom_id="button_donate_role_rejected"))
            buttons_issuing1.add_item(
                Button(
                    style=ButtonStyle.blurple,
                    label="Вернуться в меню выдачи и снятия",
                    custom_id="button_return"))

            buttons_withdrawal = View(timeout=None)
            buttons_withdrawal.add_item(
                Button(
                    style=ButtonStyle.grey,
                    label="ENDER",
                    custom_id="remove_ender_button"))
            buttons_withdrawal.add_item(
                Button(
                    style=ButtonStyle.grey,
                    label="PHANTOM",
                    custom_id="remove_phantom_button"))
            buttons_withdrawal.add_item(
                Button(
                    style=ButtonStyle.grey,
                    label="GUARDIAN",
                    custom_id="remove_guardian_button"))
            buttons_withdrawal.add_item(
                Button(
                    style=ButtonStyle.grey,
                    label="SHULKER",
                    custom_id="remove_shulker_button"))
            buttons_withdrawal.add_item(
                Button(
                    style=ButtonStyle.blurple,
                    label="→",
                    custom_id="remove_next_button"))

            buttons_withdrawal1 = View(timeout=None)
            buttons_withdrawal1.add_item(
                Button(
                    style=ButtonStyle.blurple,
                    label="←",
                    custom_id="remove_next1_button"))
            buttons_withdrawal1.add_item(
                Button(
                    style=ButtonStyle.grey,
                    label="PLAYER",
                    custom_id="remove_player_button"))
            buttons_withdrawal1.add_item(
                Button(
                    style=ButtonStyle.red,
                    label="Отклонена",
                    custom_id="button_donate_role_rejected"))
            buttons_withdrawal1.add_item(
                Button(
                    style=ButtonStyle.blurple,
                    label="Вернуться в меню выдачи и снятия",
                    custom_id="button_return"))

            buttons_close = View(timeout=None)
            buttons_close.add_item(
                Button(
                    style=ButtonStyle.green,
                    label="Одобрена",
                    disabled=True))
            buttons_close.add_item(
                Button(
                    style=ButtonStyle.red,
                    label="Отклонена",
                    disabled=True))

            if inter.channel.id == channel_donate_roles.id:
                if inter.component.custom_id == "DonateRoles_button":
                    for channel_ in guild_um.get_channel(category_donate_roles.id).text_channels:
                        if channel_.name == f"{inter.author.id}":
                            await inter.send("Вы уже создали обращение!", ephemeral=True)
                            return

                    if inter.author.current_timeout is not None:
                        await inter.response.defer()
                        return

                    channel = await guild_um.get_channel(category_donate_roles.id).create_text_channel(f'{inter.author.id}')

                    buttons_application = View()
                    buttons_application.add_item(
                        Button(
                            style=ButtonStyle.green,
                            label="Взять заявку",
                            custom_id="button_application"))
                    buttons_application.add_item(
                        Button(
                            style=ButtonStyle.blurple,
                            label="Взять заявку, для админов",
                            custom_id="button_application_admin"))
                    buttons_application.add_item(
                        Button(
                            style=ButtonStyle.red,
                            label="Отклонена",
                            custom_id="button_donate_role_rejected"))

                    embed = disnake.Embed(
                        title='Заявка на донат-роль',
                        color=0x2f3136,
                        timestamp=now
                    )

                    embed.add_field(
                        name="Форма подачи заявки:",
                        value="**1.** Ваш никнейм на сервере.\n**2.** Ваша привилегия.\n**3.** Полный скриншот игры, где видна статистика сбоку и так же в чате видно сообщение от вас с вашим ником в дискорде.",
                        inline=False)
                    embed.set_footer(
                        text=f'{inter.author} (ID: {inter.author.id})',
                        icon_url=inter.author.display_avatar)

                    await inter.send(f"<:off:892647180521836605> {inter.author.mention} Заявка создаётся. Ожидайте!", ephemeral=True)
                    msg = await inter.original_message()

                    await channel.send(content=f"<@&986714529239035975>\nЗаявка на донат роль от {inter.author.mention}", embed=embed, view=buttons_application)
                    await channel.set_permissions(inter.author, read_messages=True, send_messages=True)
                    await msg.edit(content=f'<:onn:892647180542808084> Заявка создана! Для её заполнения перейдите в канал {channel.mention}')

            if inter.channel.category == category_donate_roles:
                member = inter.message.guild.get_member(int(inter.message.channel.name))

                try:
                    if not guild_um.get_member(member.id):
                        await inter.send(content="Создатель заявки не был найден! Возможно он вышел с сервера. Данный канал будет удалён через 5 секунд.", ephemeral=True)
                        await asyncio.sleep(5)
                        await inter.message.channel.delete()
                        return
                except BaseException:
                    await inter.send(content="Создатель заявки не был найден! Возможно он вышел с сервера. Данный канал будет удалён через 5 секунд.", ephemeral=True)
                    await asyncio.sleep(5)
                    await inter.message.channel.delete()
                    return

                if member.id == inter.author.id:
                    await inter.send(content="Зачем рассматривать свои же заявки?", ephemeral=True)
                    return

                if inter.component.custom_id == "button_application_admin":
                    if inter.author.guild_permissions.administrator:
                        await inter.send("Вы успешно взяли данную заявку!", ephemeral=True)
                        await inter.message.edit(content=f"Заявка на донат роль от {member.mention}\n**С этой заявкой работает:** {inter.author.mention}", view=buttons)
                        await inter.message.channel.set_permissions(inter.author, send_messages=True)
                        return

                    await inter.send("Вы не являетесь Администратором!", ephemeral=True)

                if inter.component.custom_id == "button_application":
                    if not inter.channel.permissions_for(inter.author).send_messages:
                        await inter.send("Вы успешно взяли данную заявку!", ephemeral=True)
                        await inter.message.edit(content=f"Заявка на донат роль от {member.mention}\n**С этой заявкой работает:** {inter.author.mention}", view=buttons)
                        await inter.message.channel.set_permissions(inter.author, send_messages=True)
                        return

                    await inter.send("Вы уже взяли данную заявку, либо вы являетесь Администратором.", ephemeral=True)

                if inter.channel.permissions_for(inter.author).send_messages:
                    if inter.component.custom_id == "button_donate_role_approved":
                        await inter.response.defer()
                        await inter.message.edit(view=buttons_issuance_withdrawal)

                    if inter.component.custom_id == "button_donate_role_rejected":
                        embed = disnake.Embed(
                            title='Закрытие заявки на донат-роль',
                            description="Заявка на донат-роль была отклонена!\nКанал с заявкой будет удалён через 5 секунд.",
                            color=0x2f3136)

                        embed.set_footer(
                            text=f"Отклонил заявку: {inter.author}",
                            icon_url=inter.author.display_avatar)

                        await inter.send(content="Вы отклонили заявку на донат-роль, данный канал будет удалён через 5 секунд.", ephemeral=True)
                        await inter.message.edit(embed=embed, view=buttons_close)
                        await asyncio.sleep(5)
                        await inter.message.channel.delete()

                    if inter.component.custom_id == "buttons_closure":
                        embed = disnake.Embed(
                            title='Закрытие заявки на донат-роль',
                            description="Заявка на донат-роль была полностью закрыта!\nКанал с заявкой будет удалён через 5 секунд.",
                            color=0x2f3136)

                        embed.set_footer(
                            text=f"Закрыл заявку: {inter.author}",
                            icon_url=inter.author.display_avatar)

                        await inter.send(content="Вы закрыли заявку на донат-роль, данный канал будет удалён через 5 секунд.", ephemeral=True)
                        await inter.message.edit(embed=embed, view=buttons_close)
                        await asyncio.sleep(5)
                        await inter.message.channel.delete()

                    if inter.component.custom_id == "add_role_button":
                        await inter.response.defer()
                        await inter.message.edit(view=buttons_issuing)

                    if inter.component.custom_id == "remove_role_button":
                        await inter.response.defer()
                        await inter.message.edit(view=buttons_withdrawal)

                    if inter.component.custom_id == "add_next_button":
                        await inter.response.defer()
                        await inter.message.edit(view=buttons_issuing1)

                    if inter.component.custom_id == "add_next1_button":
                        await inter.response.defer()
                        await inter.message.edit(view=buttons_issuing)

                    if inter.component.custom_id == "remove_next_button":
                        await inter.response.defer()
                        await inter.message.edit(view=buttons_withdrawal1)

                    if inter.component.custom_id == "remove_next1_button":
                        await inter.response.defer()
                        await inter.message.edit(view=buttons_withdrawal)

                    if inter.component.custom_id == "button_return":
                        await inter.response.defer()
                        await inter.message.edit(view=buttons_issuance_withdrawal)

                    if inter.component.custom_id == "add_ender_button":
                        if ender_role not in member.roles:
                            embed = disnake.Embed(
                                color=0x2f3136,
                                title="Роль была выдана!",
                                description=f"**Роль {ender_role.mention} выдана участнику {member.mention}.**",
                                timestamp=now)

                            embed.set_author(
                                name=f"Выдал роль: {inter.author}",
                                icon_url=inter.author.display_avatar)

                            member_embed_donate = disnake.Embed(
                                color=0x2f3136,
                                title="Ваша заявка на донат-роль была рассмотрена!",
                                description=f"**{member.mention}, ваша заявка заявка на донат-роль была принята!**\n"
                                f"Вам была выдана роль **{ender_role.name}**!",
                                timestamp=now)

                            member_embed_donate.set_author(
                                name=guild_um.name, icon_url=guild_um.icon)
                            member_embed_donate.set_footer(
                                text="Удачной времяпровождение на нашем Discord сервере!")

                            links_embed_donate = disnake.Embed(
                                color=0x2f3136,
                                title="Ваша заявка на донат-роль была рассмотрена!",
                                description=f"**{member.mention}, ваша заявка заявка на донат-роль была принята!**\n"
                                f"Вам была выдана роль {ender_role.mention}!",
                                timestamp=now)

                            links_embed_donate.set_author(
                                name=f"Оповещение для {member}", icon_url=member.display_avatar)
                            links_embed_donate.set_footer(
                                text="Удачной времяпровождение на нашем Discord сервере!")

                            logs = disnake.Embed(
                                title="Была выдана роль!", color=0x2f3136, timestamp=now)
                            logs.add_field(
                                name="Участник", value=member.mention)
                            logs.add_field(
                                name="ID участника", value=member.id)
                            logs.add_field(
                                name="Выданная роль", value=ender_role.mention)
                            logs.add_field(
                                name="ID роли", value=ender_role.id)
                            logs.add_field(
                                name="Участник, который выдал роль",
                                value=inter.author.mention)
                            logs.add_field(
                                name="ID участника, который выдал роль",
                                value=inter.author.id)

                            if player_role in member.roles:
                                await inter.response.defer()
                                await member.add_roles(ender_role)
                                await member.remove_roles(player_role)
                                await channel_logs.send(embed=logs)
                                await inter.message.edit(embed=embed, view=buttons_waiting_closure)

                                try:
                                    await member.send(embed=member_embed_donate)
                                except BaseException:
                                    pass
                                return

                            await inter.response.defer()
                            await member.add_roles(ender_role)
                            await channel_logs.send(embed=logs)
                            await inter.message.edit(embed=embed, view=buttons_waiting_closure)

                            try:
                                await member.send(embed=member_embed_donate)
                            except BaseException:
                                pass
                        else:
                            await inter.send(content=f"У участника уже есть роль {ender_role.mention}!", ephemeral=True)

                    if inter.component.custom_id == "add_phantom_button":
                        if phantom_role not in member.roles:
                            embed = disnake.Embed(
                                color=0x2f3136,
                                title="Роль была выдана!",
                                description=f"**Роль {phantom_role.mention} выдана участнику {member.mention}.**",
                                timestamp=now)

                            embed.set_author(
                                name=f"Выдал роль: {inter.author}",
                                icon_url=inter.author.display_avatar)

                            member_embed_donate = disnake.Embed(
                                color=0x2f3136,
                                title="Ваша заявка на донат-роль была рассмотрена!",
                                description=f"**{member.mention}, ваша заявка заявка на донат-роль была принята!**\n"
                                f"Вам была выдана роль **{phantom_role.name}**!",
                                timestamp=now)

                            member_embed_donate.set_author(
                                name=guild_um.name, icon_url=guild_um.icon)
                            member_embed_donate.set_footer(
                                text="Удачной времяпровождение на нашем Discord сервере!")

                            links_embed_donate = disnake.Embed(
                                color=0x2f3136,
                                title="Ваша заявка на донат-роль была рассмотрена!",
                                description=f"**{member.mention}, ваша заявка заявка на донат-роль была принята!**\n"
                                f"Вам была выдана роль {phantom_role.mention}!",
                                timestamp=now)

                            links_embed_donate.set_author(
                                name=f"Оповещение для {member}", icon_url=member.display_avatar)
                            links_embed_donate.set_footer(
                                text="Удачной времяпровождение на нашем Discord сервере!")

                            logs = disnake.Embed(
                                title="Была выдана роль!", color=0x2f3136, timestamp=now)
                            logs.add_field(
                                name="Участник", value=member.mention)
                            logs.add_field(
                                name="ID участника", value=member.id)
                            logs.add_field(
                                name="Выданная роль", value=phantom_role.mention)
                            logs.add_field(
                                name="ID роли", value=phantom_role.id)
                            logs.add_field(
                                name="Участник, который выдал роль",
                                value=inter.author.mention)
                            logs.add_field(
                                name="ID участника, который выдал роль",
                                value=inter.author.id)

                            if player_role in member.roles:
                                await inter.response.defer()
                                await member.add_roles(phantom_role)
                                await member.remove_roles(player_role)
                                await channel_logs.send(embed=logs)
                                await inter.message.edit(embed=embed, view=buttons_waiting_closure)

                                try:
                                    await member.send(embed=member_embed_donate)
                                except BaseException:
                                    pass
                                return

                            await inter.response.defer()
                            await member.add_roles(phantom_role)
                            await channel_logs.send(embed=logs)
                            await inter.message.edit(embed=embed, view=buttons_waiting_closure)

                            try:
                                await member.send(embed=member_embed_donate)
                            except BaseException:
                                pass
                        else:
                            await inter.send(content=f"У участника уже есть роль {phantom_role.mention}!", ephemeral=True)

                    if inter.component.custom_id == "add_guardian_button":
                        if guardian_role not in member.roles:
                            embed = disnake.Embed(
                                color=0x2f3136,
                                title="Роль была выдана!",
                                description=f"**Роль {guardian_role.mention} выдана участнику {member.mention}.**",
                                timestamp=now)

                            embed.set_author(
                                name=f"Выдал роль: {inter.author}",
                                icon_url=inter.author.display_avatar)

                            member_embed_donate = disnake.Embed(
                                color=0x2f3136,
                                title="Ваша заявка на донат-роль была рассмотрена!",
                                description=f"**{member.mention}, ваша заявка заявка на донат-роль была принята!**\n"
                                f"Вам была выдана роль **{guardian_role.name}**!",
                                timestamp=now)

                            member_embed_donate.set_author(
                                name=guild_um.name, icon_url=guild_um.icon)
                            member_embed_donate.set_footer(
                                text="Удачной времяпровождение на нашем Discord сервере!")

                            links_embed_donate = disnake.Embed(
                                color=0x2f3136,
                                title="Ваша заявка на донат-роль была рассмотрена!",
                                description=f"**{member.mention}, ваша заявка заявка на донат-роль была принята!**\n"
                                f"Вам была выдана роль {guardian_role.mention}!",
                                timestamp=now)

                            links_embed_donate.set_author(
                                name=f"Оповещение для {member}", icon_url=member.display_avatar)
                            links_embed_donate.set_footer(
                                text="Удачной времяпровождение на нашем Discord сервере!")

                            logs = disnake.Embed(
                                title="Была выдана роль!", color=0x2f3136, timestamp=now)
                            logs.add_field(
                                name="Участник", value=member.mention)
                            logs.add_field(
                                name="ID участника", value=member.id)
                            logs.add_field(
                                name="Выданная роль", value=guardian_role.mention)
                            logs.add_field(
                                name="ID роли", value=guardian_role.id)
                            logs.add_field(
                                name="Участник, который выдал роль",
                                value=inter.author.mention)
                            logs.add_field(
                                name="ID участника, который выдал роль",
                                value=inter.author.id)

                            if player_role in member.roles:
                                await inter.response.defer()
                                await member.add_roles(guardian_role)
                                await member.remove_roles(player_role)
                                await channel_logs.send(embed=logs)
                                await inter.message.edit(embed=embed, view=buttons_waiting_closure)

                                try:
                                    await member.send(embed=member_embed_donate)
                                except BaseException:
                                    pass
                                return

                            await inter.response.defer()
                            await member.add_roles(guardian_role)
                            await channel_logs.send(embed=logs)
                            await inter.message.edit(embed=embed, view=buttons_waiting_closure)

                            try:
                                await member.send(embed=member_embed_donate)
                            except BaseException:
                                pass
                        else:
                            await inter.send(content=f"У участника уже есть роль {guardian_role.mention}!", ephemeral=True)

                    if inter.component.custom_id == "add_shulker_button":
                        if shulker_role not in member.roles:
                            embed = disnake.Embed(
                                color=0x2f3136,
                                title="Роль была выдана!",
                                description=f"**Роль {shulker_role.mention} выдана участнику {member.mention}.**",
                                timestamp=now)

                            embed.set_author(
                                name=f"Выдал роль: {inter.author}",
                                icon_url=inter.author.display_avatar)

                            member_embed_donate = disnake.Embed(
                                color=0x2f3136,
                                title="Ваша заявка на донат-роль была рассмотрена!",
                                description=f"**{member.mention}, ваша заявка заявка на донат-роль была принята!**\n"
                                f"Вам была выдана роль **{shulker_role.name}**!",
                                timestamp=now)

                            member_embed_donate.set_author(
                                name=guild_um.name, icon_url=guild_um.icon)
                            member_embed_donate.set_footer(
                                text="Удачной времяпровождение на нашем Discord сервере!")

                            links_embed_donate = disnake.Embed(
                                color=0x2f3136,
                                title="Ваша заявка на донат-роль была рассмотрена!",
                                description=f"**{member.mention}, ваша заявка заявка на донат-роль была принята!**\n"
                                f"Вам была выдана роль {shulker_role.mention}!",
                                timestamp=now)

                            links_embed_donate.set_author(
                                name=f"Оповещение для {member}", icon_url=member.display_avatar)
                            links_embed_donate.set_footer(
                                text="Удачной времяпровождение на нашем Discord сервере!")

                            logs = disnake.Embed(
                                title="Была выдана роль!", color=0x2f3136, timestamp=now)
                            logs.add_field(
                                name="Участник", value=member.mention)
                            logs.add_field(
                                name="ID участника", value=member.id)
                            logs.add_field(
                                name="Выданная роль", value=shulker_role.mention)
                            logs.add_field(
                                name="ID роли", value=shulker_role.id)
                            logs.add_field(
                                name="Участник, который выдал роль",
                                value=inter.author.mention)
                            logs.add_field(
                                name="ID участника, который выдал роль",
                                value=inter.author.id)

                            if player_role in member.roles:
                                await inter.response.defer()
                                await member.add_roles(shulker_role)
                                await member.remove_roles(player_role)
                                await channel_logs.send(embed=logs)
                                await inter.message.edit(embed=embed, view=buttons_waiting_closure)

                                try:
                                    await member.send(embed=member_embed_donate)
                                except BaseException:
                                    pass
                                return

                            await inter.response.defer()
                            await member.add_roles(shulker_role)
                            await channel_logs.send(embed=logs)
                            await inter.message.edit(embed=embed, view=buttons_waiting_closure)

                            try:
                                await member.send(embed=member_embed_donate)
                            except BaseException:
                                pass
                        else:
                            await inter.send(content=f"У участника уже есть роль {shulker_role.mention}!", ephemeral=True)

                    if inter.component.custom_id == "remove_ender_button":
                        if ender_role in member.roles:
                            embed = disnake.Embed(
                                color=0x2f3136,
                                title="Роль была убрана!",
                                description=f"**Роль {ender_role.mention} снята у участника {member.mention}.**",
                                timestamp=now)

                            embed.set_author(
                                name=f"Снял роль: {inter.author}",
                                icon_url=inter.author.display_avatar)

                            logs = disnake.Embed(
                                title="Была убрана роль!", color=0x2f3136, timestamp=now)
                            logs.add_field(
                                name="Участник", value=member.mention)
                            logs.add_field(
                                name="ID участника", value=member.id)
                            logs.add_field(
                                name="Убранная роль", value=ender_role.mention)
                            logs.add_field(
                                name="ID роли", value=ender_role.id)
                            logs.add_field(
                                name="Участник, который снял роль",
                                value=inter.author.mention)
                            logs.add_field(
                                name="ID участника, который снял роль",
                                value=inter.author.id)

                            await inter.response.defer()
                            await member.remove_roles(ender_role)
                            await channel_logs.send(embed=logs)
                            await inter.message.edit(embed=embed, view=buttons_waiting_closure)
                        else:
                            await inter.send(content=f"У участника нету роли {ender_role.mention}!", ephemeral=True)

                    if inter.component.custom_id == "remove_phantom_button":
                        if phantom_role in member.roles:
                            embed = disnake.Embed(
                                color=0x2f3136,
                                title="Роль была убрана!",
                                description=f"**Роль {phantom_role.mention} снята у участника {member.mention}.**",
                                timestamp=now)

                            embed.set_author(
                                name=f"Снял роль: {inter.author}",
                                icon_url=inter.author.display_avatar)

                            logs = disnake.Embed(
                                title="Была убрана роль!", color=0x2f3136, timestamp=now)
                            logs.add_field(
                                name="Участник", value=member.mention)
                            logs.add_field(
                                name="ID участника", value=member.id)
                            logs.add_field(
                                name="Убранная роль", value=phantom_role.mention)
                            logs.add_field(
                                name="ID роли", value=phantom_role.id)
                            logs.add_field(
                                name="Участник, который снял роль",
                                value=inter.author.mention)
                            logs.add_field(
                                name="ID участника, который снял роль",
                                value=inter.author.id)

                            await inter.response.defer()
                            await member.remove_roles(phantom_role)
                            await channel_logs.send(embed=logs)
                            await inter.message.edit(embed=embed, view=buttons_waiting_closure)
                        else:
                            await inter.send(content=f"У участника нету роли {phantom_role.mention}!", ephemeral=True)

                    if inter.component.custom_id == "remove_guardian_button":
                        if guardian_role in member.roles:
                            embed = disnake.Embed(
                                color=0x2f3136,
                                title="Роль была убрана!",
                                description=f"**Роль {guardian_role.mention} снята у участника {member.mention}.**",
                                timestamp=now)

                            embed.set_author(
                                name=f"Снял роль: {inter.author}",
                                icon_url=inter.author.display_avatar)

                            logs = disnake.Embed(
                                title="Была убрана роль!", color=0x2f3136, timestamp=now)
                            logs.add_field(
                                name="Участник", value=member.mention)
                            logs.add_field(
                                name="ID участника", value=member.id)
                            logs.add_field(
                                name="Убранная роль", value=guardian_role.mention)
                            logs.add_field(
                                name="ID роли", value=guardian_role.id)
                            logs.add_field(
                                name="Участник, который снял роль",
                                value=inter.author.mention)
                            logs.add_field(
                                name="ID участника, который снял роль",
                                value=inter.author.id)

                            await inter.response.defer()
                            await member.remove_roles(guardian_role)
                            await channel_logs.send(embed=logs)
                            await inter.message.edit(embed=embed, view=buttons_waiting_closure)
                        else:
                            await inter.send(content=f"У участника нету роли {guardian_role.mention}!", ephemeral=True)

                    if inter.component.custom_id == "remove_shulker_button":
                        if shulker_role in member.roles:
                            embed = disnake.Embed(
                                color=0x2f3136,
                                title="Роль была убрана!",
                                description=f"**Роль {shulker_role.mention} снята у участника {member.mention}.**",
                                timestamp=now)

                            embed.set_author(
                                name=f"Снял роль: {inter.author}",
                                icon_url=inter.author.display_avatar)

                            logs = disnake.Embed(
                                title="Была убрана роль!", color=0x2f3136, timestamp=now)
                            logs.add_field(
                                name="Участник", value=member.mention)
                            logs.add_field(
                                name="ID участника", value=member.id)
                            logs.add_field(
                                name="Убранная роль", value=shulker_role.mention)
                            logs.add_field(
                                name="ID роли", value=shulker_role.id)
                            logs.add_field(
                                name="Участник, который снял роль",
                                value=inter.author.mention)
                            logs.add_field(
                                name="ID участника, который снял роль",
                                value=inter.author.id)

                            await inter.response.defer()
                            await member.remove_roles(shulker_role)
                            await channel_logs.send(embed=logs)
                            await inter.message.edit(embed=embed, view=buttons_waiting_closure)
                        else:
                            await inter.send(content=f"У участника нету роли {shulker_role.mention}!", ephemeral=True)

                    if inter.component.custom_id == "remove_player_button":
                        if player_role in member.roles:
                            embed = disnake.Embed(
                                color=0x2f3136,
                                title="Роль была убрана!",
                                description=f"**Роль {player_role.mention} снята у участника {member.mention}.**",
                                timestamp=now)

                            embed.set_author(
                                name=f"Снял роль: {inter.author}",
                                icon_url=inter.author.display_avatar)

                            logs = disnake.Embed(
                                title="Была убрана роль!", color=0x2f3136, timestamp=now)
                            logs.add_field(
                                name="Участник", value=member.mention)
                            logs.add_field(
                                name="ID участника", value=member.id)
                            logs.add_field(
                                name="Убранная роль", value=player_role.mention)
                            logs.add_field(
                                name="ID роли", value=player_role.id)
                            logs.add_field(
                                name="Участник, который снял роль",
                                value=inter.author.mention)
                            logs.add_field(
                                name="ID участника, который снял роль",
                                value=inter.author.id)

                            await inter.response.defer()
                            await member.remove_roles(player_role)
                            await channel_logs.send(embed=logs)
                            await inter.message.edit(embed=embed, view=buttons_waiting_closure)
                        else:
                            await inter.send(content=f"У участника нету роли {player_role.mention}!", ephemeral=True)
                else:
                    await inter.send(content="Данную заявку рассматривает другой человек!", ephemeral=True)


def setup(bot):
    bot.remove_cog(MinecraftDonateSystem(bot))
