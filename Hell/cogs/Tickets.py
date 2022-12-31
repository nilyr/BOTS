import disnake
import sqlite3
from disnake import ButtonStyle
from disnake.ext import commands
from disnake.ui import View, Button, Select

with sqlite3.connect("database (Hell).db") as db:
    cursor = db.cursor()

    class Tickets(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.command(name="tickets")
        async def ticketsinformation(self, ctx):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            guild_tc = self.bot.get_guild(614081676116754465)

            if perms_owner is not None or perms_dev is not None:
                if ctx.guild == guild_tc:
                    channel_tickets = self.bot.get_channel(1025850211354021919)

                    tickets_menu = View()
                    tickets_menu.add_item(Select(placeholder="Выберите по какой из тем хотите создать тикет.", custom_id="tickets_menu",
                    options = [disnake.SelectOption(emoji="<a:No_Check:877264845366517770>", label="Не выбрано", value="default_option", default=True),
                            disnake.SelectOption(emoji="<a:question_red:916001629122216036>", label="Обращения к персоналу", value="tickets")]))

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

        @commands.Cog.listener()
        async def on_dropdown(self, inter):
            guild_tc = self.bot.get_guild(614081676116754465)

            if inter.guild == guild_tc:
                waiting_category = disnake.utils.get(inter.guild.categories, id=1025844970936074302)

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

                        if ticket_created_waiting is not None or ticket_created_processing is not None:
                            await inter.send("Вы уже создали обращение.", ephemeral=True)
                            return

                        await inter.send(content=f"<a:waiting:1011657420860293180> Обращение создаётся...", ephemeral=True)
                        msg = await inter.original_message()

                        cursor.execute("""UPDATE tickets_numbers SET numbers = numbers + 1""")
                        db.commit()

                        tickets_numbering = cursor.execute("""SELECT numbers FROM tickets_numbers""").fetchone()[0]
                        ticket_channel = await waiting_category.create_text_channel(f"ticket-{tickets_numbering}")

                        embed_msg = await ticket_channel.send(content="Создание обращения...")
                        
                        cursor.execute(f"""INSERT INTO tickets VALUES ({inter.guild.id}, 'WAITING', {inter.author.id}, 'None', {ticket_channel.id}, {embed_msg.id})""")
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

                        await embed_msg.edit(content=f"<@&825112987446673488>\nОбращение от {author_ticket.mention} | `{author_ticket.id}`", embed=embed, view=support_button)
                        await ticket_channel.set_permissions(author_ticket, read_messages=True, send_messages=True)
                        await msg.edit(content=f"Обращение создано. Для его заполнения перейдите в канал {ticket_channel.mention}.")

        @commands.Cog.listener()
        async def on_button_click(self, inter):       
            guild_tc = self.bot.get_guild(614081676116754465)

            if inter.guild == guild_tc:
                channel_logs = self.bot.get_channel(1025836891620261928)

                processing_category = disnake.utils.get(inter.guild.categories, id=1025845037986222150)
                closed_category = disnake.utils.get(inter.guild.categories, id=1025845078574514206)

                security_role = disnake.utils.get(inter.guild.roles, id=813365784487133204)
                discord_team_role = disnake.utils.get(inter.guild.roles, id=825112987446673488)

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

                            await ticket_channel.edit(category=closed_category)
                            return
                    except BaseException:
                        await inter.response.defer()
                        await inter.message.edit(view=None)
                        await inter.channel.send(content=f"Обращение закрыто, участник вышел.")
                        
                        cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                        db.commit()

                        await ticket_channel.edit(category=closed_category)
                        return

                    cursor.execute(f"""UPDATE tickets SET support_id = {inter.author.id} WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                    cursor.execute(f"""UPDATE tickets SET status = 'PROCESSING' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                    db.commit()

                    support_ticket_db = cursor.execute(f"""SELECT support_id FROM tickets WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""").fetchone()[0]
                    support_ticket = inter.guild.get_member(support_ticket_db)

                    embed = disnake.Embed(
                        description="Напишите свой вопрос и ожидайте ответ от персонала.",
                        color=0x2f3136)
                    embed.add_field(name="Создал обращение", value=author_ticket.mention)
                    embed.add_field(name="Обрабатывает обращение", value=support_ticket.mention)

                    await inter.response.defer()

                    await inter.message.edit(content=f"<@&825112987446673488>\nОбращение от {author_ticket.mention} | `{author_ticket.id}`", embed=embed, view=support_button)
                    await ticket_channel.edit(category=processing_category)

                    await ticket_channel.set_permissions(discord_team_role, overwrite=None)
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
                                
                                cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                                db.commit()

                                await ticket_channel.edit(category=closed_category)
                                return
                        except BaseException:
                            await inter.response.defer()
                            await inter.message.edit(view=None)
                            await inter.channel.send(content=f"{support_ticket.mention}\nОбращение закрыто, участник вышел.")

                            await ticket_channel.set_permissions(support_ticket, overwrite=None)
                            
                            cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                            db.commit()

                            await ticket_channel.edit(category=closed_category)
                            return

                        embed = disnake.Embed(
                            title="Оценка обращения",
                            description="Пожалуйста, оцените работу человека, обрабатывающего ваше обращение.",
                            color=0x2f3136)

                        await inter.response.defer()
                        await inter.message.edit(view=None)
                        await ticket_channel.edit(category=closed_category)
                        await ticket_channel.set_permissions(author_ticket, read_messages=True, send_messages=False)
                        await ticket_channel.set_permissions(support_ticket, read_messages=True, send_messages=False)
                        await ticket_channel.send(content=author_ticket.mention, embed=embed, view=assessment_button)
                        return
                    
                    await inter.send(content="На эту кнопку может нажимать только тот человек, который обрабатывает данное обращение.", ephemeral=True)
                
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
                                
                                cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                                db.commit()

                                await ticket_channel.edit(category=closed_category)
                                return
                        except BaseException:
                            await inter.response.defer()
                            await inter.message.edit(view=None)
                            await inter.channel.send(content=f"{support_ticket.mention}\nОбращение закрыто, участник вышел.")

                            await ticket_channel.set_permissions(support_ticket, overwrite=None)
                            
                            cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                            db.commit()

                            await ticket_channel.edit(category=closed_category)
                            return

                        await inter.response.defer()
                        await inter.message.edit(content=f"{support_ticket.mention} закрыл обращение досрочно.", embed=None, view=None)

                        await ticket_channel.set_permissions(author_ticket, overwrite=None)
                        await ticket_channel.set_permissions(support_ticket, overwrite=None)
                        await ticket_channel.set_permissions(security_role, read_messages=True)
                        
                        cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                        db.commit()

                        await ticket_channel.edit(category=closed_category)
                        return
                    
                    await inter.send(content="На эту кнопку может нажимать только тот человек, который обрабатывает данное обращение.", ephemeral=True)

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
                        await ticket_channel.set_permissions(security_role, read_messages=True)
                        
                        cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                        db.commit()

                        await ticket_channel.edit(category=closed_category)
                        return
                    
                    await inter.send(content="На эту кнопку может нажимать только автор обращения.", ephemeral=True)

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
                        await ticket_channel.set_permissions(security_role, read_messages=True)
                        
                        cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                        db.commit()

                        await ticket_channel.edit(category=closed_category)
                        return
                    
                    await inter.send(content="На эту кнопку может нажимать только автор обращения.", ephemeral=True)

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
                        await ticket_channel.set_permissions(security_role, read_messages=True)
                        
                        cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                        db.commit()

                        await ticket_channel.edit(category=closed_category)
                        return
                    
                    await inter.send(content="На эту кнопку может нажимать только автор обращения.", ephemeral=True)

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
                        await ticket_channel.set_permissions(security_role, read_messages=True)
                        
                        cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                        db.commit()

                        await ticket_channel.edit(category=closed_category)
                        return
                    
                    await inter.send(content="На эту кнопку может нажимать только автор обращения.", ephemeral=True)

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
                        await ticket_channel.set_permissions(security_role, read_messages=True)
                        
                        cursor.execute(f"""UPDATE tickets SET status = 'CLOSED' WHERE channel_id == {ticket_channel.id} AND guild_id == {inter.guild.id}""")
                        db.commit()

                        await ticket_channel.edit(category=closed_category)
                        return
                    
                    await inter.send(content="На эту кнопку может нажимать только автор обращения.", ephemeral=True)

        @commands.command(name="tickets-clear")
        async def ticketschannelclear(self, ctx):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()
            
            category_closed = disnake.utils.get(ctx.guild.categories, id=1025845078574514206)

            delc = 0
            await ctx.message.delete()

            if perms_owner is not None or perms_dev is not None:
                for channel in ctx.guild.text_channels:
                    if channel.category == category_closed:
                        await channel.delete()
                        delc = delc + 1

                await ctx.send(f"Удалено **{delc}** закрытых обращений.", delete_after=5)

def setup(bot):
    bot.add_cog(Tickets(bot))