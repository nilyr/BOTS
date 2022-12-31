import disnake
from disnake.ext import tasks, commands


class TaskServers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.taskstatusmembers.start()
        self.taskaimemberroles.start()

    @tasks.loop(minutes=30, reconnect=True)
    async def taskstatusmembers(self):
        guild = self.bot.get_guild(387409949442965506)
        channel_status_voice_members = self.bot.get_channel(927487215624392774)
        channel_members = self.bot.get_channel(927487246779695104)
        channel_status_members = self.bot.get_channel(927487993512591360)

        online = []
        idle = []
        dnd = []

        voice_members = 0
        for channels in guild.voice_channels:
            voice = voice_members + len(channels.members)
            voice_members = voice

        for members in guild.members:
            if members.status == disnake.Status.online:
                online.append(f'{members.name}#{members.discriminator}')

            if members.status == disnake.Status.idle:
                idle.append(f'{members.name}#{members.discriminator}')
                
            if members.status == disnake.Status.dnd:
                dnd.append(f'{members.name}#{members.discriminator}')

        await channel_status_voice_members.edit(name=f"🔊 В голосовых: {voice_members}")
        await channel_members.edit(name=f"👥 Участников: {guild.member_count}")
        await channel_status_members.edit(name=f"🟢 {len(online)} ⛔ {len(dnd)} 🌙 {len(idle)}")

    @tasks.loop(seconds=1, reconnect=True)
    async def taskaimemberroles(self):
        guild = self.bot.get_guild(387409949442965506)

        master_ai_role = disnake.utils.get(guild.roles, id=993531794743894026)
        senior_ai_role = disnake.utils.get(guild.roles, id=993531804424343633)
        ai_role = disnake.utils.get(guild.roles, id=993531807360368755)
        bot_role = disnake.utils.get(guild.roles, id=610843872792281088)

        for member in master_ai_role.members:
            if member.bot:
                pass
            else:
                await member.remove_roles(master_ai_role)

        for member in senior_ai_role.members:
            if member.bot:
                pass
            else:
                await member.remove_roles(senior_ai_role)

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
