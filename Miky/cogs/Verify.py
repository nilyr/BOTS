import disnake
import sqlite3
from disnake import ButtonStyle
from disnake.ext import commands
from disnake.ui import View, Button
from cogs.InteractionDatabase import natame_guild, mossymineskills_guild

with sqlite3.connect("database (Miky).db") as db:
    cursor = db.cursor()

    class Verification(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.command(name="verify")
        async def verifyinformation(self, ctx):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            guild_na = self.bot.get_guild(natame_guild)
            guild_mm = self.bot.get_guild(mossymineskills_guild)

            if perms_owner is not None or perms_dev is not None:
                if ctx.guild == guild_na:
                    channel_verify = self.bot.get_channel(997429823473455135)

                    embed = disnake.Embed(
                        color=0x2f3136,
                        title="Верификация",
                        description=f"Приветствую тебя на дискорд сервере `{ctx.guild}`.\n**Ты находишься в начальном канале верификации.**\n\nЧтобы пройти верификацию, тебе нужно нажать на кнопку внизу этого сообщения."
                    )

                    embed.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/992086461581119658/Verify.gif")
                    embed.set_footer(
                        text="После прохождения верификации ты свободно сможешь общаться на этом сервере.")

                    verify_button = View()
                    verify_button.add_item(
                        Button(
                            style=ButtonStyle.grey,
                            label="Верификация",
                            custom_id="verify_button"))
                    
                    await ctx.message.delete()
                    await channel_verify.purge()
                    await channel_verify.send(embed=embed, view=verify_button)
                    return

                if ctx.guild == guild_mm:
                    channel_verify = self.bot.get_channel(999339946362019981)

                    embed = disnake.Embed(
                        color=0x2f3136,
                        title="Верификация",
                        description=f"Приветствую тебя на дискорд сервере `{ctx.guild}`.\n**Ты находишься в начальном канале верификации.**\n\nЧтобы пройти верификацию, тебе нужно нажать на кнопку внизу этого сообщения."
                    )

                    embed.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/992086461581119658/Verify.gif")
                    embed.set_footer(
                        text="После прохождения верификации ты свободно сможешь общаться на этом сервере.")

                    verify_button = View()
                    verify_button.add_item(
                        Button(
                            style=ButtonStyle.grey,
                            label="Верификация",
                            custom_id="verify_button"))
                    
                    await ctx.message.delete()
                    await channel_verify.purge()
                    await channel_verify.send(embed=embed, view=verify_button)
                    return

            await ctx.message.delete(delay=5)
            await ctx.reply(content="Права на использование есть только у разработчика бота.", delete_after=5)

        @commands.Cog.listener()
        async def on_button_click(self, inter):
            guild_na = self.bot.get_guild(natame_guild)
            guild_mm = self.bot.get_guild(mossymineskills_guild)

            if inter.guild == guild_na:
                channel_chat = self.bot.get_channel(1006515165572890674)
                
                verify_role = disnake.utils.get(inter.guild.roles, id=997429040824733746)
                user_role = disnake.utils.get(inter.guild.roles, id=995992349480058960)

                female_role = disnake.utils.get(inter.guild.roles, id=1006871226968453162)
                male_role = disnake.utils.get(inter.guild.roles, id=1006873929488543764)

                gender_button = View()
                gender_button.add_item(
                    Button(
                        style=ButtonStyle.grey,
                        emoji="<:Male:985985761679642725>",
                        label="Мальчик",
                        custom_id="male_button"))
                gender_button.add_item(
                    Button(
                        style=ButtonStyle.grey,
                        emoji="<:Female:985985786476384268>",
                        label="Девочка",
                        custom_id="female_button"))

                gender_embed = disnake.Embed(
                    color=0x2f3136,
                    title="Выберите свой пол")

                embed_chat = disnake.Embed(
                    color=0x2f3136,
                    title="Приветствуем! Рады тебя видеть 🤗",
                    description=f"Рады тебя видеть, {inter.author.mention}! Присаживайся, рассказывай, как твои дела? Может тебе чаю? Кофе? А хотя знаешь, уверен, местные жители тебе со всем помогут 😌\nЕсли есть какие-то вопросы, не забудь заглянуть в <#1006514841529360474>.")
                embed_chat.set_image(url="https://images-ext-1.discordapp.net/external/wvE39B7oL9Y9zD-maOHvSw5VzySssiwKd7moi4dBS9Q/https/i.pinimg.com/originals/17/a1/f1/17a1f18ea42cdafce703fbb3bce60c7a.gif")
                
                if inter.channel.id == 997429823473455135:
                    if inter.component.custom_id == "verify_button":
                        await inter.send(content="Функция недоступна.", ephemeral=True)
                        return
                        
                        if verify_role in inter.author.roles:
                            if user_role in inter.author.roles:
                                if male_role not in inter.author.roles or female_role not in inter.author.roles:
                                    await inter.author.remove_roles(user_role, reason="Прохождение верификации")
                                    await inter.send(embed=gender_embed, view=gender_button, ephemeral=True)
                                    return
                                
                                await inter.send(content="**Верификация прошла успешно!**\nПриятного времяпровождения на нашем сервере!", ephemeral=True)
                                await inter.author.remove_roles(verify_role, reason="Прохождение верификации")
                                await channel_chat.send(content=inter.author.mention, embed=embed_chat)
                                return

                            if male_role in inter.author.roles or female_role in inter.author.roles:
                                if user_role not in inter.author.roles:
                                    await inter.send(content="**Верификация прошла успешно!**\nПриятного времяпровождения на нашем сервере!", ephemeral=True)
                                    await inter.author.add_roles(user_role, reason="Прохождение верификации")
                                    await inter.author.remove_roles(verify_role, reason="Прохождение верификации")
                                    await channel_chat.send(content=inter.author.mention, embed=embed_chat)
                                    return

                                await inter.send(content="**Верификация прошла успешно!**\nПриятного времяпровождения на нашем сервере!", ephemeral=True)
                                await inter.author.remove_roles(verify_role, reason="Прохождение верификации")
                                await channel_chat.send(content=inter.author.mention, embed=embed_chat)
                                return

                            await inter.send(embed=gender_embed, view=gender_button, ephemeral=True)
                            return

                        await inter.send(content="Вы уже верифицированы.", ephemeral=True)

                    if inter.component.custom_id == "male_button":
                        if verify_role in inter.author.roles:
                            await inter.send(content="**Верификация прошла успешно!**\nПриятного времяпровождения на нашем сервере!", ephemeral=True)
                            await inter.author.add_roles(male_role, reason="Прохождение верификации")
                            await inter.author.add_roles(user_role, reason="Прохождение верификации")
                            await inter.author.remove_roles(verify_role, reason="Прохождение верификации")
                            await channel_chat.send(content=inter.author.mention, embed=embed_chat)

                    if inter.component.custom_id == "female_button":
                        if verify_role in inter.author.roles:
                            await inter.send(content="**Верификация прошла успешно!**\nПриятного времяпровождения на нашем сервере!", ephemeral=True)
                            await inter.author.add_roles(female_role, reason="Прохождение верификации")
                            await inter.author.add_roles(user_role, reason="Прохождение верификации")
                            await inter.author.remove_roles(verify_role, reason="Прохождение верификации")
                            await channel_chat.send(content=inter.author.mention, embed=embed_chat)
                    
            if inter.guild == guild_mm:
                user_role = disnake.utils.get(inter.guild.roles, id=998684071829966997)

                if inter.channel.id == 999339946362019981:
                    if inter.component.custom_id == "verify_button":
                        if user_role in inter.author.roles:
                            await inter.send(content="Вы уже верифицированы.", ephemeral=True)
                            return

                        await inter.send(content="**Верификация прошла успешно!**\nПриятного времяпровождения на нашем сервере!", ephemeral=True)
                        await inter.author.add_roles(user_role, reason="Прохождение верификации")

def setup(bot):
    bot.add_cog(Verification(bot))
