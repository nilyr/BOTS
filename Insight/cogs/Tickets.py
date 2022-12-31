import disnake
import sqlite3
from disnake import ButtonStyle
from disnake.ext import commands
from disnake.ui import View, Button, Select

with sqlite3.connect("database (Insight).db") as db:
    cursor = db.cursor()

    class Tickets(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.command(name="tickets")
        async def ticketsinformation(self, ctx):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            guild_kp = self.bot.get_guild(387409949442965506)

            if perms_owner is not None or perms_dev is not None:
                if ctx.guild == guild_kp:
                    channel_tickets = self.bot.get_channel(738771385949749338)

                    tickets_menu = View()
                    tickets_menu.add_item(Select(placeholder="Выберите по какой из тем хотите создать тикет.", custom_id="tickets_menu",
                    options = [disnake.SelectOption(emoji="<a:No_Check:877264845366517770>", label="Не выбрано", value="default_option", default=True),
                            disnake.SelectOption(emoji="<a:question_red:916001629122216036>", label="Обращения к персоналу", value="tickets"),
                            disnake.SelectOption(emoji="<a:tochka_anim:965680033807101952>", label="Жалобы на персонал", value="complaints_staff"),
                            disnake.SelectOption(emoji="<:members:885624936901787738>", label="Жалобы на участников", value="complaints_members")]))

                    embed = disnake.Embed(
                        color=0x2f3136,
                        title="Тикеты",
                        description="В данном канале, нажав на меню, вы можете создать обращения по разным вопросам.")

                    embed.set_footer(
                        text="Запрещается создание обращений без должной на то причины.")
                    embed.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/936998470877851668/support.gif")

                    await ctx.message.delete()
                    await channel_tickets.send(embed=embed, view=tickets_menu)
                    return

            await ctx.message.delete(delay=5)
            await ctx.reply(content="Права на использование есть только у разработчика бота.", delete_after=5)

        @commands.slash_command(name="tickets-clear", description="Удаление закрытых тикетов", guild_ids=[387409949442965506])
        async def ticketschannelclear(self, ctx):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            guild_kp = self.bot.get_guild(387409949442965506)

            if ctx.guild == guild_kp:
                closed_button = View()
                closed_button.add_item(
                    Button(
                        style=ButtonStyle.grey,
                        label="Обращения к персоналу",
                        custom_id="clear_ticket_closed_button"))
                closed_button.add_item(
                    Button(
                        style=ButtonStyle.grey,
                        label="Жалобы на персонал",
                        custom_id="clear_complaints_staff_closed_button"))
                closed_button.add_item(
                    Button(
                        style=ButtonStyle.grey,
                        label="Жалобы на участников",
                        custom_id="clear_complaints_members_closed_button"))

                if perms_owner is not None or perms_dev is not None:
                    await ctx.send(content="Выберите категорию удалённых закрытых каналов.", view=closed_button, ephemeral=True)
                    return
                
                await ctx.send(content="Недостаточно прав.", ephemeral=True)

        @commands.Cog.listener()
        async def on_dropdown(self, inter):
            guild_kp = self.bot.get_guild(387409949442965506)

            if inter.guild == guild_kp:
                ticket_waiting_category = disnake.utils.get(inter.guild.categories, id=1017466409439219732)

                complaints_staff_category = disnake.utils.get(inter.guild.categories, id=1017468432716931102)
                complaints_members_category = disnake.utils.get(inter.guild.categories, id=1017468480099983391)

                mute_role = disnake.utils.get(inter.guild.roles, id=1028711769599909959)
                mute_voice_role = disnake.utils.get(inter.guild.roles, id=574291156431536132)

                if inter.component.custom_id == "tickets_menu":
                    if "tickets" in inter.values:
                        ticket_created_waiting = cursor.execute(f"""SELECT author_id FROM tickets WHERE author_id = {inter.author.id} AND guild_id == {inter.guild.id} AND status == 'WAITING'""").fetchone()
                        ticket_created_processing = cursor.execute(f"""SELECT author_id FROM tickets WHERE author_id = {inter.author.id} AND guild_id == {inter.guild.id} AND status == 'PROCESSING'""").fetchone()

                        support_button = View()
                        support_button.add_item(
                            Button(
                                style=ButtonStyle.grey,
                                label="Взять обращение",
                                custom_id="take_ticket"))

                        if mute_role in inter.author.roles or mute_voice_role in inter.author.roles:
                            await inter.send("Вы заглушены.", ephemeral=True)
                            return

                        if ticket_created_waiting is not None or ticket_created_processing is not None:
                            await inter.send("Вы уже создали обращение.", ephemeral=True)
                            return

                        await inter.send(content=f"<a:waiting:1011657420860293180> Обращение создаётся...", ephemeral=True)
                        msg = await inter.original_message()

                        cursor.execute("""UPDATE tickets_numbers SET numbers = numbers + 1""")
                        db.commit()

                        tickets_numbering = cursor.execute("""SELECT numbers FROM tickets_numbers""").fetchone()[0]
                        ticket_channel = await ticket_waiting_category.create_text_channel(f"ticket-{tickets_numbering}")

                        embed_msg = await ticket_channel.send(content="Создание обращения...")
                        
                        cursor.execute(f"""INSERT INTO tickets VALUES ({inter.guild.id}, 'WAITING', {inter.author.id}, 'None', {ticket_channel.id})""")
                        db.commit()

                        author_ticket_db = cursor.execute(f"""SELECT author_id FROM tickets WHERE author_id = {inter.author.id} AND channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                        author_ticket = inter.guild.get_member(author_ticket_db)

                        support_ticket = cursor.execute(f"""SELECT support_id FROM tickets WHERE author_id = {inter.author.id} AND channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                        
                        embed = disnake.Embed(
                            description="Напишите свой вопрос и ожидайте ответ от персонала.",
                            color=0x2f3136)
                        embed.add_field(name="Создал обращение", value=author_ticket.mention)
                        
                        if support_ticket == "None":
                            embed.add_field(name="Обрабатывает обращение", value="Никто")

                        await embed_msg.edit(content=f"\nОбращение от {author_ticket.mention} | `{author_ticket.id}`", embed=embed, view=support_button)
                        await ticket_channel.set_permissions(author_ticket, read_messages=True, send_messages=True)
                        await msg.edit(content=f"Обращение создано. Для его заполнения перейдите в канал {ticket_channel.mention}.")

                    if "complaints_staff" in inter.values:
                        complaints_staff_created_waiting = cursor.execute(f"""SELECT author_id FROM staff_complaints WHERE author_id = {inter.author.id} AND guild_id == {inter.guild.id} AND status == 'WAITING'""").fetchone()
                        complaints_staff_created_processing = cursor.execute(f"""SELECT author_id FROM staff_complaints WHERE author_id = {inter.author.id} AND guild_id == {inter.guild.id} AND status == 'PROCESSING'""").fetchone()

                        support_button = View()
                        support_button.add_item(
                            Button(
                                style=ButtonStyle.grey,
                                label="Взять жалобу",
                                custom_id="take_complaints_staff"))

                        if mute_role in inter.author.roles or mute_voice_role in inter.author.roles:
                            await inter.send("Вы заглушены.", ephemeral=True)
                            return

                        if complaints_staff_created_waiting is not None or complaints_staff_created_processing is not None:
                            await inter.send("Вы уже создали жалобу на персонал.", ephemeral=True)
                            return

                        await inter.send(content=f"Ябеда корябеда\n<a:waiting:1011657420860293180> Жалоба создаётся...", ephemeral=True)
                        msg = await inter.original_message()

                        cursor.execute("""UPDATE staff_complaints_numbers SET numbers = numbers + 1""")
                        db.commit()

                        staff_complaints_numbering = cursor.execute("""SELECT numbers FROM staff_complaints_numbers""").fetchone()[0]
                        ticket_channel = await complaints_staff_category.create_text_channel(f"complaints-staff-{staff_complaints_numbering}")

                        embed_msg = await ticket_channel.send(content="Создание жалобы...")
                        
                        cursor.execute(f"""INSERT INTO staff_complaints VALUES ({inter.guild.id}, 'WAITING', {inter.author.id}, 'None', {ticket_channel.id})""")
                        db.commit()

                        author_ticket_db = cursor.execute(f"""SELECT author_id FROM staff_complaints WHERE author_id = {inter.author.id} AND channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                        author_ticket = inter.guild.get_member(author_ticket_db)

                        support_ticket = cursor.execute(f"""SELECT support_id FROM staff_complaints WHERE author_id = {inter.author.id} AND channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                        
                        embed = disnake.Embed(
                            description="Напишите свою жалобу по форме и ожидайте ответ от персонала.",
                            color=0x2f3136)
                        embed.set_author(name="Жалобы на персонал")
                        embed.add_field(name="Форма жалобы:", value="1. Discord нарушающего.\n2. Что пользователь нарушил.\n3. Доказательства.", inline=False)
                        embed.add_field(name="Создал жалобу", value=author_ticket.mention)
                        
                        if support_ticket == "None":
                            embed.add_field(name="Обрабатывает жалобу", value="Никто")

                        await embed_msg.edit(content=f"\nЖалоба от {author_ticket.mention} | `{author_ticket.id}`", embed=embed, view=support_button)
                        await ticket_channel.set_permissions(author_ticket, read_messages=True, send_messages=True)
                        await msg.edit(content=f"Ябеда корябеда\nЖалоба создана. Для её заполнения перейдите в канал {ticket_channel.mention}.")

                    if "complaints_members" in inter.values:
                        complaints_members_created_waiting = cursor.execute(f"""SELECT author_id FROM member_complaints WHERE author_id = {inter.author.id} AND guild_id == {inter.guild.id} AND status == 'WAITING'""").fetchone()
                        complaints_members_created_processing = cursor.execute(f"""SELECT author_id FROM member_complaints WHERE author_id = {inter.author.id} AND guild_id == {inter.guild.id} AND status == 'PROCESSING'""").fetchone()

                        support_button = View()
                        support_button.add_item(
                            Button(
                                style=ButtonStyle.grey,
                                label="Взять жалобу",
                                custom_id="take_complaints_members"))

                        if mute_role in inter.author.roles or mute_voice_role in inter.author.roles:
                            await inter.send("Вы заглушены.", ephemeral=True)
                            return

                        if complaints_members_created_waiting is not None or complaints_members_created_processing is not None:
                            await inter.send("Вы уже создали жалобу на участника.", ephemeral=True)
                            return

                        await inter.send(content=f"Ябеда корябеда\n<a:waiting:1011657420860293180> Жалоба создаётся...", ephemeral=True)
                        msg = await inter.original_message()

                        cursor.execute("""UPDATE member_complaints_numbers SET numbers = numbers + 1""")
                        db.commit()

                        member_complaints_numbering = cursor.execute("""SELECT numbers FROM member_complaints_numbers""").fetchone()[0]
                        ticket_channel = await complaints_members_category.create_text_channel(f"complaints-members-{member_complaints_numbering}")

                        embed_msg = await ticket_channel.send(content="Создание жалобы...")
                        
                        cursor.execute(f"""INSERT INTO member_complaints VALUES ({inter.guild.id}, 'WAITING', {inter.author.id}, 'None', {ticket_channel.id})""")
                        db.commit()

                        author_ticket_db = cursor.execute(f"""SELECT author_id FROM member_complaints WHERE author_id = {inter.author.id} AND channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                        author_ticket = inter.guild.get_member(author_ticket_db)

                        support_ticket = cursor.execute(f"""SELECT support_id FROM member_complaints WHERE author_id = {inter.author.id} AND channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                        
                        embed = disnake.Embed(
                            description="Напишите свою жалобу по форме и ожидайте ответ от персонала.",
                            color=0x2f3136)
                        embed.set_author(name="Жалобы на участников")
                        embed.add_field(name="Форма жалобы:", value="1. Discord нарушающего.\n2. Что пользователь нарушил.\n3. Доказательства.", inline=False)
                        embed.add_field(name="Создал жалобу", value=author_ticket.mention)
                        
                        if support_ticket == "None":
                            embed.add_field(name="Обрабатывает жалобу", value="Никто")

                        await embed_msg.edit(content=f"\nЖалоба от {author_ticket.mention} | `{author_ticket.id}`", embed=embed, view=support_button)
                        await ticket_channel.set_permissions(author_ticket, read_messages=True, send_messages=True)
                        await msg.edit(content=f"Ябеда корябеда\nЖалоба создана. Для её заполнения перейдите в канал {ticket_channel.mention}.")

        @commands.Cog.listener()
        async def on_button_click(self, inter):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {inter.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {inter.author.id} AND lvl_rights = 'DEV'""").fetchone()

            guild_kp = self.bot.get_guild(387409949442965506)

            if inter.guild == guild_kp:
                channel_logs = self.bot.get_channel(1017474717432688690)

                ticket_processing_category = disnake.utils.get(inter.guild.categories, id=1017466449322844341)
                
                ticket_closed_category = disnake.utils.get(inter.guild.categories, id=1017466513856397323)
                complaints_staff_closed_category = disnake.utils.get(inter.guild.categories, id=1029139609214529568)
                complaints_members_closed_category = disnake.utils.get(inter.guild.categories, id=1029139889540833310)

                clear_ticket_closed_category = disnake.utils.get(inter.guild.categories, id=1017466513856397323)
                clear_complaints_staff_closed_category = disnake.utils.get(inter.guild.categories, id=1029139609214529568)
                clear_complaints_members_closed_category = disnake.utils.get(inter.guild.categories, id=1029139889540833310)

                support_administration_role = disnake.utils.get(inter.guild.roles, id=423159755117166592)
                moderator_role = disnake.utils.get(inter.guild.roles, id=593799068606660619)
                helper_role = disnake.utils.get(inter.guild.roles, id=485843253481177091)
                overseer_role = disnake.utils.get(inter.guild.roles, id=538725888276168735)
                overseer_isp_role = disnake.utils.get(inter.guild.roles, id=575666099408994316)

                if inter.component.custom_id == "take_ticket":
                    support_button = View()
                    support_button.add_item(
                        Button(
                            style=ButtonStyle.red,
                            label="Закрыть обращение",
                            custom_id="close_ticket"))

                    ticket_channel = inter.guild.get_channel(inter.channel.id)

                    author_ticket_db = cursor.execute(f"""SELECT author_id FROM tickets WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    author_ticket = inter.guild.get_member(author_ticket_db)

                    if author_ticket == inter.author:
                        await inter.send(content="Вы не можете обрабатывать собственное обращение.", ephemeral=True)
                        return

                    try:
                        if not inter.guild.get_member(author_ticket.id):
                            await inter.response.defer()
                            await inter.message.edit(view=None)
                            await inter.channel.send(content=f"Обращение закрыто, участник вышел.")
                            
                            cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                            db.commit()

                            await ticket_channel.edit(category=ticket_closed_category)
                            return
                    except BaseException:
                        await inter.response.defer()
                        await inter.message.edit(view=None)
                        await inter.channel.send(content=f"Обращение закрыто, участник вышел.")
                        
                        cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                        db.commit()

                        await ticket_channel.edit(category=ticket_closed_category)
                        return

                    cursor.execute(f"""UPDATE tickets SET support_id = {inter.author.id} WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                    cursor.execute(f"""UPDATE tickets SET status = 'PROCESSING' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                    db.commit()

                    support_ticket_db = cursor.execute(f"""SELECT support_id FROM tickets WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    support_ticket = inter.guild.get_member(support_ticket_db)

                    embed = disnake.Embed(
                        description="Напишите свой вопрос и ожидайте ответ от персонала.",
                        color=0x2f3136)
                    embed.add_field(name="Форма жалобы:", value="1. Discord нарушающего.\n2. Что пользователь нарушил.\n3. Доказательства.", inline=False)
                    embed.add_field(name="Создал обращение", value=author_ticket.mention)
                    embed.add_field(name="Обрабатывает обращение", value=support_ticket.mention)

                    await inter.response.defer()

                    await inter.message.edit(content=f"\nОбращение от {author_ticket.mention} | `{author_ticket.id}`", embed=embed, view=support_button)
                    await ticket_channel.edit(category=ticket_processing_category)
                    
                    await ticket_channel.set_permissions(support_administration_role, overwrite=None)
                    await ticket_channel.set_permissions(moderator_role, overwrite=None)
                    await ticket_channel.set_permissions(helper_role, overwrite=None)
                    await ticket_channel.set_permissions(overseer_role, overwrite=None)
                    await ticket_channel.set_permissions(overseer_isp_role, overwrite=None)
                    await ticket_channel.set_permissions(support_ticket, read_messages=True, send_messages=True)

                if inter.component.custom_id == "take_complaints_staff":
                    support_button = View()
                    support_button.add_item(
                        Button(
                            style=ButtonStyle.red,
                            label="Закрыть жалобу",
                            custom_id="close_complaints_staff"))

                    ticket_channel = inter.guild.get_channel(inter.channel.id)

                    author_ticket_db = cursor.execute(f"""SELECT author_id FROM staff_complaints WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    author_ticket = inter.guild.get_member(author_ticket_db)

                    if author_ticket == inter.author:
                        await inter.send(content="Вы не можете обрабатывать собственную жалобу.", ephemeral=True)
                        return

                    try:
                        if not inter.guild.get_member(author_ticket.id):
                            await inter.response.defer()
                            await inter.message.edit(view=None)
                            await inter.channel.send(content=f"Жалоба закрыта, участник вышел.")
                            
                            cursor.execute(f"""UPDATE staff_complaints SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                            db.commit()

                            await ticket_channel.edit(category=complaints_staff_closed_category)
                            return
                    except BaseException:
                        await inter.response.defer()
                        await inter.message.edit(view=None)
                        await inter.channel.send(content=f"Жалоба закрыта, участник вышел.")
                        
                        cursor.execute(f"""UPDATE staff_complaints SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                        db.commit()

                        await ticket_channel.edit(category=complaints_staff_closed_category)
                        return

                    cursor.execute(f"""UPDATE staff_complaints SET support_id = {inter.author.id} WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                    cursor.execute(f"""UPDATE staff_complaints SET status = 'PROCESSING' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                    db.commit()

                    support_ticket_db = cursor.execute(f"""SELECT support_id FROM staff_complaints WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    support_ticket = inter.guild.get_member(support_ticket_db)

                    embed = disnake.Embed(
                        description="Напишите свою жалобу по форме и ожидайте ответ от персонала.",
                        color=0x2f3136)
                    embed.set_author(name="Жалобы на персонал")
                    embed.add_field(name="Форма жалобы:", value="1. Discord нарушающего.\n2. Что пользователь нарушил.\n3. Доказательства.", inline=False)
                    embed.add_field(name="Создал жалобу", value=author_ticket.mention)
                    embed.add_field(name="Обрабатывает жалобу", value=support_ticket.mention)

                    await inter.response.defer()
                    await inter.message.edit(content=f"\nЖалоба от {author_ticket.mention} | `{author_ticket.id}`", embed=embed, view=support_button)
                    
                    await ticket_channel.set_permissions(support_administration_role, overwrite=None)
                    await ticket_channel.set_permissions(support_ticket, read_messages=True, send_messages=True)

                if inter.component.custom_id == "take_complaints_members":
                    support_button = View()
                    support_button.add_item(
                        Button(
                            style=ButtonStyle.red,
                            label="Закрыть жалобу",
                            custom_id="close_complaints_members"))

                    ticket_channel = inter.guild.get_channel(inter.channel.id)

                    author_ticket_db = cursor.execute(f"""SELECT author_id FROM member_complaints WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    author_ticket = inter.guild.get_member(author_ticket_db)

                    if author_ticket == inter.author:
                        await inter.send(content="Вы не можете обрабатывать собственную жалобу.", ephemeral=True)
                        return

                    try:
                        if not inter.guild.get_member(author_ticket.id):
                            await inter.response.defer()
                            await inter.message.edit(view=None)
                            await inter.channel.send(content=f"Жалоба закрыта, участник вышел.")
                            
                            cursor.execute(f"""UPDATE member_complaints SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                            db.commit()

                            await ticket_channel.edit(category=complaints_members_closed_category)
                            return
                    except BaseException:
                        await inter.response.defer()
                        await inter.message.edit(view=None)
                        await inter.channel.send(content=f"Жалоба закрыта, участник вышел.")
                        
                        cursor.execute(f"""UPDATE member_complaints SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                        db.commit()

                        await ticket_channel.edit(category=complaints_members_closed_category)
                        return

                    cursor.execute(f"""UPDATE member_complaints SET support_id = {inter.author.id} WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                    cursor.execute(f"""UPDATE member_complaints SET status = 'PROCESSING' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                    db.commit()

                    support_ticket_db = cursor.execute(f"""SELECT support_id FROM member_complaints WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    support_ticket = inter.guild.get_member(support_ticket_db)

                    embed = disnake.Embed(
                        description="Напишите свою жалобу по форме и ожидайте ответ от персонала.",
                        color=0x2f3136)
                    embed.set_author(name="Жалобы на участников")
                    embed.add_field(name="Форма жалобы:", value="1. Discord нарушающего.\n2. Что пользователь нарушил.\n3. Доказательства.", inline=False)
                    embed.add_field(name="Создал жалобу", value=author_ticket.mention)
                    embed.add_field(name="Обрабатывает жалобу", value=support_ticket.mention)

                    await inter.response.defer()
                    await inter.message.edit(content=f"\nЖалоба от {author_ticket.mention} | `{author_ticket.id}`", embed=embed, view=support_button)
                    
                    await ticket_channel.set_permissions(support_administration_role, overwrite=None)
                    await ticket_channel.set_permissions(moderator_role, overwrite=None)
                    await ticket_channel.set_permissions(helper_role, overwrite=None)
                    await ticket_channel.set_permissions(overseer_role, overwrite=None)
                    await ticket_channel.set_permissions(overseer_isp_role, overwrite=None)
                    await ticket_channel.set_permissions(support_ticket, read_messages=True, send_messages=True)

                if inter.component.custom_id == "close_ticket":
                    ticket_channel = inter.guild.get_channel(inter.channel.id)

                    support_ticket_db = cursor.execute(f"""SELECT support_id FROM tickets WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    support_ticket = inter.guild.get_member(support_ticket_db)

                    if support_ticket == inter.author:
                        assessment_button = View()
                        assessment_button.add_item(
                            Button(
                                style=ButtonStyle.grey,
                                emoji="<:branding:1004492631117664287>",
                                label="1",
                                custom_id="assessment_1"))
                        assessment_button.add_item(
                            Button(
                                style=ButtonStyle.grey,
                                emoji="<:branding:1004492631117664287>",
                                label="2",
                                custom_id="assessment_2"))
                        assessment_button.add_item(
                            Button(
                                style=ButtonStyle.grey,
                                emoji="<:branding:1004492631117664287>",
                                label="3",
                                custom_id="assessment_3"))
                        assessment_button.add_item(
                            Button(
                                style=ButtonStyle.grey,
                                emoji="<:branding:1004492631117664287>",
                                label="4",
                                custom_id="assessment_4"))
                        assessment_button.add_item(
                            Button(
                                style=ButtonStyle.grey,
                                emoji="<:branding:1004492631117664287>",
                                label="5",
                                custom_id="assessment_5"))
                        assessment_button.add_item(
                            Button(
                                style=ButtonStyle.blurple,
                                label="Принудительное закрытие обращения",
                                custom_id="enforcement_ticket"))

                        author_ticket_db = cursor.execute(f"""SELECT author_id FROM tickets WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                        author_ticket = inter.guild.get_member(author_ticket_db)

                        try:
                            if not inter.guild.get_member(author_ticket.id):
                                await inter.response.defer()
                                await inter.message.edit(view=None)
                                await inter.channel.send(content=f"{support_ticket.mention}\nОбращение закрыто, участник вышел.")

                                await ticket_channel.set_permissions(support_ticket, overwrite=None)
                                await ticket_channel.set_permissions(support_administration_role, read_messages=True, send_messages=False)
                                
                                cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                                db.commit()

                                await ticket_channel.edit(category=ticket_closed_category)
                                return
                        except BaseException:
                            await inter.response.defer()
                            await inter.message.edit(view=None)
                            await inter.channel.send(content=f"{support_ticket.mention}\nОбращение закрыто, участник вышел.")

                            await ticket_channel.set_permissions(support_ticket, overwrite=None)
                            await ticket_channel.set_permissions(support_administration_role, read_messages=True, send_messages=False)
                            
                            cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                            db.commit()

                            await ticket_channel.edit(category=ticket_closed_category)
                            return

                        embed = disnake.Embed(
                            title="Оценка обращения",
                            description="Пожалуйста, оцените работу человека, обрабатывающего ваш тикет.",
                            color=0x2f3136)

                        await inter.response.defer()
                        await inter.message.edit(view=None)
                        await ticket_channel.edit(category=ticket_closed_category)
                        await ticket_channel.set_permissions(author_ticket, read_messages=True, send_messages=False)
                        await ticket_channel.set_permissions(support_ticket, read_messages=True, send_messages=False)
                        await ticket_channel.send(content=author_ticket.mention, embed=embed, view=assessment_button)
                        return
                    
                    await inter.send(content="На эту кнопку может нажимать только тот человек, который обрабатывает данный тикет.", ephemeral=True)
                
                if inter.component.custom_id == "close_complaints_staff":
                    ticket_channel = inter.guild.get_channel(inter.channel.id)

                    author_ticket_db = cursor.execute(f"""SELECT author_id FROM staff_complaints WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    author_ticket = inter.guild.get_member(author_ticket_db)

                    support_ticket_db = cursor.execute(f"""SELECT support_id FROM staff_complaints WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    support_ticket = inter.guild.get_member(support_ticket_db)

                    if support_ticket == inter.author:
                        try:
                            if not inter.guild.get_member(author_ticket.id):
                                await inter.response.defer()
                                await inter.message.edit(view=None)
                                await inter.channel.send(content=f"{support_ticket.mention}\nЖалоба закрыта, участник вышел.")

                                await ticket_channel.set_permissions(support_ticket, overwrite=None)
                                await ticket_channel.set_permissions(support_administration_role, read_messages=True, send_messages=False)
                                
                                cursor.execute(f"""UPDATE staff_complaints SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                                db.commit()

                                await ticket_channel.edit(category=complaints_staff_closed_category)
                                return
                        except BaseException:
                            await inter.response.defer()
                            await inter.message.edit(view=None)
                            await inter.channel.send(content=f"{support_ticket.mention}\nЖалоба закрыта, участник вышел.")

                            await ticket_channel.set_permissions(support_ticket, overwrite=None)
                            await ticket_channel.set_permissions(support_administration_role, read_messages=True, send_messages=False)
                            
                            cursor.execute(f"""UPDATE staff_complaints SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                            db.commit()

                            await ticket_channel.edit(category=complaints_staff_closed_category)
                            return

                        await inter.response.defer()
                        await inter.message.edit(view=None)
                        await inter.channel.send(content=f"Жалоба закрыта {support_ticket.mention}.")

                        await ticket_channel.set_permissions(author_ticket, overwrite=None)
                        await ticket_channel.set_permissions(support_ticket, overwrite=None)
                        await ticket_channel.set_permissions(support_administration_role, read_messages=True, send_messages=False)
                        
                        cursor.execute(f"""UPDATE staff_complaints SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                        db.commit()

                        await ticket_channel.edit(category=complaints_staff_closed_category)
                        return
                    
                    await inter.send(content="На эту кнопку может нажимать только тот человек, который обрабатывает данный тикет.", ephemeral=True)

                if inter.component.custom_id == "close_complaints_members":
                    ticket_channel = inter.guild.get_channel(inter.channel.id)

                    author_ticket_db = cursor.execute(f"""SELECT author_id FROM member_complaints WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    author_ticket = inter.guild.get_member(author_ticket_db)

                    support_ticket_db = cursor.execute(f"""SELECT support_id FROM member_complaints WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    support_ticket = inter.guild.get_member(support_ticket_db)

                    if support_ticket == inter.author:
                        try:
                            if not inter.guild.get_member(author_ticket.id):
                                await inter.response.defer()
                                await inter.message.edit(view=None)
                                await inter.channel.send(content=f"{support_ticket.mention}\nЖалоба закрыта, участник вышел.")

                                await ticket_channel.set_permissions(support_ticket, overwrite=None)
                                await ticket_channel.set_permissions(support_administration_role, read_messages=True, send_messages=False)
                                
                                cursor.execute(f"""UPDATE member_complaints SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                                db.commit()

                                await ticket_channel.edit(category=complaints_members_closed_category)
                                return
                        except BaseException:
                            await inter.response.defer()
                            await inter.message.edit(view=None)
                            await inter.channel.send(content=f"{support_ticket.mention}\nЖалоба закрыта, участник вышел.")

                            await ticket_channel.set_permissions(support_ticket, overwrite=None)
                            await ticket_channel.set_permissions(support_administration_role, read_messages=True, send_messages=False)
                            
                            cursor.execute(f"""UPDATE member_complaints SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                            db.commit()

                            await ticket_channel.edit(category=complaints_members_closed_category)
                            return

                        await inter.response.defer()
                        await inter.message.edit(view=None)
                        await inter.channel.send(content=f"Жалоба закрыта {support_ticket.mention}.")

                        await ticket_channel.set_permissions(author_ticket, overwrite=None)
                        await ticket_channel.set_permissions(support_ticket, overwrite=None)
                        await ticket_channel.set_permissions(support_administration_role, read_messages=True, send_messages=False)
                        
                        cursor.execute(f"""UPDATE member_complaints SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                        db.commit()

                        await ticket_channel.edit(category=complaints_members_closed_category)
                        return
                    
                    await inter.send(content="На эту кнопку может нажимать только тот человек, который обрабатывает данный тикет.", ephemeral=True)

                if inter.component.custom_id == "enforcement_ticket":
                    ticket_channel = inter.guild.get_channel(inter.channel.id)

                    author_ticket_db = cursor.execute(f"""SELECT author_id FROM tickets WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    author_ticket = inter.guild.get_member(author_ticket_db)

                    support_ticket_db = cursor.execute(f"""SELECT support_id FROM tickets WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    support_ticket = inter.guild.get_member(support_ticket_db)

                    if support_ticket == inter.author:
                        try:
                            if not inter.guild.get_member(author_ticket.id):
                                await inter.response.defer()
                                await inter.message.edit(view=None)
                                await inter.channel.send(content=f"{support_ticket.mention}\nОбращение закрыто, участник вышел.")

                                await ticket_channel.set_permissions(support_ticket, overwrite=None)
                                await ticket_channel.set_permissions(support_administration_role, read_messages=True, send_messages=False)
                                
                                cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                                db.commit()

                                await ticket_channel.edit(category=ticket_closed_category)
                                return
                        except BaseException:
                            await inter.response.defer()
                            await inter.message.edit(view=None)
                            await inter.channel.send(content=f"{support_ticket.mention}\nОбращение закрыто, участник вышел.")

                            await ticket_channel.set_permissions(support_ticket, overwrite=None)
                            await ticket_channel.set_permissions(support_administration_role, read_messages=True, send_messages=False)
                            
                            cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                            db.commit()

                            await ticket_channel.edit(category=ticket_closed_category)
                            return

                        await inter.response.defer()
                        await inter.message.edit(content=f"{support_ticket.mention} закрыл тикет досрочно.", embed=None, view=None)

                        await ticket_channel.set_permissions(author_ticket, overwrite=None)
                        await ticket_channel.set_permissions(support_ticket, overwrite=None)
                        await ticket_channel.set_permissions(support_administration_role, read_messages=True, send_messages=False)
                        
                        cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                        db.commit()

                        await ticket_channel.edit(category=ticket_closed_category)
                        return
                    
                    await inter.send(content="На эту кнопку может нажимать только тот человек, который обрабатывает данный тикет.", ephemeral=True)

                if inter.component.custom_id == "assessment_1":
                    ticket_channel = inter.guild.get_channel(inter.channel.id)

                    author_ticket_db = cursor.execute(f"""SELECT author_id FROM tickets WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    author_ticket = inter.guild.get_member(author_ticket_db)

                    support_ticket_db = cursor.execute(f"""SELECT support_id FROM tickets WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    support_ticket = inter.guild.get_member(support_ticket_db)

                    if author_ticket == inter.author:
                        embed_logs = disnake.Embed(
                            title="Оценка обращения",
                            description=f"{author_ticket.mention} оценил работу {support_ticket.mention} на **1** <:branding:1004492631117664287>.",
                            color=0x2f3136)

                        await inter.response.defer()
                        await inter.message.edit(content=f"{author_ticket.mention}, вы оценили работу {support_ticket.mention} на **1** <:branding:1004492631117664287>.", embed=None, view=None)
                        await channel_logs.send(content=support_ticket.mention, embed=embed_logs)

                        await ticket_channel.set_permissions(author_ticket, overwrite=None)
                        await ticket_channel.set_permissions(support_ticket, overwrite=None)
                        await ticket_channel.set_permissions(support_administration_role, read_messages=True, send_messages=False)
                        
                        cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                        db.commit()

                        await ticket_channel.edit(category=ticket_closed_category)
                        return
                    
                    await inter.send(content="На эту кнопку может нажимать только автор тикета.", ephemeral=True)

                if inter.component.custom_id == "assessment_2":
                    ticket_channel = inter.guild.get_channel(inter.channel.id)

                    author_ticket_db = cursor.execute(f"""SELECT author_id FROM tickets WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    author_ticket = inter.guild.get_member(author_ticket_db)

                    support_ticket_db = cursor.execute(f"""SELECT support_id FROM tickets WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    support_ticket = inter.guild.get_member(support_ticket_db)

                    if author_ticket == inter.author:
                        embed_logs = disnake.Embed(
                            title="Оценка обращения",
                            description=f"{author_ticket.mention} оценил работу {support_ticket.mention} на **2** <:branding:1004492631117664287>.",
                            color=0x2f3136)

                        await inter.response.defer()
                        await inter.message.edit(content=f"{author_ticket.mention}, вы оценили работу {support_ticket.mention} на **2** <:branding:1004492631117664287>.", embed=None, view=None)
                        await channel_logs.send(content=support_ticket.mention, embed=embed_logs)

                        await ticket_channel.set_permissions(author_ticket, overwrite=None)
                        await ticket_channel.set_permissions(support_ticket, overwrite=None)
                        await ticket_channel.set_permissions(support_administration_role, read_messages=True, send_messages=False)
                        
                        cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                        db.commit()

                        await ticket_channel.edit(category=ticket_closed_category)
                        return
                    
                    await inter.send(content="На эту кнопку может нажимать только автор тикета.", ephemeral=True)

                if inter.component.custom_id == "assessment_3":
                    ticket_channel = inter.guild.get_channel(inter.channel.id)

                    author_ticket_db = cursor.execute(f"""SELECT author_id FROM tickets WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    author_ticket = inter.guild.get_member(author_ticket_db)

                    support_ticket_db = cursor.execute(f"""SELECT support_id FROM tickets WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    support_ticket = inter.guild.get_member(support_ticket_db)

                    if author_ticket == inter.author:
                        embed_logs = disnake.Embed(
                            title="Оценка обращения",
                            description=f"{author_ticket.mention} оценил работу {support_ticket.mention} на **3** <:branding:1004492631117664287>.",
                            color=0x2f3136)

                        await inter.response.defer()
                        await inter.message.edit(content=f"{author_ticket.mention}, вы оценили работу {support_ticket.mention} на **3** <:branding:1004492631117664287>.", embed=None, view=None)
                        await channel_logs.send(content=support_ticket.mention, embed=embed_logs)

                        await ticket_channel.set_permissions(author_ticket, overwrite=None)
                        await ticket_channel.set_permissions(support_ticket, overwrite=None)
                        await ticket_channel.set_permissions(support_administration_role, read_messages=True, send_messages=False)
                        
                        cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                        db.commit()

                        await ticket_channel.edit(category=ticket_closed_category)
                        return
                    
                    await inter.send(content="На эту кнопку может нажимать только автор тикета.", ephemeral=True)

                if inter.component.custom_id == "assessment_4":
                    ticket_channel = inter.guild.get_channel(inter.channel.id)

                    author_ticket_db = cursor.execute(f"""SELECT author_id FROM tickets WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    author_ticket = inter.guild.get_member(author_ticket_db)

                    support_ticket_db = cursor.execute(f"""SELECT support_id FROM tickets WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    support_ticket = inter.guild.get_member(support_ticket_db)

                    if author_ticket == inter.author:
                        embed_logs = disnake.Embed(
                            title="Оценка обращения",
                            description=f"{author_ticket.mention} оценил работу {support_ticket.mention} на **4** <:branding:1004492631117664287>.",
                            color=0x2f3136)

                        await inter.response.defer()
                        await inter.message.edit(content=f"{author_ticket.mention}, вы оценили работу {support_ticket.mention} на **4** <:branding:1004492631117664287>.", embed=None, view=None)
                        await channel_logs.send(content=support_ticket.mention, embed=embed_logs)

                        await ticket_channel.set_permissions(author_ticket, overwrite=None)
                        await ticket_channel.set_permissions(support_ticket, overwrite=None)
                        await ticket_channel.set_permissions(support_administration_role, read_messages=True, send_messages=False)
                        
                        cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                        db.commit()

                        await ticket_channel.edit(category=ticket_closed_category)
                        return
                    
                    await inter.send(content="На эту кнопку может нажимать только автор тикета.", ephemeral=True)

                if inter.component.custom_id == "assessment_5":
                    ticket_channel = inter.guild.get_channel(inter.channel.id)

                    author_ticket_db = cursor.execute(f"""SELECT author_id FROM tickets WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    author_ticket = inter.guild.get_member(author_ticket_db)

                    support_ticket_db = cursor.execute(f"""SELECT support_id FROM tickets WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    support_ticket = inter.guild.get_member(support_ticket_db)

                    if author_ticket == inter.author:
                        embed_logs = disnake.Embed(
                            title="Оценка обращения",
                            description=f"{author_ticket.mention} оценил работу {support_ticket.mention} на **5** <:branding:1004492631117664287>.",
                            color=0x2f3136)

                        await inter.response.defer()
                        await inter.message.edit(content=f"{author_ticket.mention}, вы оценили работу {support_ticket.mention} на **5** <:branding:1004492631117664287>.", embed=None, view=None)
                        await channel_logs.send(content=support_ticket.mention, embed=embed_logs)

                        await ticket_channel.set_permissions(author_ticket, overwrite=None)
                        await ticket_channel.set_permissions(support_ticket, overwrite=None)
                        await ticket_channel.set_permissions(support_administration_role, read_messages=True, send_messages=False)
                        
                        cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                        db.commit()

                        await ticket_channel.edit(category=ticket_closed_category)
                        return
                    
                    await inter.send(content="На эту кнопку может нажимать только автор тикета.", ephemeral=True)
                
                if inter.component.custom_id == "clear_ticket_closed_button":
                    delc = 0

                    if perms_owner is not None or perms_dev is not None:
                        await inter.send(content="Процесс удаления пошёл...", ephemeral=True)

                        for channel in inter.guild.text_channels:
                            if channel.category == clear_ticket_closed_category:
                                await channel.delete()
                                delc = delc + 1

                        await inter.send(f"Удалено **{delc}** закрытых обращений.", ephemeral=True)

                if inter.component.custom_id == "clear_complaints_staff_closed_button":
                    delc = 0

                    if perms_owner is not None or perms_dev is not None:
                        await inter.send(content="Процесс удаления пошёл...", ephemeral=True)

                        for channel in inter.guild.text_channels:
                            if channel.category == clear_complaints_staff_closed_category:
                                await channel.delete()
                                delc = delc + 1

                        await inter.send(f"Удалено **{delc}** закрытых обращений.", ephemeral=True)

                if inter.component.custom_id == "clear_complaints_members_closed_button":
                    delc = 0

                    if perms_owner is not None or perms_dev is not None:
                        await inter.send(content="Процесс удаления пошёл...", ephemeral=True)

                        for channel in inter.guild.text_channels:
                            if channel.category == clear_complaints_members_closed_category:
                                await channel.delete()
                                delc = delc + 1

                        await inter.send(f"Удалено **{delc}** закрытых обращений.", ephemeral=True)


def setup(bot):
    bot.add_cog(Tickets(bot))