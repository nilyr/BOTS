import disnake
import sqlite3
from disnake.ext import commands
from datetime import datetime, timezone, timedelta
from cogs.InteractionDatabase import module_profile, module_user_info, module_server_info, module_inrole

with sqlite3.connect("database (Miky).db") as db:
    cursor = db.cursor()
    
    class InformationCommands(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.slash_command(name="profile",
                                description="Профиль пользователя",
                                guild_ids=module_profile,
                                options=[disnake.Option(name="member",
                                                        description="Укажите любого пользователя",
                                                        type=disnake.OptionType.user)])
        async def profile(self, ctx, member: disnake.User = None):
            member = ctx.author if not member else member

            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {member.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {member.id} AND lvl_rights = 'DEV'""").fetchone()
            perms_adm = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {member.id} AND lvl_rights = 'ADM'""").fetchone()

            aboutme_entry = cursor.execute(f"""SELECT user_id FROM aboutme WHERE user_id = {member.id} AND guild_id = {ctx.guild.id}""").fetchone()
            badges_entry = cursor.execute(f"""SELECT user_id FROM badges WHERE user_id = {member.id}""").fetchone()

            if aboutme_entry is None:
                cursor.execute(f"""INSERT INTO aboutme VALUES ({ctx.guild.id}, {member.id}, 'Пользователь ничего о себе не рассказал.')""")
                db.commit()

            if badges_entry is None:
                cursor.execute(f"""INSERT INTO badges VALUES ({member.id}, 'None', 'Нет значков.')""")
                db.commit()

            badge = cursor.execute(f"""SELECT badge FROM badges WHERE user_id = {member.id}""").fetchone()[0]
            verify_status = cursor.execute(f"""SELECT verify_status FROM badges WHERE user_id = {member.id}""").fetchone()[0]
            aboutme = cursor.execute(f"""SELECT text FROM aboutme WHERE user_id = {member.id} AND guild_id = {ctx.guild.id}""").fetchone()[0]
            
            if verify_status == "VERIFY":
                embed = disnake.Embed(
                    color=0x2f3136,
                    title=f"Профиль пользователя {member} <a:verify:1014164258298265652>",
                    description=f"{badge}\n\n"
                    f"**О себе:** {aboutme}")
            else:
                embed = disnake.Embed(
                    color=0x2f3136,
                    title=f"Профиль пользователя {member}",
                    description=f"{badge}\n\n"
                    f"**О себе:** {aboutme}")

            if member == ctx.guild.me:
                embed.set_author(name=self.bot.user.name, icon_url="https://cdn.discordapp.com/emojis/1010585382527709224.png")
            if perms_owner is not None:
                embed.set_author(name="Создатель бота", icon_url="https://cdn.discordapp.com/emojis/1014175967499014217.png")
            if perms_dev is not None:
                embed.set_author(name="Разработчик бота", icon_url="https://cdn.discordapp.com/emojis/1014175969180930078.png")
            if perms_adm is not None:
                embed.set_author(name="Администратор бота", icon_url="https://cdn.discordapp.com/emojis/1014176927768125530.png")

            embed.set_thumbnail(url=member.display_avatar)
            embed.set_footer(text="Установить информацию о себе можно командой /about-me")

            await ctx.send(embed=embed)

        @commands.slash_command(name="about-me",
                                description="Указать информацию о себе",
                                guild_ids=module_profile,
                                options=[disnake.Option(name="info",
                                                        description="Напишите информацию о себе",
                                                        type=disnake.OptionType.string,
                                                        required=True),
                                        disnake.Option(name="servers",
                                                        description="Изменить информацию о себе на всех серверах?",
                                                        type=disnake.OptionType.string)])
        async def aboutme(self, ctx, info: str, servers=None):
            aboutme_entry = cursor.execute(f"""SELECT user_id FROM aboutme WHERE user_id = {ctx.author.id} AND guild_id = {ctx.guild.id}""").fetchone()

            embed_all = disnake.Embed(
                color=0x2f3136,
                description=f"**Установлено:** {info}")
            embed_all.set_author(name="Информация о себе успешно обновлена")
            embed_all.set_footer(text="На всех серверах")

            embed_local = disnake.Embed(
                color=0x2f3136,
                description=f"**Установлено:** {info}")
            embed_local.set_author(name="Информация о себе успешно обновлена")
            embed_local.set_footer(text="На этом сервере")

            if aboutme_entry is None:
                cursor.execute(f"""INSERT INTO aboutme VALUES ({ctx.guild.id}, {ctx.author.id}, 'Пользователь ничего о себе не рассказал.')""")
                db.commit()

            if servers is None:
                cursor.execute(f"""UPDATE aboutme SET text = '{info}' WHERE user_id = {ctx.author.id} AND guild_id = {ctx.guild.id}""")
                db.commit()

                await ctx.send(embed=embed_local, ephemeral=True)
                return

            cursor.execute(f"""UPDATE aboutme SET text = '{info}' WHERE user_id = {ctx.author.id}""")
            db.commit()

            await ctx.send(embed=embed_all, ephemeral=True)

        @commands.slash_command(name="user",
                                description="Узнайте информацию о себе или о другом пользователе",
                                guild_ids=module_user_info,
                                options=[disnake.Option(name="member",
                                                        description="Укажите любого пользователя",
                                                        type=disnake.OptionType.user)])
        async def userinfo(self, ctx, member: disnake.User = None):
            member = ctx.author if not member else member

            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {member.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {member.id} AND lvl_rights = 'DEV'""").fetchone()
            perms_adm = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {member.id} AND lvl_rights = 'ADM'""").fetchone()

            discordtimejoin_ = member.created_at.timestamp()
            discordtimejoin = f'{round(discordtimejoin_, 0)}'.replace('.0', '')

            servertimejoin_ = member.joined_at.timestamp()
            servertimejoin = f'{round(servertimejoin_, 0)}'.replace('.0', '')

            Roles = [role for role in member.roles]

            if member.bot:
                embed = disnake.Embed(
                    color=0x2f3136,
                    title=f"Информация о **Боте**",
                    description=f"**Аккаунт бота {member.mention}**")
            else:
                embed = disnake.Embed(
                    color=0x2f3136,
                    title=f"Информация о пользователе {member}")

            embed.set_thumbnail(url=member.display_avatar)
            embed.add_field(name="ID пользователя", value=member.id, inline=False)
            embed.add_field(name="Ник", value=member, inline=False)
            embed.add_field(
                name="Наивысшая роль",
                value="**" +
                member.top_role.mention +
                "**")
            embed.add_field(name="Все роли", value="**" +
                            " ".join([role.mention for role in Roles[1:]]) +
                            "**", inline=False)
            embed.add_field(
                name="Аккаунт создан",
                value=f'<t:{discordtimejoin}:D> (<t:{discordtimejoin}:R>)',
                inline=False)
            embed.add_field(
                name="Присоединился к серверу",
                value=f'<t:{servertimejoin}:D> (<t:{servertimejoin}:R>)',
                inline=False)

            if member == ctx.guild.me:
                embed.set_author(name=self.bot.user.name, icon_url="https://cdn.discordapp.com/emojis/1010585382527709224.png")
                embed.set_image(
                    url="https://cdn.discordapp.com/attachments/838848278858039336/993440699762618398/anime-pink.gif")

            if perms_owner is not None:
                embed.set_author(name="Создатель бота", icon_url="https://cdn.discordapp.com/emojis/1014175967499014217.png")
                embed.set_image(
                    url="https://cdn.discordapp.com/attachments/838848278858039336/993439008573108244/admin_opinion.gif")

            if perms_dev is not None:
                embed.set_author(name="Разработчик бота", icon_url="https://cdn.discordapp.com/emojis/1014175969180930078.png")
                embed.set_image(
                    url="https://cdn.discordapp.com/attachments/838848278858039336/993439008573108244/admin_opinion.gif")

            if perms_adm is not None:
                embed.set_author(name="Администратор бота", icon_url="https://cdn.discordapp.com/emojis/1014176927768125530.png")
                embed.set_image(
                    url="https://cdn.discordapp.com/attachments/838848278858039336/993439008573108244/admin_opinion.gif")

            await ctx.send(embed=embed)

        @commands.user_command(name="User", guild_ids=module_user_info)
        async def userinfouser(self, ctx, member: disnake.User,):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {member.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {member.id} AND lvl_rights = 'DEV'""").fetchone()
            perms_adm = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {member.id} AND lvl_rights = 'ADM'""").fetchone()

            discordtimejoin_ = member.created_at.timestamp()
            discordtimejoin = f'{round(discordtimejoin_, 0)}'.replace('.0', '')

            servertimejoin_ = member.joined_at.timestamp()
            servertimejoin = f'{round(servertimejoin_, 0)}'.replace('.0', '')

            Roles = [role for role in member.roles]

            if member.bot:
                embed = disnake.Embed(
                    color=0x2f3136,
                    title=f"Информация о **Боте**",
                    description=f"**Аккаунт бота {member.mention}**")
            else:
                embed = disnake.Embed(
                    color=0x2f3136,
                    title=f"Информация о пользователе {member}")

            embed.set_thumbnail(url=member.display_avatar)
            embed.add_field(name="ID пользователя", value=member.id, inline=False)
            embed.add_field(name="Ник", value=member, inline=False)
            embed.add_field(
                name="Наивысшая роль",
                value="**" +
                member.top_role.mention +
                "**")
            embed.add_field(name="Все роли", value="**" +
                            " ".join([role.mention for role in Roles[1:]]) +
                            "**", inline=False)
            embed.add_field(
                name="Аккаунт создан",
                value=f'<t:{discordtimejoin}:D> (<t:{discordtimejoin}:R>)',
                inline=False)
            embed.add_field(
                name="Присоединился к серверу",
                value=f'<t:{servertimejoin}:D> (<t:{servertimejoin}:R>)',
                inline=False)

            if member == ctx.guild.me:
                embed.set_author(name=self.bot.user.name, icon_url="https://cdn.discordapp.com/emojis/1010585382527709224.png")
                embed.set_image(
                    url="https://cdn.discordapp.com/attachments/838848278858039336/993440699762618398/anime-pink.gif")

            if perms_owner is not None:
                embed.set_author(name="Создатель бота", icon_url="https://cdn.discordapp.com/emojis/1014175967499014217.png")
                embed.set_image(
                    url="https://cdn.discordapp.com/attachments/838848278858039336/993439008573108244/admin_opinion.gif")

            if perms_dev is not None:
                embed.set_author(name="Разработчик бота", icon_url="https://cdn.discordapp.com/emojis/1014175969180930078.png")
                embed.set_image(
                    url="https://cdn.discordapp.com/attachments/838848278858039336/993439008573108244/admin_opinion.gif")

            if perms_adm is not None:
                embed.set_author(name="Администратор бота", icon_url="https://cdn.discordapp.com/emojis/1014176927768125530.png")
                embed.set_image(
                    url="https://cdn.discordapp.com/attachments/838848278858039336/993439008573108244/admin_opinion.gif")

            await ctx.send(embed=embed, ephemeral=True)

        @commands.slash_command(name="server",
                                description="Узнайте информацию нашем сервере",
                                guild_ids=module_server_info)
        async def serverinfo(self, ctx):
            if ctx.guild:
                now = datetime.now(timezone(timedelta(hours=+3)))

                offline = []
                online = []
                idle = []
                dnd = []

                guildtimejoin_ = ctx.guild.created_at.timestamp()
                guildtimejoin = f'{round(guildtimejoin_, 0)}'.replace('.0', '')

                bots = []
                for members in ctx.guild.members:
                    if members.bot:
                        bots.append(1)

                for members in ctx.guild.members:
                    if members.status == disnake.Status.offline:
                        offline.append(f'{members.name}#{members.discriminator}')
                    if members.status == disnake.Status.online:
                        online.append(f'{members.name}#{members.discriminator}')
                    if members.status == disnake.Status.idle:
                        idle.append(f'{members.name}#{members.discriminator}')
                    if members.status == disnake.Status.dnd:
                        dnd.append(f'{members.name}#{members.discriminator}')

                member_really_count = len(
                    [x for x in ctx.guild.members if not x.bot])

                emb = disnake.Embed(
                    title=f"Информация о сервере {ctx.guild.name}",
                    timestamp=now,
                    color=0x2f3136)

                try:
                    emb.set_thumbnail(url=ctx.guild.icon)
                except:
                    pass

                if ctx.guild.description is None:
                    emb.add_field(
                        name="Описание сервера",
                        value="Описание сервера не найдено.",
                        inline=False)
                else:
                    emb.add_field(
                        name="Описание сервера",
                        value=ctx.guild.description,
                        inline=False)

                emb.add_field(
                    name="Создатель сервера",
                    value=f"**{ctx.guild.owner}** / **{ctx.guild.owner.mention}**",
                    inline=False)
                emb.add_field(
                    name=f"Участников [{ctx.guild.member_count}]",
                    value=f"<:members:885624936901787738> Людей: **{member_really_count}**\n"
                    f"<:bot:885624937015033947> Ботов: **{len(bots)}**",
                    inline=False)
                emb.add_field(
                    name="По статусам",
                    value=f"<:online:892647180614123540> В сети: {len(online)}\n<:idle:893597436155691038> Не активен: {len(idle)}\n<:dnd:893597424579391529> Не беспокоить: {len(dnd)}\n<:offline:892647180559597568> Не в сети: {len(offline)}",
                    inline=False)
                emb.add_field(
                    name=f"Каналов [{len(ctx.guild.channels)}]",
                    value=f"<:channel_text:885624937002434640> Текстовые: **{len(ctx.guild.text_channels)}**\n"
                    f"<:channel_voice:885624936926945372> Голосовые: **{len(ctx.guild.voice_channels)}**\n"
                    f"<:stage_channel:906947237559537804> Трибунные: **{len(ctx.guild.stage_channels)}**\n"
                    f"<:category:885624936922742834> Категории: **{len(ctx.guild.categories)}**",
                    inline=False)
                emb.add_field(
                    name="Дата создания сервера",
                    value=f'<t:{guildtimejoin}:D> (<t:{guildtimejoin}:R>)',
                    inline=False)

                await ctx.send(embed=emb)

        @commands.slash_command(name="inrole",
                                description="Список пользователей с указаной ролью",
                                guild_ids=module_inrole,
                                options=[disnake.Option(name="role",
                                                        description="Укажите роль",
                                                        type=disnake.OptionType.role,
                                                        required=True)])
        async def inrole(self, ctx, *, role: disnake.Role):
            members_role = []

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
                    await ctx.send(embed=embed)
                    return
                except BaseException:
                    await ctx.send(content="Список пользователей не помещается в сообщение.", ephemeral=True)
                    return

            await ctx.send(embed=embed_0)

#embed2.set_image(url = "https://24-info.pro/uploads/posts/2018-07/1532423293_wallpaper_anime-popa-hentay.jpg")


def setup(bot):
    bot.add_cog(InformationCommands(bot))