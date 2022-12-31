import disnake
from disnake.ext import tasks, commands

class PrivateСhannels(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.kptaskvoice.start()
        self.kptasklenvoice.start()

    @tasks.loop(seconds=1, reconnect=True)
    async def kptaskvoice(self):
        guild = self.bot.get_guild(387409949442965506)
        voiceperm_role = disnake.utils.get(guild.roles, id=845003968009732096)

        category = disnake.utils.get(guild.categories, id=725129148464627722)
        channel_private = self.bot.get_channel(777968491385978902)

        for channel in category.voice_channels:
            if channel == channel_private:
                for member in channel.members:
                    try:
                        channel_private = await guild.get_channel(category.id).create_voice_channel(member.name)
                        await member.move_to(channel_private)
                        await channel_private.set_permissions(member, view_channel=True, manage_channels=True, connect=True, speak=True, move_members=True, stream=True)
                        await channel_private.set_permissions(voiceperm_role, connect=True, speak=True, stream=True, mute_members=False, deafen_members=False, manage_permissions=False, manage_channels=False)
                    except BaseException:
                        await member.move_to(None)

                        try:
                            await member.send(content="Перезайдите в канал создания приватки.")
                        except BaseException:
                            pass

    @tasks.loop(seconds=2, reconnect=True)
    async def kptasklenvoice(self):
        guild = self.bot.get_guild(387409949442965506)
        category = disnake.utils.get(guild.categories, id=725129148464627722)
        channel_private = self.bot.get_channel(777968491385978902)

        for channel in category.voice_channels:
            if len(channel.members) <= 0:
                if channel != channel_private:
                    await channel.delete()

    @commands.slash_command(guild_ids=[387409949442965506])
    async def room(self, ctx):
        pass

    @room.sub_command(name="name",
                      description="Изменить название приватного канала",
                      options=[disnake.Option(name="argument",
                                              description="Укажите название канала",
                                              type=disnake.OptionType.string,
                                              required=True)])
    async def subroomname(self, ctx, *, argument):
        guild_kp = self.bot.get_guild(387409949442965506)

        if ctx.guild == guild_kp:
            category = disnake.utils.get(ctx.guild.categories, id=725129148464627722)
            channel_private = self.bot.get_channel(387409949442965506)

        if not ctx.author.voice:
            await ctx.send(content="Вы не находитесь в голосовых каналах.", ephemeral=True)
            return

        if ctx.author.voice.channel.category != category:
            await ctx.send(content="Вы находитесь вне категории приватных каналов.", ephemeral=True)
            return

        if ctx.author.voice.channel == channel_private:
            await ctx.send(content="Вы находитесь в канале создания приваток.", ephemeral=True)
            return

        if ctx.author.voice.channel.permissions_for(
                ctx.author).manage_channels:
            await ctx.author.voice.channel.edit(name=argument)
            await ctx.send(content=f"Название канала изменено на: **{argument}**.", ephemeral=True)
            return

        await ctx.send(content="У вас недостаточно прав.", ephemeral=True)

    @room.sub_command(name="limit",
                      description="Изменить лимит пользователей приватного канала",
                      options=[disnake.Option(name="limit",
                                              description="Укажите название канала",
                                              type=disnake.OptionType.integer,
                                              required=True)])
    async def subroomlimit(self, ctx, limit):
        guild_kp = self.bot.get_guild(387409949442965506)

        if ctx.guild == guild_kp:
            category = disnake.utils.get(ctx.guild.categories, id=725129148464627722)
            channel_private = self.bot.get_channel(387409949442965506)

        if not ctx.author.voice:
            await ctx.send(content="Вы не находитесь в голосовых каналах.", ephemeral=True)
            return

        if ctx.author.voice.channel.category != category:
            await ctx.send(content="Вы находитесь вне категории приватных каналов.", ephemeral=True)
            return

        if ctx.author.voice.channel == channel_private:
            await ctx.send(content="Вы находитесь в канале создания приваток.", ephemeral=True)
            return

        if ctx.author.voice.channel.permissions_for(
                ctx.author).manage_channels:
            if limit > 99:
                await ctx.send(content="Лимит не может достигать более 99 пользователей.", ephemeral=True)
                return

            await ctx.author.voice.channel.edit(user_limit=limit)
            await ctx.send(content=f"Лимит канала изменён на: **{limit}** пользователей.", ephemeral=True)
            return

        await ctx.send(content="У вас недостаточно прав.", ephemeral=True)

    @room.sub_command(name="kick",
                      description="Кикнуть участника из приватного канала",
                      options=[disnake.Option(name="member",
                                              description="Укажите любого участника",
                                              type=disnake.OptionType.user,
                                              required=True)])
    async def subroomkick(self, ctx, member: disnake.Member):
        guild_kp = self.bot.get_guild(387409949442965506)

        if ctx.guild == guild_kp:
            category = disnake.utils.get(ctx.guild.categories, id=725129148464627722)
            channel_private = self.bot.get_channel(387409949442965506)

        if not ctx.author.voice:
            await ctx.send(content="Вы не находитесь в голосовых каналах.", ephemeral=True)
            return

        if ctx.author.voice.channel.category != category:
            await ctx.send(content="Вы находитесь вне категории приватных каналов.", ephemeral=True)
            return

        if ctx.author.voice.channel == channel_private:
            await ctx.send(content="Вы находитесь в канале создания приваток.", ephemeral=True)
            return

        if ctx.author.voice.channel.permissions_for(
                ctx.author).manage_channels:
            if member == ctx.author:
                await ctx.send(content="Зачем кикать себя из своей же приватки?", ephemeral=True)
                return

            if member.voice is not None:
                if member.voice.channel == ctx.author.voice.channel:
                    await member.move_to(None)
                    await ctx.send(content=f"Из приватного канала был кикнут: **{member.mention}**.", ephemeral=True)
                    return

            await ctx.send(content=f"Не удалось кикнуть участника из канала. Данный участник не находится в вашем войсе!", ephemeral=True)
            return

        await ctx.send(content="У вас недостаточно прав.", ephemeral=True)

    @room.sub_command(name="lock",
                      description="Закрыть приватный канал",
                      options=[disnake.Option(name="member",
                                              description="Укажите любого участника",
                                              type=disnake.OptionType.user)])
    async def subroomlock(self, ctx, member: disnake.Member = None):
        guild_kp = self.bot.get_guild(387409949442965506)

        if ctx.guild == guild_kp:
            category = disnake.utils.get(ctx.guild.categories, id=725129148464627722)
            channel_private = self.bot.get_channel(387409949442965506)

            voiceperm_role = disnake.utils.get(ctx.guild.roles, id=845003968009732096)

            if not ctx.author.voice:
                await ctx.send(content="Вы не находитесь в голосовых каналах.", ephemeral=True)
                return

            if ctx.author.voice.channel.category != category:
                await ctx.send(content="Вы находитесь вне категории приватных каналов.", ephemeral=True)
                return

            if ctx.author.voice.channel == channel_private:
                await ctx.send(content="Вы находитесь в канале создания приваток.", ephemeral=True)
                return

            if ctx.author.voice.channel.permissions_for(
                    ctx.author).manage_channels:
                if member == ctx.author:
                    await ctx.send(content="Зачем закрывать себе доступ в своей же приватке?", ephemeral=True)
                    return

                if member is None:
                    await ctx.author.voice.channel.set_permissions(voiceperm_role, connect=False)
                    await ctx.send(content=f"Приватный канал был закрыт для **всех**.", ephemeral=True)
                    return

                await ctx.author.voice.channel.set_permissions(member, connect=False)

                if member.voice is not None:
                    if member.voice.channel == ctx.author.voice.channel:
                        await member.move_to(None)

                await ctx.send(content=f"Приватный канал был закрыт для **{member.mention}**.", ephemeral=True)
                return

            await ctx.send(content="У вас недостаточно прав.", ephemeral=True)
            return

    @room.sub_command(name="unlock",
                      description="Открыть приватный канал",
                      options=[disnake.Option(name="member",
                                              description="Укажите любого участника",
                                              type=disnake.OptionType.user)])
    async def subroomunlock(self, ctx, member: disnake.Member = None):
        guild_kp = self.bot.get_guild(387409949442965506)

        if ctx.guild == guild_kp:
            category = disnake.utils.get(ctx.guild.categories, id=725129148464627722)
            channel_private = self.bot.get_channel(387409949442965506)

            voiceperm_role = disnake.utils.get(ctx.guild.roles, id=845003968009732096)

            if not ctx.author.voice:
                await ctx.send(content="Вы не находитесь в голосовых каналах.", ephemeral=True)
                return

            if ctx.author.voice.channel.category != category:
                await ctx.send(content="Вы находитесь вне категории приватных каналов.", ephemeral=True)
                return

            if ctx.author.voice.channel == channel_private:
                await ctx.send(content="Вы находитесь в канале создания приваток.", ephemeral=True)
                return

            if ctx.author.voice.channel.permissions_for(
                    ctx.author).manage_channels:
                if member == ctx.author:
                    await ctx.send(content="Зачем открывать себе доступ в своей же приватке?", ephemeral=True)
                    return

                if member is None:
                    await ctx.author.voice.channel.set_permissions(voiceperm_role, connect=True)
                    await ctx.send(content=f"Приватный канал был открыт для **всех**.", ephemeral=True)
                    return

                await ctx.author.voice.channel.set_permissions(member, connect=True)
                await ctx.send(content=f"Приватный канал был открыт для **{member.mention}**.", ephemeral=True)
                return

            await ctx.send(content="У вас недостаточно прав.", ephemeral=True)
            return


def setup(bot):
    bot.add_cog(PrivateСhannels(bot))