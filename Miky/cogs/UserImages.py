import disnake
from disnake import ButtonStyle
from disnake.ext import commands
from cogs.InteractionDatabase import module_avatar, module_banner

class UserImages(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="avatar",
                            description="Показать аватар участника",
                            guild_ids=module_avatar,
                            options=[disnake.Option(name="member",
                                                    description="Укажите любого участника",
                                                    type=disnake.OptionType.user)])
    async def avatar(self, ctx, member: disnake.User = None):
        member = ctx.author if not member else member

        embed = disnake.Embed(title=f"Аватар — {member}", color=0x2f3136)
        embed.set_image(url=member.avatar)
        await ctx.send(embed=embed, view=ServerAvatarButton(ctx.author, member))

    @commands.user_command(name="Avatar", guild_ids=module_avatar)
    async def avataruser(self, ctx, member: disnake.User):
        embed = disnake.Embed(title=f"Аватар — {member}", color=0x2f3136)
        embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
        embed.set_image(url=member.display_avatar)
        await ctx.send(embed=embed, ephemeral=True)

    @commands.slash_command(name="banner",
                            description="Показать баннер участника",
                            guild_ids=module_banner,
                            options=[disnake.Option(name="member",
                                                    description="Укажите любого участника",
                                                    type=disnake.OptionType.user)])
    async def banner(self, ctx, member: disnake.User = None):
        try:
            if member is None:
                member = await self.bot.fetch_user(ctx.author.id)

                embed = disnake.Embed(
                    title=f"Баннер — {member}", color=0x2f3136)
                embed.set_author(
                    name=ctx.author,
                    icon_url=ctx.author.display_avatar)
                embed.set_image(url=member.banner)
                await ctx.send(embed=embed)
            else:
                member = await self.bot.fetch_user(member.id)
                embed = disnake.Embed(
                    title=f"Баннер — {member}", color=0x2f3136)
                embed.set_author(
                    name=ctx.author,
                    icon_url=ctx.author.display_avatar)
                embed.set_image(url=member.banner)
                await ctx.send(embed=embed)
        except BaseException:
            await ctx.send(content="У пользователя не установлен баннер.", ephemeral=True)

    @commands.user_command(name="Banner", guild_ids=module_banner)
    async def banneruser(self, ctx, member: disnake.User):
        try:
            member = await self.bot.fetch_user(member.id)

            embed = disnake.Embed(title=f"Баннер — {member}", color=0x2f3136)
            embed.set_author(
                name=ctx.author,
                icon_url=ctx.author.display_avatar)
            embed.set_image(url=member.banner)
            await ctx.send(embed=embed, ephemeral=True)
        except BaseException:
            await ctx.send(content="У пользователя не установлен баннер.", ephemeral=True)


class ServerAvatarButton(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @disnake.ui.button(label="Аватар на сервере", style=ButtonStyle.grey)
    async def server_avatar_button(self, button, inter):
        for member in inter.mentions:
            embed = disnake.Embed(title=f"Аватар — {member}", color=0x2f3136)
            embed.set_image(url=member.guild_avatar)
            await inter.edit(embed=embed)


def setup(bot):
    bot.remove_cog(UserImages(bot))
