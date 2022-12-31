import disnake
import sqlite3
from disnake.ext import commands


with sqlite3.connect("database (Miky).db") as db:
    cursor = db.cursor()
    
    for guild_natame, guild_mossymineskills in cursor.execute("SELECT * FROM bot_guilds"):
        natame_guild = guild_natame
        mossymineskills_guild = guild_mossymineskills

    module_say_messages = [module_say_messages[0] for module_say_messages in cursor.execute("SELECT module_say_messages FROM bot_modules")]
    module_reaction_commands = [module_reaction_commands[0] for module_reaction_commands in cursor.execute("SELECT module_reaction_commands FROM bot_modules")]

    module_clear = [module_clear[0] for module_clear in cursor.execute("SELECT module_clear FROM bot_modules")]
    module_mutes = [module_mutes[0] for module_mutes in cursor.execute("SELECT module_mutes FROM bot_modules")]
    module_bans = [module_bans[0] for module_bans in cursor.execute("SELECT module_bans FROM bot_modules")]
    module_permbans = [module_permbans[0] for module_permbans in cursor.execute("SELECT module_permbans FROM bot_modules")]
    module_staff_list = [module_staff_list[0] for module_staff_list in cursor.execute("SELECT module_staff_list FROM bot_modules")]
    module_sos = [module_sos[0] for module_sos in cursor.execute("SELECT module_sos FROM bot_modules")]

    module_ping = [module_ping[0] for module_ping in cursor.execute("SELECT module_ping FROM bot_modules")]

    module_profile = [module_profile[0] for module_profile in cursor.execute("SELECT module_profile FROM bot_modules")]
    module_user_info = [module_user_info[0] for module_user_info in cursor.execute("SELECT module_user_info FROM bot_modules")]
    module_server_info = [module_server_info[0] for module_server_info in cursor.execute("SELECT module_server_info FROM bot_modules")]
    module_inrole = [module_inrole[0] for module_inrole in cursor.execute("SELECT module_inrole FROM bot_modules")]

    module_avatar = [module_avatar[0] for module_avatar in cursor.execute("SELECT module_avatar FROM bot_modules")]
    module_banner = [module_banner[0] for module_banner in cursor.execute("SELECT module_banner FROM bot_modules")]
    

    class InteractionDatabase(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_message(self, message: disnake.Message):
            if message.guild:
                aboutme_entry = cursor.execute(f"""SELECT user_id FROM aboutme WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}""").fetchone()
                badges_entry = cursor.execute(f"""SELECT user_id FROM badges WHERE user_id = {message.author.id}""").fetchone()
                economy_entry = cursor.execute(f"""SELECT user_id FROM economy WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}""").fetchone()
                levels_entry = cursor.execute(f"""SELECT user_id FROM levels WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}""").fetchone()
                perms_entry = cursor.execute(f"""SELECT user_id FROM perms WHERE user_id = {message.author.id}""").fetchone()

                if aboutme_entry is None:
                    cursor.execute(f"""INSERT INTO aboutme VALUES ({message.guild.id}, {message.author.id}, 'Пользователь ничего о себе не рассказал.')""")
                    db.commit()

                if badges_entry is None:
                    cursor.execute(f"""INSERT INTO badges VALUES ({message.author.id}, 'None', 'Нет значков.')""")
                    db.commit()

                if economy_entry is None:
                    cursor.execute(f"""INSERT INTO economy VALUES ({message.guild.id}, {message.author.id}, 0, 0, 0)""")
                    db.commit()

                if levels_entry is None:
                    cursor.execute(f"""INSERT INTO levels VALUES ({message.guild.id}, {message.author.id}, 0, 0)""")
                    db.commit()

                if perms_entry is None:
                    cursor.execute(f"""INSERT INTO perms VALUES ({message.author.id}, 'USER')""")
                    db.commit()

        @commands.Cog.listener()
        async def on_member_join(self, member: disnake.Member):
            aboutme_entry = cursor.execute(f"""SELECT user_id FROM aboutme WHERE user_id = {member.id} AND guild_id = {member.guild.id}""").fetchone()
            badges_entry = cursor.execute(f"""SELECT user_id FROM badges WHERE user_id = {member.id}""").fetchone()
            economy_entry = cursor.execute(f"""SELECT user_id FROM economy WHERE user_id = {member.id} AND guild_id = {member.guild.id}""").fetchone()
            levels_entry = cursor.execute(f"""SELECT user_id FROM levels WHERE user_id = {member.id} AND guild_id = {member.guild.id}""").fetchone()
            perms_entry = cursor.execute(f"""SELECT user_id FROM perms WHERE user_id = {member.id}""").fetchone()

            if aboutme_entry is None:
                cursor.execute(f"""INSERT INTO aboutme VALUES ({member.guild.id}, {member.id}, 'Пользователь ничего о себе не рассказал.')""")
                db.commit()

            if badges_entry is None:
                cursor.execute(f"""INSERT INTO badges VALUES ({member.id}, 'None', 'Нет значков.')""")
                db.commit()

            if economy_entry is None:
                cursor.execute(f"""INSERT INTO economy VALUES ({member.guild.id}, {member.id}, 0, 0, 0)""")
                db.commit()

            if levels_entry is None:
                cursor.execute(f"""INSERT INTO levels VALUES ({member.guild.id}, {member.id}, 0, 0)""")
                db.commit()

            if perms_entry is None:
                cursor.execute(f"""INSERT INTO perms VALUES ({member.id}, 'USER')""")
                db.commit()

        @commands.slash_command(guild_ids=[])
        async def database(self, inter):
            pass

        @database.sub_command(name="add",
                        description="Добавить пользователя в БД",
                        options=[disnake.Option(name="user",
                                                description="Укажите пользователя",
                                                type=disnake.OptionType.user,
                                                required=True)])
        async def adddatabase(self, inter, user: disnake.User):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {inter.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {inter.author.id} AND lvl_rights = 'DEV'""").fetchone()

            aboutme_entry = cursor.execute(f"""SELECT user_id FROM aboutme WHERE user_id = {user.id} AND guild_id = {inter.guild.id}""").fetchone()
            badges_entry = cursor.execute(f"""SELECT user_id FROM badges WHERE user_id = {user.id}""").fetchone()
            economy_entry = cursor.execute(f"""SELECT user_id FROM economy WHERE user_id = {user.id} AND guild_id = {inter.guild.id}""").fetchone()
            levels_entry = cursor.execute(f"""SELECT user_id FROM levels WHERE user_id = {user.id} AND guild_id = {inter.guild.id}""").fetchone()
            perms_entry = cursor.execute(f"""SELECT user_id FROM perms WHERE user_id = {user.id}""").fetchone()

            if perms_owner is not None or perms_dev is not None:
                if aboutme_entry is None:
                    cursor.execute(f"""INSERT INTO aboutme VALUES ({inter.guild.id}, {user.id}, 'Пользователь ничего о себе не рассказал.')""")
                    db.commit()

                    await inter.send(content=f"Пользователь {user.mention} добавлен в таблицу **aboutme**.", ephemeral=True)
                else:
                    await inter.send(content=f"Пользователь {user.mention} был зарегистрирован в таблице **aboutme**.", ephemeral=True)

                if badges_entry is None:
                    cursor.execute(f"""INSERT INTO badges VALUES ({user.id}, 'None', 'Нет значков.')""")
                    db.commit()

                    await inter.send(content=f"Пользователь {user.mention} добавлен в таблицу **badges**.", ephemeral=True)
                else:
                    await inter.send(content=f"Пользователь {user.mention} был зарегистрирован в таблице **badges**.", ephemeral=True)

                if economy_entry is None:
                    cursor.execute(f"""INSERT INTO economy VALUES ({inter.guild.id}, {user.id}, 0, 0, 0)""")
                    db.commit()

                    await inter.send(content=f"Пользователь {user.mention} добавлен в таблицу **economy**.", ephemeral=True)
                else:
                    await inter.send(content=f"Пользователь {user.mention} был зарегистрирован в таблице **economy**.", ephemeral=True)

                if levels_entry is None:
                    cursor.execute(f"""INSERT INTO levels VALUES ({inter.guild.id}, {user.id}, 0, 0)""")
                    db.commit()

                    await inter.send(content=f"Пользователь {user.mention} добавлен в таблицу **levels**.", ephemeral=True)
                else:
                    await inter.send(content=f"Пользователь {user.mention} был зарегистрирован в таблице **levels**.", ephemeral=True)

                if perms_entry is None:
                    cursor.execute(f"""INSERT INTO perms VALUES ({user.id}, 'USER')""")
                    db.commit()

                    await inter.send(content=f"Пользователь {user.mention} добавлен в таблицу **perms**.", ephemeral=True)
                else:
                    await inter.send(content=f"Пользователь {user.mention} был зарегистрирован в таблице **perms**.", ephemeral=True)
            else:
                await inter.send(content="Права на использование есть только у разработчика бота.", ephemeral=True)

        @database.sub_command(name="remove",
                        description="Удалить пользователя из БД",
                        options=[disnake.Option(name="user",
                                                description="Укажите пользователя",
                                                type=disnake.OptionType.user,
                                                required=True)])
        async def removedatabase(self, inter, user: disnake.User):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {inter.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {inter.author.id} AND lvl_rights = 'DEV'""").fetchone()

            owner_entry = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {user.id} AND lvl_rights = 'OWN'""").fetchone()
            aboutme_entry = cursor.execute(f"""SELECT user_id FROM aboutme WHERE user_id = {user.id} AND guild_id = {inter.guild.id}""").fetchone()
            badges_entry = cursor.execute(f"""SELECT user_id FROM badges WHERE user_id = {user.id}""").fetchone()
            economy_entry = cursor.execute(f"""SELECT user_id FROM economy WHERE user_id = {user.id} AND guild_id = {inter.guild.id}""").fetchone()
            levels_entry = cursor.execute(f"""SELECT user_id FROM levels WHERE user_id = {user.id} AND guild_id = {inter.guild.id}""").fetchone()
            perms_entry = cursor.execute(f"""SELECT user_id FROM perms WHERE user_id = {user.id}""").fetchone()

            if perms_owner is not None or perms_dev is not None:
                if owner_entry is not None:
                    await inter.send(content="Нельзя взаимодействовать с пользователями, уровень прав которых равен **OWN**.", ephemeral=True)
                    return

                if aboutme_entry is not None:
                    cursor.execute(f"""DELETE FROM aboutme WHERE user_id = {user.id}""")
                    db.commit()

                    await inter.send(content=f"Пользователь {user.mention} удалён из таблицы **aboutme**.", ephemeral=True)
                else:
                    await inter.send(content=f"Пользователь {user.mention} уже был удалён в таблице **aboutme**.", ephemeral=True)

                if badges_entry is not None:
                    cursor.execute(f"""DELETE FROM badges WHERE user_id = {user.id}""")
                    db.commit()

                    await inter.send(content=f"Пользователь {user.mention} удалён из таблицы **badges**.", ephemeral=True)
                else:
                    await inter.send(content=f"Пользователь {user.mention} уже был удалён в таблице **badges**.", ephemeral=True)

                if economy_entry is not None:
                    cursor.execute(f"""DELETE FROM economy WHERE user_id = {user.id}""")
                    db.commit()

                    await inter.send(content=f"Пользователь {user.mention} удалён из таблицы **economy**.", ephemeral=True)
                else:
                    await inter.send(content=f"Пользователь {user.mention} уже был удалён в таблице **economy**.", ephemeral=True)

                if levels_entry is not None:
                    cursor.execute(f"""DELETE FROM levels WHERE user_id = {user.id}""")
                    db.commit()

                    await inter.send(content=f"Пользователь {user.mention} удалён из таблицы **levels**.", ephemeral=True)
                else:
                    await inter.send(content=f"Пользователь {user.mention} уже был удалён в таблице **levels**.", ephemeral=True)

                if perms_entry is not None:
                    cursor.execute(f"""DELETE FROM perms WHERE user_id = {user.id}""")
                    db.commit()

                    await inter.send(content=f"Пользователь {user.mention} удалён из таблицы **perms**.", ephemeral=True)
                else:
                    await inter.send(content=f"Пользователь {user.mention} уже был удалён в таблице **perms**.", ephemeral=True)
            else:
                await inter.send(content="Права на использование есть только у разработчика бота, уровень прав которого равен **OWN**.", ephemeral=True)

        @database.sub_command(name="perms",
                        description="Изменить права пользователя",
                        options=[disnake.Option(name="user",
                                                description="Укажите пользователя",
                                                type=disnake.OptionType.user,
                                                required=True),
                                    disnake.Option(name="perms",
                                                description="Установите права пользователя",
                                                type=disnake.OptionType.string,
                                                required=True)])
        async def permsdatabase(self, inter, user: disnake.User, perms: str):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {inter.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {inter.author.id} AND lvl_rights = 'DEV'""").fetchone()
            perms_entry = cursor.execute(f"""SELECT user_id FROM perms WHERE user_id = {user.id}""").fetchone()

            if perms_owner is not None or perms_dev is not None:
                if perms == "OWN":
                    await inter.send(content="Нельзя выставлять значение уровня прав на **OWN**.", ephemeral=True)
                    return

                if perms_entry is None:
                    cursor.execute(f"""INSERT INTO perms VALUES ({user.id}, 'USER')""")
                    db.commit()

                try:
                    cursor.execute(f"""UPDATE perms SET lvl_rights = '{perms}' WHERE user_id = {user.id} AND lvl_rights != 'OWN'""")
                    db.commit()
                except BaseException:
                    await inter.send(content="Нельзя взаимодействовать с пользователями, уровень прав которых равен **OWN**.", ephemeral=True)
                    return

                await inter.send(content=f"Изменено значение **lvl_rights** на {perms} у пользователя {user.mention} в базе данных.", ephemeral=True)
                return

            await inter.send(content="Права на использование есть только у разработчика бота.", ephemeral=True)

        @database.sub_command(name="badges",
                        description="Изменить значки пользователя",
                        options=[disnake.Option(name="user",
                                                description="Укажите пользователя",
                                                type=disnake.OptionType.user,
                                                required=True),
                                    disnake.Option(name="badge",
                                                description="Установите значки пользователя",
                                                type=disnake.OptionType.string,
                                                required=True)])
        async def badgesdatabase(self, inter, user: disnake.User, badge):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {inter.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {inter.author.id} AND lvl_rights = 'DEV'""").fetchone()
            perms_adm = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {inter.author.id} AND lvl_rights = 'ADM'""").fetchone()
            
            badges_entry = cursor.execute(f"""SELECT user_id FROM badges WHERE user_id = {user.id}""").fetchone()

            if perms_owner is not None or perms_dev is not None or perms_adm is not None:
                if badges_entry is None:
                    cursor.execute(f"""INSERT INTO badges VALUES ({user.id}, 'None', 'Нет значков.')""")
                    db.commit()

                cursor.execute(f"""UPDATE badges SET badge = '{badge}' WHERE user_id = {user.id}""")
                db.commit()

                await inter.send(content=f"Изменено значение **badge** на {badge} у пользователя {user.mention} в базе данных.", ephemeral=True)
                return

            await inter.send(content="Права на использование есть только у разработчика бота.", ephemeral=True)

        @database.sub_command(name="verify-add",
                        description="Верификацировать пользователя",
                        options=[disnake.Option(name="user",
                                                description="Укажите пользователя",
                                                type=disnake.OptionType.user,
                                                required=True)])
        async def addverifydatabase(self, inter, user: disnake.User):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {inter.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {inter.author.id} AND lvl_rights = 'DEV'""").fetchone()
            perms_adm = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {inter.author.id} AND lvl_rights = 'ADM'""").fetchone()
            
            badges_entry = cursor.execute(f"""SELECT user_id FROM badges WHERE user_id = {user.id}""").fetchone()

            if perms_owner is not None or perms_dev is not None or perms_adm is not None:
                if badges_entry is None:
                    cursor.execute(f"""INSERT INTO badges VALUES ({user.id}, 'None', 'Нет значков.')""")
                    db.commit()

                cursor.execute(f"""UPDATE badges SET verify_status = 'VERIFY' WHERE user_id = {user.id}""")
                db.commit()

                await inter.send(content=f"Изменено значение **verify_status** на **VERIFY** у пользователя {user.mention} в базе данных.", ephemeral=True)
                return

            await inter.send(content="Права на использование есть только у разработчика бота.", ephemeral=True)

        @database.sub_command(name="verify-remove",
                        description="Убрать верификацию у пользователя",
                        options=[disnake.Option(name="user",
                                                description="Укажите пользователя",
                                                type=disnake.OptionType.user,
                                                required=True)])
        async def removeverifydatabase(self, inter, user: disnake.User):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {inter.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {inter.author.id} AND lvl_rights = 'DEV'""").fetchone()
            perms_adm = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {inter.author.id} AND lvl_rights = 'ADM'""").fetchone()
            
            badges_entry = cursor.execute(f"""SELECT user_id FROM badges WHERE user_id = {user.id}""").fetchone()

            if perms_owner is not None or perms_dev is not None or perms_adm is not None:
                if badges_entry is None:
                    cursor.execute(f"""INSERT INTO badges VALUES ({user.id}, 'None', 'Нет значков.')""")
                    db.commit()

                cursor.execute(f"""UPDATE badges SET verify_status = 'None' WHERE user_id = {user.id}""")
                db.commit()

                await inter.send(content=f"Изменено значение **verify_status** на **None** у пользователя {user.mention} в базе данных.", ephemeral=True)
                return

            await inter.send(content="Права на использование есть только у разработчика бота.", ephemeral=True)


def setup(bot):
    bot.add_cog(InteractionDatabase(bot))