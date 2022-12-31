import disnake
from mcstatus import MinecraftServer
from disnake.ext import tasks, commands


class TaskServers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.taskserver.start()
        self.taskaimemberroles.start()

    @tasks.loop(minutes=30, reconnect=True)
    async def taskserver(self):
        guild = self.bot.get_guild(614081676116754465)
        channel_status = self.bot.get_channel(1025842790460051537)
        msg = await channel_status.fetch_message(1025848185542955029)

        offline = []
        online = []
        idle = []
        dnd = []

        bots = []
        for members in guild.members:
            if members.bot:
                bots.append(1)

        voice_members = 0
        for channels in guild.voice_channels:
            voice = voice_members + len(channels.members)
            voice_members = voice

        for members in guild.members:
            if members.status == disnake.Status.offline:
                offline.append(f'{members.name}#{members.discriminator}')
            if members.status == disnake.Status.online:
                online.append(f'{members.name}#{members.discriminator}')
            if members.status == disnake.Status.idle:
                idle.append(f'{members.name}#{members.discriminator}')
            if members.status == disnake.Status.dnd:
                dnd.append(f'{members.name}#{members.discriminator}')

        member_really_count = len([x for x in guild.members if not x.bot])

        try:
            server = MinecraftServer.lookup("mc.toycube.su")
            status = server.status()
            embed_minecraft = disnake.Embed(
                color=0x2f3136,
                title="Статистика проекта"
            )

            embed_minecraft.add_field(
                name="Статус сервера",
                value="<:yes_minecraft:958081418641149954> Включен"
            )

            embed_minecraft.add_field(
                name="Игроков",
                value=status.players.online
            )

            embed_minecraft.set_thumbnail(url=guild.icon)
        except BaseException:
            embed_minecraft = disnake.Embed(
                color=0x2f3136,
                title="Статистика проекта"
            )

            embed_minecraft.add_field(
                name="Статус сервера",
                value="<:no_minecraft:958081430435541012> Отключен"
            )

            embed_minecraft.set_thumbnail(url=guild.icon)

        embed_discord = disnake.Embed(
            color=0x2f3136,
            title="Статистика сервера Discord"
        )

        embed_discord.add_field(
            name="Общее",
            value=f"<:roles:885624937015033916> Кол-во ролей: **{len(guild.roles)}**\n"
            f"<:channel_voice:885624936926945372> Голосовой онлайн: **{voice_members}**\n"
            f"<:emoji:885624936658501693> Кол-во эмодзи: **{len(guild.emojis)}**")

        embed_discord.add_field(
            name=f"Участников [{guild.member_count}]",
            value=f"<:members:885624936901787738> Людей: **{member_really_count}**\n"
            f"<:bot:885624937015033947> Ботов: **{len(bots)}**")

        embed_discord.add_field(
            name="По статусам",
            value=f"<:online:892647180614123540> В сети: {len(online)}\n"
            f"<:idle:893597436155691038> Не активен: {len(idle)}\n"
            f"<:dnd:893597424579391529> Не беспокоить: {len(dnd)}\n"
            f"<:offline:892647180559597568> Не в сети: {len(offline)}"
        )

        embed_discord.add_field(
            name=f"Каналов [{len(guild.channels)}]",
            value=f"<:channel_text:885624937002434640> Текстовые: **{len(guild.text_channels)}**\n"
            f"<:channel_voice:885624936926945372> Голосовые: **{len(guild.voice_channels)}**\n"
            f"<:stage_channel:906947237559537804> Трибунные: **{len(guild.stage_channels)}**\n"
            f"<:category:885624936922742834> Категории: **{len(guild.categories)}**")

        if guild.premium_tier == 0 and len(
                guild.premium_subscribers) == 0 and guild.premium_subscription_count == 0:
            embed_discord.set_thumbnail(url=guild.icon)
            embed_discord.set_footer(
                text="Статистика обновляется раз в 30 минут.")

            await msg.edit(embeds=[embed_minecraft, embed_discord])
            return

        if guild.premium_tier == 0:
            embed_discord.add_field(
                name="Буст сервера",
                value=f"<:boost_3:885624937090539591> Кол-во бустеров: **{len(guild.premium_subscribers)}**\n"
                f"<a:nitro:877264844921929749> Кол-во бустов: **{guild.premium_subscription_count}**")
        else:
            embed_discord.add_field(
                name="Буст сервера",
                value=f"<a:boosting:916001610319155210> Уровень буста: **{guild.premium_tier}**\n"
                f"<:boost_3:885624937090539591> Кол-во бустеров: **{len(guild.premium_subscribers)}**\n"
                f"<a:nitro:877264844921929749> Кол-во бустов: **{guild.premium_subscription_count}**")

        embed_discord.set_thumbnail(url=guild.icon)
        embed_discord.set_footer(text="Статистика обновляется раз в 30 минут.")

        await msg.edit(embeds=[embed_minecraft, embed_discord])

    @tasks.loop(seconds=1, reconnect=True)
    async def taskaimemberroles(self):
        guild = self.bot.get_guild(614081676116754465)

        master_ai_role = disnake.utils.get(guild.roles, id=1025480913792008277)
        ai_role = disnake.utils.get(guild.roles, id=1025480857949044827)
        bot_role = disnake.utils.get(guild.roles, id=813363371369431050)

        for member in master_ai_role.members:
            if member.bot:
                pass
            else:
                await member.remove_roles(master_ai_role)

        for member in ai_role.members:
            if member.bot:
                pass
            else:
                await member.remove_roles(ai_role)

        for member in bot_role.members:
            if member.bot:
                pass
            else:
                await member.remove_roles(bot_role)


def setup(bot):
    bot.add_cog(TaskServers(bot))
