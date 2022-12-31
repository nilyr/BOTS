import disnake
import random
import nekos
from disnake.ext import commands
from cogs.InteractionDatabase import module_reaction_commands


class ReactionСommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    gif_punch = [
        "https://neko-love.xyz/v1/punch/neko-love-punch_7.gif",
        "https://neko-love.xyz/v1/punch/neko-love-punch_2.gif",
        "https://neko-love.xyz/v1/punch/neko-love-punch_3.gif",
        "https://neko-love.xyz/v1/punch/neko-love-punch_12.gif",
        "https://neko-love.xyz/v1/punch/neko-love-punch_6.gif",
        "https://neko-love.xyz/v1/punch/neko-love-punch_10.gif",
        "https://neko-love.xyz/v1/punch/neko-love-punch_11.gif",
        "https://neko-love.xyz/v1/punch/neko-love-punch_13.gif",
        "https://neko-love.xyz/v1/punch/neko-love-punch_9.gif",
        "https://media1.tenor.com/images/e7e2fd04ec681304d1db9e52b0147b57/tenor.gif"]

    gif_bite = [
        "https://media.tenor.com/images/785facc91db815ae613926cddb899ed4/tenor.gif",
        "https://media.tenor.com/images/2fea7567f38e27d7d571b32e87d0dd15/tenor.gif",
        "https://media.tenor.com/images/57f08a1c0a7999f98d4d2cc6f2a33666/tenor.gif",
        "https://media.tenor.com/images/774226b902dac2639f2162bc40e1ad83/tenor.gif",
        "https://media.tenor.com/images/17ba890dc4bd5aed76ddb152ff6753a7/tenor.gif",
        "https://media.tenor.com/images/b9c3cd95d4e40e8f2cfdeb7756dc93ee/tenor.gif",
        "https://media.tenor.com/images/4d5f122005aa56241929550c49a0abf9/tenor.gif",
        "https://media.tenor.com/images/34a08d324868d33358e0a465040f210e/tenor.gif",
        "https://media.tenor.com/images/e2c3b97c6bcf475ec0eed309c553d719/tenor.gif"]

    @commands.slash_command(name="hug",
                            description="Обнять участника",
                            guild_ids=module_reaction_commands,
                            options=[disnake.Option(name="member",
                                                    description="Укажите любого участника",
                                                    type=disnake.OptionType.user),
                                     disnake.Option(name="argument",
                                                    description="Укажите причину",
                                                    type=disnake.OptionType.string)])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def hug(self, ctx, member: disnake.User = None, *, argument=None):
        member = ctx.author if not member else member

        if member.bot:
            await ctx.send(content="Это же бездушная машина, зачем её обнимать?", ephemeral=True)
            return

        if member == ctx.author and argument is None:
            embed = disnake.Embed(
                color=0x2f3136,
                description=f"**{ctx.author.mention}** обнимает **самого себя!**")

            embed.set_image(url=nekos.img("hug"))

            await ctx.send(embed=embed)
            return

        if member == ctx.author:
            embed = disnake.Embed(
                color=0x2f3136,
                description=f"**{ctx.author.mention}** обнимает **самого себя!**\nПотому что **{argument}**"
            )

            embed.set_image(url=nekos.img("hug"))

            await ctx.send(embed=embed)
            return

        if argument is None:
            embed = disnake.Embed(
                color=0x2f3136,
                description=f"**{ctx.author.mention}** обнимает **{member.mention}**")

            embed.set_image(url=nekos.img("hug"))

            await ctx.send(embed=embed)
            return

        embed = disnake.Embed(
            color=0x2f3136,
            description=f"**{ctx.author.mention}** обнимает **{member.mention}**\nПотому что **{argument}**"
        )

        embed.set_image(url=nekos.img("hug"))

        await ctx.send(embed=embed)

    @commands.slash_command(name="kiss",
                            description="Поцеловать участника",
                            guild_ids=module_reaction_commands,
                            options=[disnake.Option(name="member",
                                                    description="Укажите любого участника",
                                                    type=disnake.OptionType.user),
                                     disnake.Option(name="argument",
                                                    description="Укажите причину",
                                                    type=disnake.OptionType.string)])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def kiss(self, ctx, member: disnake.User = None, *, argument=None):
        member = ctx.author if not member else member

        if member.bot:
            await ctx.send(content="Это же бездушная машина, зачем её целовать?", ephemeral=True)
            return

        if member == ctx.author and argument is None:
            embed = disnake.Embed(
                color=0x2f3136,
                description=f"**{ctx.author.mention}** целует **самого себя!**"
            )

            embed.set_image(url=nekos.img("kiss"))

            await ctx.send(embed=embed)
            return

        if member == ctx.author:
            embed = disnake.Embed(
                color=0x2f3136,
                description=f"**{ctx.author.mention}** целует **самого себя!**\nПотому что **{argument}**"
            )

            embed.set_image(url=nekos.img("kiss"))

            await ctx.send(embed=embed)
            return

        if argument is None:
            embed = disnake.Embed(
                color=0x2f3136,
                description=f"**{ctx.author.mention}** целует **{member.mention}**")

            embed.set_image(url=nekos.img("kiss"))

            await ctx.send(embed=embed)
            return

        embed = disnake.Embed(
            color=0x2f3136,
            description=f"**{ctx.author.mention}** целует **{member.mention}**\nПотому что **{argument}**"
        )

        embed.set_image(url=nekos.img("kiss"))

        await ctx.send(embed=embed)

    @commands.slash_command(name="punch",
                            description="Ударить участника",
                            guild_ids=module_reaction_commands,
                            options=[disnake.Option(name="member",
                                                    description="Укажите любого участника",
                                                    type=disnake.OptionType.user),
                                     disnake.Option(name="argument",
                                                    description="Укажите причину",
                                                    type=disnake.OptionType.string)])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def punch(self, ctx, member: disnake.User = None, *, argument=None):
        member = ctx.author if not member else member

        if member.bot:
            await ctx.send(content="Это же бездушная машина, зачем её бить?", ephemeral=True)
            return

        if member == ctx.author and argument is None:
            embed = disnake.Embed(
                color=0x2f3136,
                description=f"**{ctx.author.mention}** ударяет **самого себя!**")

            embed.set_image(url=random.choice(self.gif_punch))

            await ctx.send(embed=embed)
            return

        if member == ctx.author:
            embed = disnake.Embed(
                color=0x2f3136,
                description=f"**{ctx.author.mention}** ударяет **самого себя!**\nПотому что **{argument}**"
            )

            embed.set_image(url=random.choice(self.gif_punch))

            await ctx.send(embed=embed)
            return

        if argument is None:
            embed = disnake.Embed(
                color=0x2f3136,
                description=f"**{ctx.author.mention}** ударяет **{member.mention}**")

            embed.set_image(url=random.choice(self.gif_punch))

            await ctx.send(embed=embed)
            return

        embed = disnake.Embed(
            color=0x2f3136,
            description=f"**{ctx.author.mention}** ударяет **{member.mention}**\nПотому что **{argument}**"
        )

        embed.set_image(url=random.choice(self.gif_punch))

        await ctx.send(embed=embed)

    @commands.slash_command(name="bite",
                            description="Укусить участника",
                            guild_ids=module_reaction_commands,
                            options=[disnake.Option(name="member",
                                                    description="Укажите любого участника",
                                                    type=disnake.OptionType.user),
                                     disnake.Option(name="argument",
                                                    description="Укажите причину",
                                                    type=disnake.OptionType.string)])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def bite(self, ctx, member: disnake.User = None, *, argument=None):
        member = ctx.author if not member else member

        if member.bot:
            await ctx.send(content="Это же бездушная машина, зачем её куськать?", ephemeral=True)
            return

        if member == ctx.author and argument is None:
            embed = disnake.Embed(
                color=0x2f3136,
                description=f"**{ctx.author.mention}** кусает **самого себя!**"
            )

            embed.set_image(url=random.choice(self.gif_bite))

            await ctx.send(embed=embed)
            return

        if member == ctx.author:
            embed = disnake.Embed(
                color=0x2f3136,
                description=f"**{ctx.author.mention}** кусает **самого себя!**\nПотому что **{argument}**"
            )

            embed.set_image(url=random.choice(self.gif_bite))

            await ctx.send(embed=embed)
            return

        if argument is None:
            embed = disnake.Embed(
                color=0x2f3136,
                description=f"**{ctx.author.mention}** кусает **{member.mention}**")

            embed.set_image(url=random.choice(self.gif_bite))

            await ctx.send(embed=embed)
            return

        embed = disnake.Embed(
            color=0x2f3136,
            description=f"**{ctx.author.mention}** кусает **{member.mention}**\nПотому что **{argument}**"
        )

        embed.set_image(url=random.choice(self.gif_bite))

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ReactionСommands(bot))
