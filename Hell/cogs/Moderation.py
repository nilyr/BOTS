import disnake
import sqlite3
from disnake import ButtonStyle
from disnake.ext import commands
from disnake.ui import View, Button
from disnake.ext.commands import has_permissions
from datetime import datetime, timezone, timedelta


with sqlite3.connect("database (Hell).db") as db:
    cursor = db.cursor()

    class Moderation(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        async def check_status_personal(self, member):
            if member.status == disnake.Status.offline:
                return '<:offline:892647180559597568>'
            if member.status == disnake.Status.online:
                return '<:online:892647180614123540>'
            if member.status == disnake.Status.dnd:
                return '<:dnd:893597424579391529>'
            if member.status == disnake.Status.idle:
                return '<:idle:893597436155691038>'

        @commands.slash_command(name="clear",
                                description="Очистка сообщений",
                                guild_ids=[614081676116754465],
                                options=[disnake.Option(name="количество",
                                                        description="Количество сообщений",
                                                        type=disnake.OptionType.integer)])
        @has_permissions(manage_messages=True)
        async def clear(self, ctx, количество=1):
            guild_tc = self.bot.get_guild(614081676116754465)

            now = datetime.now(timezone(timedelta(hours=+3)))

            if ctx.guild == guild_tc:
                channel_logs = self.bot.get_channel(1025836634069008395)

            end_embed = disnake.Embed(
                title="Чат был очищен",
                description=f"Было очищено **{количество}** сообщений.",
                color=0x2f3136,
                timestamp=now)
            end_embed.set_footer(text=ctx.author)

            logs = disnake.Embed(
                title="Чат был очищен",
                description=f"Было очищено **{количество}** сообщений!",
                color=0x2f3136,
                timestamp=now)
            logs.set_footer(text=ctx.author)

            if количество < 0 or количество == 0:
                await ctx.send(content="Нельзя указывать число меньше нуля.", ephemeral=True)
                return

            if количество > 500:
                await ctx.send(content="Нельзя указывать число больше пятисот.", ephemeral=True)
                return

            await ctx.send(content="Процесс удаления сообщений пошёл...", ephemeral=True)
            msg = await ctx.original_message()
            await ctx.channel.purge(limit=количество)
            await msg.edit(content="Процесс удаления сообщений прошёл успешно.")
            await ctx.channel.send(embed=end_embed, delete_after=25)
            await channel_logs.send(embed=logs)

        @commands.slash_command(
            name="mute", description="Мут пользователя", guild_ids=[614081676116754465], options=[
                disnake.Option(
                    name="пользователь", description="Укажите пользователя", type=disnake.OptionType.user, required=True), disnake.Option(
                        name="время", description="Укажите время", type=disnake.OptionType.integer, required=True), disnake.Option(
                            name="едниница_времени", description="Укажите единицу времени", choices=[
                                disnake.OptionChoice(
                                    name="секунды", value="seconds"), disnake.OptionChoice(
                                        name="минуты", value="minutes"), disnake.OptionChoice(
                                            name="часы", value="hours"), disnake.OptionChoice(
                                                name="дни", value="days")], required=True), disnake.Option(
                                                    name="причина", description="Укажите причину", type=disnake.OptionType.string, required=True)])
        @has_permissions(moderate_members=True)
        async def mute(self, ctx, пользователь: disnake.Member, время: int, едниница_времени: str, *, причина):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {пользователь.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {пользователь.id} AND lvl_rights = 'DEV'""").fetchone()

            guild_tc = self.bot.get_guild(614081676116754465)

            now = datetime.now(timezone(timedelta(hours=+3)))

            out_seconds_ = (datetime.now() + timedelta(seconds=время)).timestamp()
            out_seconds = f'<t:{round(out_seconds_,0)}:R>'.replace(".0", "")

            out_minutes_ = (
                datetime.now() +
                timedelta(
                    seconds=время *
                    60)).timestamp()
            out_minutes = f'<t:{round(out_minutes_,0)}:R>'.replace(".0", "")

            out_hours_ = (
                datetime.now() +
                timedelta(
                    seconds=время *
                    60 *
                    60)).timestamp()
            out_hours = f'<t:{round(out_hours_,0)}:R>'.replace(".0", "")

            out_days_ = (
                datetime.now() +
                timedelta(
                    seconds=время *
                    60 *
                    60 *
                    24)).timestamp()
            out_days = f'<t:{round(out_days_,0)}:R>'.replace(".0", "")

            if ctx.guild == guild_tc:
                channel_logs = self.bot.get_channel(1025836634069008395)

            if пользователь.current_timeout is not None:
                await ctx.send(content=f"{пользователь.mention} уже заглушен.", ephemeral=True)
                return

            if пользователь.id == ctx.guild.owner.id:
                await ctx.send(content=f"{пользователь.mention} является создателем этого сервера.", ephemeral=True)
                return

            if perms_owner is not None or perms_dev is not None:
                await ctx.send(content="Разраб запретил мне его мутить.", ephemeral=True)
                return

            if пользователь.guild_permissions.administrator:
                await ctx.send(content=f"Я не могу замутить {пользователь.mention} так как у него права Администратора.", ephemeral=True)
                return

            if пользователь.id == ctx.guild.me.id:
                await ctx.send(content="Слушайте, я мутить самого себя не собираюсь.", ephemeral=True)
                return

            if ctx.author.top_role.position < пользователь.top_role.position:
                await ctx.send(content="Ты не можешь замутить человека с ролью выше твоей или такой же как у тебя.", ephemeral=True)
                return

            if пользователь.id == ctx.author.id:
                await ctx.send(content="Я не дам тебе замутить самого себя.", ephemeral=True)
                return

            if пользователь.top_role > ctx.guild.me.top_role:
                await ctx.send(content=f"Я не могу замутить {пользователь.mention} так как его роль выше моей.", ephemeral=True)
                return

            if время > 28 and едниница_времени == "days" or время > 672 and едниница_времени == "hours" or время > 40320 and едниница_времени == "minutes" or время > 2419200 and едниница_времени == "seconds":
                await ctx.send(content="Нельзя мутить на 24 дня и более.", ephemeral=True)
                return

            emb = disnake.Embed(
                title="Мут был выдан",
                description=f"Причина: {причина}",
                color=0x2f3136,
                timestamp=now)
            emb.set_footer(text=ctx.author)
            emb.add_field(
                name="Нарушитель",
                value=пользователь.mention)

            emb_user_button = View()
            emb_user_button.add_item(
                Button(
                    style=ButtonStyle.grey,
                    emoji="📨",
                    label=f"Отправлено с {ctx.guild}",
                    disabled=True))

            emb_user = disnake.Embed(
                title="Вам был выдан мут",
                description=f"Причина: {причина}",
                color=0x2f3136,
                timestamp=now)
            emb_user.set_footer(text=f"Заглушил: {ctx.author}")

            logs = disnake.Embed(
                title="Мут был выдан",
                description=f"Причина: {причина}",
                color=0x2f3136,
                timestamp=now)
            logs.set_footer(text=ctx.author)
            logs.add_field(
                name="Нарушитель",
                value=пользователь.mention)

            if пользователь.voice is not None:
                if пользователь.voice.channel is not None:
                    await пользователь.move_to(None)

            if едниница_времени == "seconds":
                emb.add_field(
                    name="Размут",
                    value=f"{out_seconds}")
                emb_user.add_field(
                    name="Размут",
                    value=f"{out_seconds}")
                logs.add_field(
                    name="Размут",
                    value=f"{out_seconds}")

                await ctx.guild.timeout(пользователь, duration=время, reason=f"{ctx.author}: {причина}")
            if едниница_времени == "minutes":
                emb.add_field(
                    name="Размут",
                    value=f"{out_minutes}")
                emb_user.add_field(
                    name="Размут",
                    value=f"{out_minutes}")
                logs.add_field(
                    name="Размут",
                    value=f"{out_minutes}")

                await ctx.guild.timeout(пользователь, duration=время*60, reason=f"{ctx.author}: {причина}")
            if едниница_времени == "hours":
                emb.add_field(
                    name="Размут",
                    value=f"{out_hours}")
                emb_user.add_field(
                    name="Размут",
                    value=f"{out_hours}")
                logs.add_field(
                    name="Размут",
                    value=f"{out_hours}")

                await ctx.guild.timeout(пользователь, duration=время*60*60, reason=f"{ctx.author}: {причина}")
            if едниница_времени == "days":
                emb.add_field(
                    name="Размут",
                    value=f"{out_days}")
                emb_user.add_field(
                    name="Размут",
                    value=f"{out_days}")
                logs.add_field(
                    name="Размут",
                    value=f"{out_days}")

                await ctx.guild.timeout(пользователь, duration=время*60*60*24, reason=f"{ctx.author}: {причина}")

            await ctx.send(embed=emb)
            try:
                await пользователь.send(embed=emb_user, view=emb_user_button)
            except BaseException:
                pass
            await channel_logs.send(embed=logs)

        @commands.slash_command(name="unmute",
                                description="Размут пользователя",
                                guild_ids=[614081676116754465],
                                options=[disnake.Option(name="пользователь",
                                                        description="Укажите пользователя",
                                                        type=disnake.OptionType.user,
                                                        required=True)])
        @has_permissions(moderate_members=True)
        async def unmute(self, ctx, пользователь: disnake.Member):
            guild_tc = self.bot.get_guild(614081676116754465)

            now = datetime.now(timezone(timedelta(hours=+3)))

            if ctx.guild == guild_tc:
                channel_logs = self.bot.get_channel(1025836634069008395)

            if пользователь.current_timeout is not None:
                if пользователь.id == ctx.author.id:
                    await ctx.send(content="Я не дам тебе размутить самого себя.", ephemeral=True)
                    return

                emb = disnake.Embed(
                    title="Размут был выдан",
                    color=0x2f3136,
                    timestamp=now)
                emb.set_footer(text=ctx.author)
                emb.add_field(
                    name="Разглушенный пользователь",
                    value=пользователь.mention)

                emb_user_button = View()
                emb_user_button.add_item(
                    Button(
                        style=ButtonStyle.grey,
                        emoji="📨",
                        label=f"Отправлено с {ctx.guild}",
                        disabled=True))

                emb_user = disnake.Embed(
                    title="Вам был выдан размут",
                    color=0x2f3136,
                    timestamp=now)
                emb_user.set_footer(text=f"Заглушил: {ctx.author}")

                logs = disnake.Embed(
                    title="Размут был выдан",
                    color=0x2f3136,
                    timestamp=now)
                logs.set_footer(text=ctx.author)
                logs.add_field(
                    name="Разглушенный пользователь",
                    value=пользователь.mention)

                await ctx.guild.timeout(пользователь, duration=None, reason=f"{ctx.author}")
                await ctx.send(embed=emb)
                try:
                    await пользователь.send(embed=emb_user, view=emb_user_button)
                except BaseException:
                    pass
                await channel_logs.send(embed=logs)
            else:
                await ctx.send(content="Данный пользователь не находится в муте.", ephemeral=True)


        @commands.slash_command(name="ban",
                                description="Пермаментный бан пользователя",
                                guild_ids=[614081676116754465],
                                options=[disnake.Option(name="пользователь",
                                                        description="Укажите пользователя",
                                                        type=disnake.OptionType.user,
                                                        required=True),
                                        disnake.Option(name="причина",
                                                    description="Укажите причину",
                                                    type=disnake.OptionType.string,
                                                    required=True)])
        @has_permissions(ban_members=True)
        async def permamentban(self, ctx, пользователь: disnake.Member, *, причина):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {пользователь.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {пользователь.id} AND lvl_rights = 'DEV'""").fetchone()

            guild_tc = self.bot.get_guild(614081676116754465)

            now = datetime.now(timezone(timedelta(hours=+3)))

            if ctx.guild == guild_tc:
                channel_logs = self.bot.get_channel(1025836634069008395)
                
            if пользователь.id == ctx.guild.owner.id:
                await ctx.send(content=f"{пользователь.mention} является создателем этого сервера.", ephemeral=True)
                return

            if perms_owner is not None or perms_dev is not None:
                await ctx.send(content="Разраб запретил мне его мутить.", ephemeral=True)
                return

            if пользователь.guild_permissions.administrator:
                await ctx.send(content=f"Я не могу забанить {пользователь.mention} так как у него права Администратора.", ephemeral=True)
                return

            if пользователь.id == ctx.guild.me.id:
                await ctx.send(content="Слушайте, я банить самого себя не собираюсь.", ephemeral=True)
                return

            if ctx.author.top_role.position < пользователь.top_role.position:
                await ctx.send(content="Ты не можешь забанить человека с ролью выше твоей или такой же как у тебя.", ephemeral=True)
                return

            if пользователь.id == ctx.author.id:
                await ctx.send(content="Я не дам тебе забанить самого себя.", ephemeral=True)
                return

            if пользователь.top_role > ctx.guild.me.top_role:
                await ctx.send(content=f"Я не могу забанить {пользователь.mention} так как его роль выше моей.", ephemeral=True)
                return

            emb = disnake.Embed(
                title="Пермаментный бан был выдан",
                description=f"Причина: {причина}",
                color=0x2f3136,
                timestamp=now)
            emb.set_footer(text=ctx.author)
            emb.add_field(
                name="Нарушитель",
                value=пользователь.mention)

            emb_user_button = View()
            emb_user_button.add_item(
                Button(
                    style=ButtonStyle.grey,
                    emoji="📨",
                    label=f"Отправлено с {ctx.guild}",
                    disabled=True))

            emb_user = disnake.Embed(
                title="Вам был выдан пермаментный бан",
                description=f"Причина: {причина}",
                color=0x2f3136,
                timestamp=now)
            emb_user.set_footer(text=f"Забанил: {ctx.author}")

            logs = disnake.Embed(
                title="Пермаментный бан был выдан",
                description=f"Причина: {причина}",
                color=0x2f3136,
                timestamp=now)
            logs.set_footer(text=ctx.author)
            logs.add_field(
                name="Нарушитель",
                value=пользователь.mention)

            await ctx.guild.ban(пользователь, reason=f"{ctx.author}: {причина}")
            try:
                await пользователь.send(embed=emb_user, view=emb_user_button)
            except BaseException:
                pass
            await ctx.send(embed=emb)
            await channel_logs.send(embed=logs)

        @commands.slash_command(name="unban",
                                description="Пермаментный разбан пользователя",
                                guild_ids=[614081676116754465],
                                options=[disnake.Option(name="пользователь",
                                                        description="Укажите пользователя",
                                                        type=disnake.OptionType.user,
                                                        required=True)])
        @has_permissions(ban_members=True)
        async def unpermamentban(self, ctx, пользователь: disnake.Member):
            guild_tc = self.bot.get_guild(614081676116754465)

            now = datetime.now(timezone(timedelta(hours=+3)))
            banned_users = await ctx.guild.bans(limit=123).flatten()

            if ctx.guild == guild_tc:
                channel_logs = self.bot.get_channel(1025836634069008395)

            if пользователь.id == ctx.guild.me.id:
                await ctx.send(content="Слушайте, я к вашему великому сожалению, в бане не нахожусь.", ephemeral=True)
                return

            emb = disnake.Embed(
                title="Пермаментный разбан был выдан",
                color=0x2f3136,
                timestamp=now)
            emb.set_footer(text=ctx.author)
            emb.add_field(
                name="Разбаненный пользователь",
                value=пользователь.mention)

            emb_user_button = View()
            emb_user_button.add_item(
                Button(
                    style=ButtonStyle.grey,
                    emoji="📨",
                    label=f"Отправлено с {ctx.guild}",
                    disabled=True))

            emb_user = disnake.Embed(
                title="Вам был выдан пермаментный разбан",
                color=0x2f3136,
                timestamp=now)
            emb_user.set_footer(text=f"Разбанил: {ctx.author}")

            logs = disnake.Embed(
                title="Пермаментный разбан был выдан",
                color=0x2f3136,
                timestamp=now)
            logs.set_footer(text=ctx.author)
            logs.add_field(
                name="Разбаненный пользователь",
                value=пользователь.mention)

            for member in banned_users:
                member = пользователь

                try:
                    await ctx.guild.unban(member, reason=f"Выдал разбан: {ctx.author}")
                    try:
                        await member.send(embed=emb_user, view=emb_user_button)
                    except BaseException:
                        pass
                    await ctx.send(embed=emb)
                    await channel_logs.send(embed=logs)
                    return
                except BaseException:
                    await ctx.send(content="Данный пользователь не находится в пермаментном бане.", ephemeral=True)
                    return

        @commands.slash_command(name="staff",
                                description="Посмотреть онлайн Персонала Discord",
                                guild_ids=[614081676116754465])
        async def stafflist(self, ctx):
            guild_tc = self.bot.get_guild(614081676116754465)

            sostav = []

            if ctx.guild == guild_tc:
                discord_lead_role = disnake.utils.get(ctx.guild.roles, id=813671668442333184)
                admin_discord_role = disnake.utils.get(ctx.guild.roles, id=813387947733680210)
                security_discord_role = disnake.utils.get(ctx.guild.roles, id=813365784487133204)
                moder_discord_role = disnake.utils.get(ctx.guild.roles, id=813385204059865108)
                assistant_discord_role = disnake.utils.get(ctx.guild.roles, id=813363055626289152)

                for member in discord_lead_role.members:
                    sostav.append(f'{await self.check_status_personal(member)} **`{member}`** <a:tochka_anim1:978740315676631092> {discord_lead_role.mention}')

                for member in admin_discord_role.members:
                    sostav.append(f'{await self.check_status_personal(member)} **`{member}`** <a:tochka_anim1:978740315676631092> {admin_discord_role.mention}')
                
                for member in security_discord_role.members:
                    sostav.append(f'{await self.check_status_personal(member)} **`{member}`** <a:tochka_anim1:978740315676631092> {security_discord_role.mention}')

                for member in moder_discord_role.members:
                    sostav.append(f'{await self.check_status_personal(member)} **`{member}`** <a:tochka_anim1:978740315676631092> {moder_discord_role.mention}')
                
                for member in assistant_discord_role.members:
                    sostav.append(f'{await self.check_status_personal(member)} **`{member}`** <a:tochka_anim1:978740315676631092> {assistant_discord_role.mention}')
            
            personal = f'{str(sostav)}'.replace('[', '').replace(']', '').replace(',', '\n').replace("'", "").replace('"', '')
                
            embed_end = disnake.Embed(
                title="Персонал сервера",
                description=f"{personal}",
                color=0x2f3136)
            embed_end.set_image(
                url="https://cdn.discordapp.com/attachments/834837020056616992/992091846257950782/typo_staff.gif")

            await ctx.response.defer()
            await ctx.send(embed=embed_end)

        @commands.slash_command(name="sos",
                                description="Сообщить о нарушении модерации сервера",
                                guild_ids=[614081676116754465],
                                options=[disnake.Option(name="причина",
                                                        description="Укажите причину",
                                                        type=disnake.OptionType.string,
                                                        required=True)])
        @commands.cooldown(1, 3600, commands.BucketType.user)
        async def sos(self, ctx, *, причина):
            guild_tc = self.bot.get_guild(614081676116754465)

            emb = disnake.Embed(
                color=0x2f3136,
                title="Найдено нарушение",
                description=f"Нарушение: {причина}")
            emb.set_footer(text=f"Вызвал: {ctx.author}")
            emb.set_image(url="https://images-ext-2.discordapp.net/external/zvx2Ey8dUmAmYJcRDNGs68xxjrivhcXMsCJOLpFTLUM/https/i.pinimg.com/originals/9e/45/f4/9e45f4a736e361f369a1e7dd1378c6e1.gif")

            if ctx.guild == guild_tc:
                discord_team_role = disnake.utils.get(ctx.guild.roles, id=825112987446673488)

                await ctx.send(content="Команда вызвана успешно.", ephemeral=True)
                await ctx.channel.send(content=discord_team_role.mention, embed=emb)

def setup(bot):
    bot.add_cog(Moderation(bot))