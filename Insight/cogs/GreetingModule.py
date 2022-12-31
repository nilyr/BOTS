import disnake
import sqlite3
from disnake import ButtonStyle
from disnake.ext import commands, tasks
from disnake.ui import View, Button, Select


with sqlite3.connect("database (Insight).db") as db:
    cursor = db.cursor()

    class GreetingModule(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.command(name="welcome")
        async def welcometotheclub(self, ctx):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            guild_kp = self.bot.get_guild(387409949442965506)

            if perms_owner is not None or perms_dev is not None:
                if ctx.guild == guild_kp:
                    channel_welcome = self.bot.get_channel(1028721677657460879)
                    channel_profile = self.bot.get_channel(1028720959655518328)

                    new_videos_kopanda_role = disnake.utils.get(ctx.guild.roles, id=676013694861443093)
                    access_panda_city_kopanda_role = disnake.utils.get(ctx.guild.roles, id=582940305129472001)
                    free_games_kopanda_role = disnake.utils.get(ctx.guild.roles, id=692830850215182407)
                    roblox_news_and_items_kopanda_role = disnake.utils.get(ctx.guild.roles, id=786308011936710726)
                    competition_kopanda_role = disnake.utils.get(ctx.guild.roles, id=614343444986593290)
                    events_kopanda_role = disnake.utils.get(ctx.guild.roles, id=1004707957604352011)

                    welcome = disnake.Embed(
                        color=0x2f3136)
                    welcome.set_image(
                        url="https://sun9-east.userapi.com/sun9-76/s/v1/ig2/l53vOXP6H-STbuvKr9kHHKBn4uHTQJEWRXBKn06xV90LfofjIJnqKhjyw-Z-IucNUSfY_-JHUvPxKlF-2pabBKwC.jpg?size=1023x408&quality=95&type=album")

                    welcome1 = disnake.Embed(
                        color=0x2f3136,
                        title="Приветствую тебя, друг!",
                        description="Прежде чем начать общение с нашими участниками, рекомендуем ознакомиться с пунктами ниже, чтобы сервер стал вам понятнее и ближе.")
                    welcome1.add_field(name="Выбери раздел, нажав на него в меню выбора:", value="\n<:rules:885624936910168094> **Правила** - свод здешних правил.\n<:channel_text:885624937002434640> **Каналы** - информация о каналах сервер.\n<:roles:885624937015033916> **Роли** - информация о ролях сервера.\n<:boost_3:885624937090539591> **Награды за буст** - свод здешних правил нахождения.", inline=False)
                    welcome1.set_image(
                        url="https://cdn.discordapp.com/attachments/838848278858039336/1002270493749027006/linia.png")

                    navigation_menu = View()
                    navigation_menu.add_item(Select(placeholder="Выбери свой путь", custom_id="navigation_menu",
                    options = [disnake.SelectOption(emoji="<:rules:885624936910168094>", label="Правила сервера", value="server_rules"),
                                disnake.SelectOption(emoji="<:channel_text:885624937002434640>", label="Каналы сервера", value="server_channels"),
                                disnake.SelectOption(emoji="<:roles:885624937015033916>", label="Роли сервера", value="server_roles"),
                                disnake.SelectOption(emoji="<:members:885624936901787738>", label="Помощь по серверу", value="server_help"),
                                disnake.SelectOption(emoji="<:boost_3:885624937090539591>", label="Награды за буст", value="server_boost")]))

                    profile_roles = disnake.Embed(
                        color=0x2f3136,
                        description="<a:tochka_anim1:978740315676631092> Вы можете выбрать **любую роль** для получения уведомления о серверных оповещениях, для этого внизу есть кнопки.\n\n"
                        "💻 — нажми на кнопку с этим эмодзи, чтобы получать уведомления о новых видео.\n🐼 — нажми на кнопку с этим эмодзи, чтобы получить доступ к Панда городу.\n🎮 — нажми на кнопку с этим эмодзи, чтобы получать уведомления о новых бесплатных играх.\n<:roblox:993882533018218588> — нажми на кнопку с этим эмодзи, если хочешь получать уведомления о новостях и бесплатных вещах в роблоксе.\n🎉 — нажми на кнопку с эмодзи, чтобы открыть доступ к конкурсам.\n🎊 — нажми на кнопку с этим эмодзи, чтобы получать уведомления о предстоящих ивентах.\n\n"
                        "<a:tochka_anim1:978740315676631092> Эти роли можно снять, повторным нажатием.")
                    profile_roles.set_author(
                        name="Бесплатные роли")
                    profile_roles.set_footer(
                        text="[] - число людей у которых есть данная роль.")
                    profile_roles.set_image(
                        url="https://cdn.discordapp.com/attachments/838848278858039336/993880891371823156/uwp357160.gif")

                    color_selection = disnake.Embed(
                        color=0x2f3136,
                        description="<a:tochka_anim1:978740315676631092> Вы можете выбрать **любой цвет** вашего ника, для этого внизу есть панель (меню), где вы можете выбрать себе какой хотите цвет.\n\n"
                        "<a:tochka_anim1:978740315676631092> Вы не сможете выбрать сразу 2 цвета.\n"
                        "<a:tochka_anim1:978740315676631092> Эти роли можно снять, повторным нажатием.")
                    color_selection.set_author(
                        name="Смена цвета")
                    color_selection.set_image(
                        url="https://cdn.discordapp.com/attachments/838848278858039336/993492488780267670/cd0ac53c65a93a2ccfabb720e1dcb0fe.gif")

                    profile_roles_button = View()
                    profile_roles_button.add_item(
                        Button(
                            style=ButtonStyle.blurple,
                            emoji="💻",
                            label=f"[{len(new_videos_kopanda_role.members)}]",
                            custom_id="new_videos_kopanda_button"))
                    profile_roles_button.add_item(
                        Button(
                            style=ButtonStyle.blurple,
                            emoji="🐼",
                            label=f"[{len(access_panda_city_kopanda_role.members)}]",
                            custom_id="access_panda_city_kopanda_button"))
                    profile_roles_button.add_item(
                        Button(
                            style=ButtonStyle.blurple,
                            emoji="🎮",
                            label=f"[{len(free_games_kopanda_role.members)}]",
                            custom_id="free_games_kopanda_button"))
                    profile_roles_button.add_item(
                        Button(
                            style=ButtonStyle.blurple,
                            emoji="<:roblox:993882533018218588>",
                            label=f"[{len(roblox_news_and_items_kopanda_role.members)}]",
                            custom_id="roblox_news_and_items_kopanda_button"))
                    profile_roles_button.add_item(
                        Button(
                            style=ButtonStyle.blurple,
                            emoji="🎉",
                            label=f"[{len(competition_kopanda_role.members)}]",
                            custom_id="competition_kopanda_button"))
                    profile_roles_button.add_item(
                        Button(
                            style=ButtonStyle.blurple,
                            emoji="🎊",
                            label=f"[{len(events_kopanda_role.members)}]",
                            custom_id="events_kopanda_button"))

                    color_selection_menu = View()
                    color_selection_menu.add_item(Select(placeholder="Выберите цвет ника", custom_id="color_selection_menu",
                    options = [disnake.SelectOption(emoji="<a:No_Check:877264845366517770>", label="Не выбрано", value="default_option", default=True),
                                disnake.SelectOption(emoji="<:roles:885624937015033916>", label="Просмотр ролей", value="role_viewing_option"),
                                disnake.SelectOption(emoji="<:doge:1045669283847487521>", label="zxc", value="zxc_role_option"),
                                disnake.SelectOption(emoji="⚪", label="Белый", value="white_role_option"),
                                disnake.SelectOption(emoji="👀", label="Глазик", value="eye_role_option"),
                                disnake.SelectOption(emoji="⚔️", label="Акимов", value="akimov_role_option"),
                                disnake.SelectOption(emoji="🔴", label="Красный", value="red_role_option"),
                                disnake.SelectOption(emoji="<:blue:762194897246748694>", label="Синий", value="blue_role_option"),
                                disnake.SelectOption(emoji="<:pink:762194897590943764>", label="Розовый", value="pink_role_option"),
                                disnake.SelectOption(emoji="<:purple:762194897624629268>", label="Фиолетовый", value="purple_role_option"),
                                disnake.SelectOption(emoji="🟢", label="Лаймовый", value="lime_role_option"),
                                disnake.SelectOption(emoji="🟠", label="Оранжевый", value="orange_role_option"),
                                disnake.SelectOption(emoji="<:orangeyellow:762194897641537547>", label="Оранжево-жёлтый", value="orange_yellow_role_option"),
                                disnake.SelectOption(emoji="🟡", label="Жёлтый", value="yellow_role_option"),
                                disnake.SelectOption(emoji="🕵️", label="Невидимка", value="invisible_role_option"),
                                disnake.SelectOption(emoji="🔵", label="Бирюзовый", value="turquoise_role_option"),
                                disnake.SelectOption(emoji="<:nebesniy:762194897629085696>", label="Небесный", value="celestial_role_option"),
                                disnake.SelectOption(emoji="<:morskoy:762194897552801832>", label="Морской", value="marine_role_option"),
                                disnake.SelectOption(emoji="⚫", label="Чёрный", value="black_role_option"),
                                disnake.SelectOption(emoji="<:seriy:762219398177619968>", label="Серый", value="grey_role_option")]))

                    await ctx.message.delete()
                    await channel_welcome.send(embeds=[welcome, welcome1], view=navigation_menu)
                    await channel_profile.send(embed=profile_roles, view=profile_roles_button)
                    await channel_profile.send(embed=color_selection, view=color_selection_menu)
                    return

            await ctx.message.delete(delay=5)
            await ctx.reply(content="Права на использование есть только у разработчика бота.", delete_after=5)

        @commands.Cog.listener()
        async def on_ready(self):
            self.kopanda_role_user_counter.start()

        @tasks.loop(seconds=1, reconnect=True)
        async def kopanda_role_user_counter(self):
            guild_kp = self.bot.get_guild(387409949442965506)

            profile_message = 1045669493633990766
            channel_profile = self.bot.get_channel(1028720959655518328)
            channel_profile_message = await channel_profile.fetch_message(profile_message)

            new_videos_kopanda_role = disnake.utils.get(guild_kp.roles, id=676013694861443093)
            access_panda_city_kopanda_role = disnake.utils.get(guild_kp.roles, id=582940305129472001)
            free_games_kopanda_role = disnake.utils.get(guild_kp.roles, id=692830850215182407)
            roblox_news_and_items_kopanda_role = disnake.utils.get(guild_kp.roles, id=786308011936710726)
            competition_kopanda_role = disnake.utils.get(guild_kp.roles, id=614343444986593290)
            events_kopanda_role = disnake.utils.get(guild_kp.roles, id=1004707957604352011)

            profile_roles_button = View()
            profile_roles_button.add_item(
                Button(
                    style=ButtonStyle.blurple,
                    emoji="💻",
                    label=f"[{len(new_videos_kopanda_role.members)}]",
                    custom_id="new_videos_kopanda_button"))
            profile_roles_button.add_item(
                Button(
                    style=ButtonStyle.blurple,
                    emoji="🐼",
                    label=f"[{len(access_panda_city_kopanda_role.members)}]",
                    custom_id="access_panda_city_kopanda_button"))
            profile_roles_button.add_item(
                Button(
                    style=ButtonStyle.blurple,
                    emoji="🎮",
                    label=f"[{len(free_games_kopanda_role.members)}]",
                    custom_id="free_games_kopanda_button"))
            profile_roles_button.add_item(
                Button(
                    style=ButtonStyle.blurple,
                    emoji="<:roblox:993882533018218588>",
                    label=f"[{len(roblox_news_and_items_kopanda_role.members)}]",
                    custom_id="roblox_news_and_items_kopanda_button"))
            profile_roles_button.add_item(
                Button(
                    style=ButtonStyle.blurple,
                    emoji="🎉",
                    label=f"[{len(competition_kopanda_role.members)}]",
                    custom_id="competition_kopanda_button"))
            profile_roles_button.add_item(
                Button(
                    style=ButtonStyle.blurple,
                    emoji="🎊",
                    label=f"[{len(events_kopanda_role.members)}]",
                    custom_id="events_kopanda_button"))

            await channel_profile_message.edit(view=profile_roles_button)

        @commands.Cog.listener()
        async def on_button_click(self, inter):
            guild_kp = self.bot.get_guild(387409949442965506)

            if inter.guild == guild_kp:
                new_videos_kopanda_role = disnake.utils.get(inter.guild.roles, id=676013694861443093)
                access_panda_city_kopanda_role = disnake.utils.get(inter.guild.roles, id=582940305129472001)
                free_games_kopanda_role = disnake.utils.get(inter.guild.roles, id=692830850215182407)
                roblox_news_and_items_kopanda_role = disnake.utils.get(inter.guild.roles, id=786308011936710726)
                competition_kopanda_role = disnake.utils.get(inter.guild.roles, id=614343444986593290)
                events_kopanda_role = disnake.utils.get(inter.guild.roles, id=1004707957604352011)

                subscription_roles_button = View()
                subscription_roles_button.add_item(
                    Button(
                        style=ButtonStyle.blurple,
                        emoji="💻",
                        label=f"[{len(new_videos_kopanda_role.members)}]",
                        custom_id="new_videos_kopanda_button"))
                subscription_roles_button.add_item(
                    Button(
                        style=ButtonStyle.blurple,
                        emoji="🐼",
                        label=f"[{len(access_panda_city_kopanda_role.members)}]",
                        custom_id="access_panda_city_kopanda_button"))
                subscription_roles_button.add_item(
                    Button(
                        style=ButtonStyle.blurple,
                        emoji="🎮",
                        label=f"[{len(free_games_kopanda_role.members)}]",
                        custom_id="free_games_kopanda_button"))
                subscription_roles_button.add_item(
                    Button(
                        style=ButtonStyle.blurple,
                        emoji="<:roblox:993882533018218588>",
                        label=f"[{len(roblox_news_and_items_kopanda_role.members)}]",
                        custom_id="roblox_news_and_items_kopanda_button"))
                subscription_roles_button.add_item(
                    Button(
                        style=ButtonStyle.blurple,
                        emoji="🎉",
                        label=f"[{len(competition_kopanda_role.members)}]",
                        custom_id="competition_kopanda_button"))
                subscription_roles_button.add_item(
                    Button(
                        style=ButtonStyle.blurple,
                        emoji="🎊",
                        label=f"[{len(events_kopanda_role.members)}]",
                        custom_id="events_kopanda_button"))

                if inter.component.custom_id == "new_videos_kopanda_button":
                    if new_videos_kopanda_role in inter.author.roles:
                        await inter.send(content=f"Роль {new_videos_kopanda_role.mention} убрана.", ephemeral=True)
                        await inter.author.remove_roles(new_videos_kopanda_role)
                        return

                    await inter.send(content=f"Роль {new_videos_kopanda_role.mention} выдана.", ephemeral=True)
                    await inter.author.add_roles(new_videos_kopanda_role)

                if inter.component.custom_id == "access_panda_city_kopanda_button":
                    if access_panda_city_kopanda_role in inter.author.roles:
                        await inter.send(content=f"Роль {access_panda_city_kopanda_role.mention} убрана.", ephemeral=True)
                        await inter.author.remove_roles(access_panda_city_kopanda_role)
                        return

                    await inter.send(content=f"Роль {access_panda_city_kopanda_role.mention} выдана.", ephemeral=True)
                    await inter.author.add_roles(access_panda_city_kopanda_role)

                if inter.component.custom_id == "free_games_kopanda_button":
                    if free_games_kopanda_role in inter.author.roles:
                        await inter.send(content=f"Роль {free_games_kopanda_role.mention} убрана.", ephemeral=True)
                        await inter.author.remove_roles(free_games_kopanda_role)
                        return

                    await inter.send(content=f"Роль {free_games_kopanda_role.mention} выдана.", ephemeral=True)
                    await inter.author.add_roles(free_games_kopanda_role)

                if inter.component.custom_id == "roblox_news_and_items_kopanda_button":
                    if roblox_news_and_items_kopanda_role in inter.author.roles:
                        await inter.send(content=f"Роль {roblox_news_and_items_kopanda_role.mention} убрана.", ephemeral=True)
                        await inter.author.remove_roles(roblox_news_and_items_kopanda_role)
                        return

                    await inter.send(content=f"Роль {roblox_news_and_items_kopanda_role.mention} выдана.", ephemeral=True)
                    await inter.author.add_roles(roblox_news_and_items_kopanda_role)

                if inter.component.custom_id == "competition_kopanda_button":
                    if competition_kopanda_role in inter.author.roles:
                        await inter.send(content=f"Роль {competition_kopanda_role.mention} убрана.", ephemeral=True)
                        await inter.author.remove_roles(competition_kopanda_role)
                        return

                    await inter.send(content=f"Роль {competition_kopanda_role.mention} выдана.", ephemeral=True)
                    await inter.author.add_roles(competition_kopanda_role)

                if inter.component.custom_id == "events_kopanda_button":
                    if events_kopanda_role in inter.author.roles:
                        await inter.send(content=f"Роль {events_kopanda_role.mention} убрана.", ephemeral=True)
                        await inter.author.remove_roles(events_kopanda_role)
                        return

                    await inter.send(content=f"Роль {events_kopanda_role.mention} выдана.", ephemeral=True)
                    await inter.author.add_roles(events_kopanda_role)

        @commands.Cog.listener()
        async def on_dropdown(self, inter: disnake.MessageInteraction):
            guild_kp = self.bot.get_guild(387409949442965506)
                
            if inter.guild == guild_kp:
                administration_assistant_role = disnake.utils.get(inter.guild.roles, id=423159755117166592)
                moderator_role = disnake.utils.get(inter.guild.roles, id=593799068606660619)
                helper_role = disnake.utils.get(inter.guild.roles, id=485843253481177091)
                overseer_role = disnake.utils.get(inter.guild.roles, id=538725888276168735)
                overseer_isp_role = disnake.utils.get(inter.guild.roles, id=575666099408994316)
                bot_adjuster_role = disnake.utils.get(inter.guild.roles, id=582941723798274069)
                booster_role = disnake.utils.get(inter.guild.roles, id=592987207199883266)
                custom_color_role = disnake.utils.get(inter.guild.roles, id=761651266333442081)

                zxc_role = disnake.utils.get(inter.guild.roles, id=1024321978057887846)
                white_role = disnake.utils.get(inter.guild.roles, id=761910147001483266)
                eye_role = disnake.utils.get(inter.guild.roles, id=947837534287826985)
                akimov_role = disnake.utils.get(inter.guild.roles, id=825629696091881492)
                red_role = disnake.utils.get(inter.guild.roles, id=761910140458369034)
                blue_role = disnake.utils.get(inter.guild.roles, id=761910142110531614)
                pink_role = disnake.utils.get(inter.guild.roles, id=761910145855782932)
                purple_role = disnake.utils.get(inter.guild.roles, id=761910142831820810)
                lime_role = disnake.utils.get(inter.guild.roles, id=761910141208494100)
                orange_role = disnake.utils.get(inter.guild.roles, id=761910146536177664)
                orange_yellow_role = disnake.utils.get(inter.guild.roles, id=761910144334037003)
                yellow_role = disnake.utils.get(inter.guild.roles, id=761910143864406036)
                invisible_role = disnake.utils.get(inter.guild.roles, id=762208264938717184)
                turquoise_role = disnake.utils.get(inter.guild.roles, id=761910143570411552)
                celestial_role = disnake.utils.get(inter.guild.roles, id=761911672466047016)
                marine_role = disnake.utils.get(inter.guild.roles, id=761910145399521290)
                black_role = disnake.utils.get(inter.guild.roles, id=761911670750576640)
                grey_role = disnake.utils.get(inter.guild.roles, id=761911671433592852)

                if inter.component.custom_id == "navigation_menu":
                    if "server_rules" in inter.values:
                        rules_embed_url = disnake.Embed(
                            color=0x2f3136)
                        rules_embed_url.set_image(
                            url="https://sun9-west.userapi.com/sun9-72/s/v1/ig2/LcZpnG1aBFmMUC_SKxIQS-WtdNiR3Y1NPg2eoS6I1JWP5JTSIDKKkeXrGMeIEqTR0tW03Khxb3RySebNCd-7RtTF.jpg?size=1023x408&quality=95&type=album")

                        rules_embed = disnake.Embed(
                            color=0x2f3136, description="Правила сервера можно посмотреть в канале <#440721422025752577>.")

                        await inter.send(content="Идёт загрузка...", ephemeral=True)
                        msg = await inter.original_message()
                        await msg.edit(content=None, embeds=[rules_embed_url, rules_embed])

                    if "server_channels" in inter.values:
                        channel_embed_url = disnake.Embed(
                            color=0x2f3136)
                        channel_embed_url.set_image(
                            url="https://sun9-north.userapi.com/sun9-85/s/v1/ig2/ny5i6cQcy8exgD8pMSyuUBD9cCV4uPwEC6I746NNFNM4jsbtGujhwKNPFWxtkUOV-tUdWUnQzCt1Fn81hDG3Zo40.jpg?size=1023x408&quality=95&type=album")

                        channel_embed = disnake.Embed(
                            color=0x2f3136,
                            title="Каналы сервера",
                            description="> **Воу, ты здесь впервые?**\n> **Тебе стоит познакомиться с нами.**\n> **Уверен, тебе здесь понравится.**\n\n"
                        )
                        
                        channel_embed.add_field(name="╭───・Информация",
                            value="<#1028721677657460879> — навигация по серверу.\n"
                            "<#440721422025752577> — правила сервера.\n"
                            "<#617609750229549056> — новости сервера.",
                            inline=False)

                        channel_embed.add_field(name="╭───・Важное",
                            value="<#754631611445936208> — уведомления о обновлениях на сервере.\n"
                            "<#754247558628507689> - уведомления о новых бустах для сервера.\n"
                            "<#1028720959655518328> — канал, где можно взять различные роли.\n"
                            "<#738771385949749338> — обращения к персоналу и жалобы.\n"
                            "<#617612117847179275> — опросы среди участников сервера.\n"
                            "<#630440089889144852> - конкурсы сервера.\n"
                            "<#692822103296180305> - раздача бесплатных игр.\n"
                            "<#819888207926919179> - партнёры сервера.",
                            inline=False)

                        channel_embed.add_field(name="╭───・KoPanda",
                            value="<#569934570993221632> - уведомления о новых видео КоПанды.\n"
                            "<#559787110295404544> - арт-рисунки с КоПандой.",
                            inline=False)

                        channel_embed.add_field(name="╭───・Roblox",
                            value="<#617612385347305496> - новости роблокса.\n"
                            "<#558928639690014736> - коды для роблокса.\n"
                            "<#577486494298669066> - вип сервера для роблокса.",
                            inline=False)

                        channel_embed.add_field(name="╭───・Лента",
                            value="<#1028979168257507348> - всякие прикольные картинки не предназначенные для мемов.\n"
                            "<#1028979263120085022> - форум для общения между участниками.\n"
                            "<#1028979332649078785> - всяческие мемы от участников сервера.",
                            inline=False)

                        channel_embed.add_field(name="╭───・Общение",
                            value="<#538388815560179722> - чатик для общения.\n"
                            "<#878269944935088198> - трейды между участниками сервера.\n"
                            "<#745343637818310676> - поиск тиммейтов для совместной игры.\n"
                            "<#569210503071662080> - чат для флуда и команд.",
                            inline=False)

                        channel_embed.add_field(name="╭───・Блоги",
                            value="<#735144929050886185> - форма для открытия вашего блога.\n"
                            "<#735168854619062363> - информация о блогах.",
                            inline=False)

                        await inter.send(content="Идёт загрузка...", ephemeral=True)
                        msg = await inter.original_message()
                        await msg.edit(content=None, embeds=[channel_embed_url, channel_embed])

                    if "server_roles" in inter.values:
                        role_embed_url = disnake.Embed(
                            color=0x2f3136)
                        role_embed_url.set_image(
                            url="https://sun9-west.userapi.com/sun9-10/s/v1/ig2/IoCeSsnKKGbEQjYmwNM6_KuK27K5ZTbLDDuG9aCPtHilE8ntNt0Ut3QDVZ-oPfkE1DwWjlHBDN0A06BdUz4xphpN.jpg?size=1023x408&quality=95&type=album")

                        role_embed = disnake.Embed(
                            color=0x2f3136,
                            title="Администрация",
                            description="<@&387454972851257345> — Роль КоПанды.\n\n"
                            "<@&600258400978468874> — Даётся только доверенным людям, они занимаются настройкой сервера и самим сервером, самая высшая и главная роль на сервере.\n\n"
                            "<@&926155535391264809> — Человек, который занимается разработкой личного бота для сервера.\n\n"
                            "<@&927329713431646228> - Люди, которые контролируют порядок в модерации.")

                        role_embed1 = disnake.Embed(
                            color=0x2f3136,
                            title="Модерация",
                            description="<@&423159755117166592> — Модерация сервера, доказавшие, что на них можно положиться, занимаются персоналом и помогают администрации.\n\n"
                            "<@&593799068606660619> — Люди, имеющие эту роль контролируют порядок на сервере и помогают с сервером, но и участникам, ответственная роль, которую могут получить немногие.\n\n"
                            "<@&485843253481177091> — Поддерживают порядок на сервере и оказывают многочисленную помощь новым участникам.\n\n"
                            "<@&538725888276168735> — Люди, которые просматривают, что находится в чатах и голосовых каналах, при нарушении порядка наказывают, помогают новеньким.")

                        role_embed2 = disnake.Embed(
                            color=0x2f3136,
                            title="Уровневые",
                            description="<@&735111364552556626> — У вас есть все права ниже перечисленных ролей, и возможность добавить ещё одно своё эмодзи.\n\n"
                            "<@&689913499446542357> — Вы можете добавить своё эмодзи.\n\n"
                            "<@&612628020712308746> — Вы можете добавлять в общем чате к сообщениям реакции, менять свой никнейм, так же у вас появляется свой голосовой чат (временный).")

                        role_embed3 = disnake.Embed(
                            color=0x2f3136,
                            title="Лимитированные",
                            description="<@&707343932794863695> — Люди, которые провели время на сервере в лето 2020.\n\n"
                            "<@&683580393269624904> — Люди, отличившиеся по уровню, только 5 людей прошли в зимнем сезоне.\n\n"
                            "<@&639902318375993363> — Люди, которые были зимой на сервере во время нового года.\n\n"
                            "<@&635074316442009600> — Люди, которые были на сервере во время Хэллоуина.\n\n"
                            "<@&638439158594928651> — Лимитированная роль, можно было получить во время хеллоуина 2019, на сервере, после прохождения задания.\n\n"
                            "<@&573160416335757352> — Лимитная роль.")

                        role_embed4 = disnake.Embed(
                            color=0x2f3136,
                            title="Обычные",
                            description="<@&980887484579864596> — Личность, которая хочет обмануть вас при обмене/продаже чего либо.\n\n"
                            "<@&861684857700089888> — Человек, который поможет вам безопасно совершить трейд.\n\n"
                            "<@&758406928300245003> — Участник сервера, у которого сегодня проходит день рождения.\n\n"
                            "<@&593805486172930051> — Особенные люди на сервере, имеют уважение.\n\n"
                            "<@&617819165893459968> — Люди, которые имеют 30.000 подписчиков, взаимное партнёрство.\n\n"
                            "<@&594534426550075402> — Человек, который пробыл долгое время на сервере. `Требование:` быть на сервере 1 год и 6000 сообщений.\n\n"
                            "<@&617731413315158044> — Люди, которые помогают КоПанде в различных играх.\n\n"
                            "<@&499590684295036932> — От этих людей была большая поддержка в виде денежных средств.\n\n"
                            "<@&738007075803758623> — Роль для Пандочки от КоПанды.\n\n"
                            "<@&601042894194737162> — Выдаёт сам КоПанда.")

                        role_embed5 = disnake.Embed(
                            color=0x2f3136,
                            title="Прочие",
                            description="<@&589851189303050240> — Проводят розыгрыши для участников сервера.\n\n"
                            "<@&692830850215182407> — Узнаёт о новостях скидках и раздачи игр.\n\n"
                            "<@&676013694861443093> — Получают уведомления о новых видео КоПанды.\n\n"
                            "<@&614343444986593290> — Учавствуют в конкурсах сервера.\n\n"
                            "<@&582940305129472001> — Позволяет открыть экономический пусть дискорд сервера.\n\n"
                            "<@&1028711769599909959> — Люди, которые были наказаны за нарушение правил сервера. Не могут общаться в текстовых каналах.\n\n"
                            "<@&574291156431536132> — Люди, нарушившие правила сервера, и теперь не могут общаться в голосовых каналах.")

                        await inter.send(content="Идёт загрузка...", ephemeral=True)
                        msg = await inter.original_message()
                        await msg.edit(content=None, embeds=[role_embed_url, role_embed, role_embed1, role_embed2, role_embed3, role_embed4, role_embed5])

                    if "bots_option" in inter.values:
                        bot_embed = disnake.Embed(
                            color=0x2f3136)
                        bot_embed.add_field(name="Профиль пользователя",
                                            value="``+profile`` - отображает ваш профиль.\n"
                                            "``+user`` - отображает информацию о тебе.\n"
                                            "``+set-profile`` - настроить свой профиль.",
                                            inline=False)
                        bot_embed.add_field(name="Экономика",
                                            value="``+balance`` - узнать свой баланс.\n"
                                            "``+daily`` - забрать ежедневный бонус.\n"
                                            "``+deposit`` - вложить деньги в банк.\n"
                                            "``+leaderboard`` - голосовой, текстовый рейтинг участников.\n"
                                            "``+monthly`` - забрать ежемесячный бонус.\n"
                                            "``+pay`` - перевести валюту другому участнику.\n"
                                            "``+rob`` - ограбить участника.\n"
                                            "``+slots`` - сыграть в рулетку.\n"
                                            "``+shop`` - посетить магазин сервера.\n"
                                            "``+timely`` - забрать бонус.\n"
                                            "``+transfer`` - перевести валюту на другой сервер.\n"
                                            "``+weekly`` - забрать еженедельный бонус.\n"
                                            "``+withdraw`` - вывести деньги из банка.\n"
                                            "``+work`` - выйти на работу.",
                                            inline=False)
                        bot_embed.add_field(name="Любовные",
                                            value="``+marry @user`` — отправить запрос для заключения брака.\n"
                                            "``+divorce`` — развестись.",
                                            inline=False)
                        bot_embed.add_field(name="Пожелания",
                                            value="``/hi`` - поздороваться со всеми.\n"
                                            "``/bb`` - попрощаться со всеми.\n"
                                            "``/gm`` - пожелать доброго утра.\n"
                                            "``/gn`` - пожелать доброй ночи.",
                                            inline=False)

                        await inter.send(content="Идёт загрузка...", ephemeral=True)
                        msg = await inter.original_message()
                        await msg.edit(content=None, embed=bot_embed)
                
                if inter.component.custom_id == "color_selection_menu":
                    if "role_viewing_option" in inter.values:
                        role_viewing_embed = disnake.Embed(
                            color=0x2f3136,
                            description="\n```md\n# Доступ к функции имеют:\n```\n"
                            f"**`Администрация`**\n"
                            f"**`Модерация`**\n"
                            f"**{booster_role.mention}**\n"
                            f"**{custom_color_role.mention}**\n"

                            "\n```md\n# Цветный роли:\n```\n"
                            f"**{zxc_role.mention}** [{len(zxc_role.members)}]\n"
                            f"**{white_role.mention}** [{len(white_role.members)}]\n"
                            f"**{eye_role.mention}** [{len(eye_role.members)}]\n"
                            f"**{akimov_role.mention}** [{len(akimov_role.members)}]\n"
                            f"**{red_role.mention}** [{len(red_role.members)}]\n"
                            f"**{blue_role.mention}** [{len(blue_role.members)}]\n"
                            f"**{pink_role.mention}** [{len(pink_role.members)}]\n"
                            f"**{purple_role.mention}** [{len(purple_role.members)}]\n"
                            f"**{lime_role.mention}** [{len(lime_role.members)}]\n"
                            f"**{orange_role.mention}** [{len(orange_role.members)}]\n"
                            f"**{orange_yellow_role.mention}** [{len(orange_yellow_role.members)}]\n"
                            f"**{yellow_role.mention}** [{len(yellow_role.members)}]\n"
                            f"**`{invisible_role}`** [{len(invisible_role.members)}]\n"
                            f"**{turquoise_role.mention}** [{len(turquoise_role.members)}]\n"
                            f"**{celestial_role.mention}** [{len(celestial_role.members)}]\n"
                            f"**{marine_role.mention}** [{len(marine_role.members)}]\n"
                            f"**{black_role.mention}** [{len(black_role.members)}]\n"
                            f"**{grey_role.mention}** [{len(grey_role.members)}]")
                        role_viewing_embed.set_footer(
                            text="[] - число людей у которых есть данная роль.")

                        await inter.send(content="Идёт загрузка...", ephemeral=True)
                        msg = await inter.original_message()
                        await msg.edit(content=None, embed=role_viewing_embed)

                    if "zxc_role_option" in inter.values:
                        if inter.author.guild_permissions.administrator or administration_assistant_role in inter.author.roles or moderator_role in inter.author.roles or helper_role in inter.author.roles or overseer_role in inter.author.roles or overseer_isp_role in inter.author.roles or bot_adjuster_role in inter.author.roles or booster_role in inter.author.roles or custom_color_role in inter.author.roles:
                            await inter.response.defer()
                            
                            if zxc_role in inter.author.roles:
                                await inter.send(content=f"Роль {zxc_role.mention} убрана.", ephemeral=True)
                                await inter.author.remove_roles(zxc_role)
                                return

                            if white_role in inter.author.roles:
                                await inter.author.remove_roles(white_role)
                            if eye_role in inter.author.roles:
                                await inter.author.remove_roles(eye_role)
                            if akimov_role in inter.author.roles:
                                await inter.author.remove_roles(akimov_role)
                            if red_role in inter.author.roles:
                                await inter.author.remove_roles(red_role)
                            if blue_role in inter.author.roles:
                                await inter.author.remove_roles(blue_role)
                            if pink_role in inter.author.roles:
                                await inter.author.remove_roles(pink_role)
                            if purple_role in inter.author.roles:
                                await inter.author.remove_roles(purple_role)
                            if lime_role in inter.author.roles:
                                await inter.author.remove_roles(lime_role)
                            if orange_role in inter.author.roles:
                                await inter.author.remove_roles(orange_role)
                            if orange_yellow_role in inter.author.roles:
                                await inter.author.remove_roles(orange_yellow_role)
                            if yellow_role in inter.author.roles:
                                await inter.author.remove_roles(yellow_role)
                            if invisible_role in inter.author.roles:
                                await inter.author.remove_roles(invisible_role)
                            if turquoise_role in inter.author.roles:
                                await inter.author.remove_roles(turquoise_role)
                            if celestial_role in inter.author.roles:
                                await inter.author.remove_roles(celestial_role)
                            if marine_role in inter.author.roles:
                                await inter.author.remove_roles(marine_role)
                            if black_role in inter.author.roles:
                                await inter.author.remove_roles(black_role)
                            if grey_role in inter.author.roles:
                                await inter.author.remove_roles(grey_role)

                            await inter.send(content=f"Роль {zxc_role.mention} выдана.", ephemeral=True)
                            await inter.author.add_roles(zxc_role)
                            return

                        await inter.send(content="У вас нет доступа к данной функции.", ephemeral=True)

                    if "white_role_option" in inter.values:
                        if inter.author.guild_permissions.administrator or administration_assistant_role in inter.author.roles or moderator_role in inter.author.roles or helper_role in inter.author.roles or overseer_role in inter.author.roles or overseer_isp_role in inter.author.roles or bot_adjuster_role in inter.author.roles or booster_role in inter.author.roles or custom_color_role in inter.author.roles:
                            await inter.response.defer()

                            if white_role in inter.author.roles:
                                await inter.send(content=f"Роль {white_role.mention} убрана.", ephemeral=True)
                                await inter.author.remove_roles(white_role)
                                return

                            if zxc_role in inter.author.roles:
                                await inter.author.remove_roles(zxc_role)
                            if eye_role in inter.author.roles:
                                await inter.author.remove_roles(eye_role)
                            if akimov_role in inter.author.roles:
                                await inter.author.remove_roles(akimov_role)
                            if red_role in inter.author.roles:
                                await inter.author.remove_roles(red_role)
                            if blue_role in inter.author.roles:
                                await inter.author.remove_roles(blue_role)
                            if pink_role in inter.author.roles:
                                await inter.author.remove_roles(pink_role)
                            if purple_role in inter.author.roles:
                                await inter.author.remove_roles(purple_role)
                            if lime_role in inter.author.roles:
                                await inter.author.remove_roles(lime_role)
                            if orange_role in inter.author.roles:
                                await inter.author.remove_roles(orange_role)
                            if orange_yellow_role in inter.author.roles:
                                await inter.author.remove_roles(orange_yellow_role)
                            if yellow_role in inter.author.roles:
                                await inter.author.remove_roles(yellow_role)
                            if invisible_role in inter.author.roles:
                                await inter.author.remove_roles(invisible_role)
                            if turquoise_role in inter.author.roles:
                                await inter.author.remove_roles(turquoise_role)
                            if celestial_role in inter.author.roles:
                                await inter.author.remove_roles(celestial_role)
                            if marine_role in inter.author.roles:
                                await inter.author.remove_roles(marine_role)
                            if black_role in inter.author.roles:
                                await inter.author.remove_roles(black_role)
                            if grey_role in inter.author.roles:
                                await inter.author.remove_roles(grey_role)

                            await inter.send(content=f"Роль {white_role.mention} выдана.", ephemeral=True)
                            await inter.author.add_roles(white_role)
                            return

                        await inter.send(content="У вас нет доступа к данной функции.", ephemeral=True)

                    if "eye_role_option" in inter.values:
                        if inter.author.guild_permissions.administrator or administration_assistant_role in inter.author.roles or moderator_role in inter.author.roles or helper_role in inter.author.roles or overseer_role in inter.author.roles or overseer_isp_role in inter.author.roles or bot_adjuster_role in inter.author.roles or booster_role in inter.author.roles or custom_color_role in inter.author.roles:
                            await inter.response.defer()

                            if eye_role in inter.author.roles:
                                await inter.send(content=f"Роль {eye_role.mention} убрана.", ephemeral=True)
                                await inter.author.remove_roles(eye_role)
                                return

                            if zxc_role in inter.author.roles:
                                await inter.author.remove_roles(zxc_role)
                            if white_role in inter.author.roles:
                                await inter.author.remove_roles(white_role)
                            if akimov_role in inter.author.roles:
                                await inter.author.remove_roles(akimov_role)
                            if red_role in inter.author.roles:
                                await inter.author.remove_roles(red_role)
                            if blue_role in inter.author.roles:
                                await inter.author.remove_roles(blue_role)
                            if pink_role in inter.author.roles:
                                await inter.author.remove_roles(pink_role)
                            if purple_role in inter.author.roles:
                                await inter.author.remove_roles(purple_role)
                            if lime_role in inter.author.roles:
                                await inter.author.remove_roles(lime_role)
                            if orange_role in inter.author.roles:
                                await inter.author.remove_roles(orange_role)
                            if orange_yellow_role in inter.author.roles:
                                await inter.author.remove_roles(orange_yellow_role)
                            if yellow_role in inter.author.roles:
                                await inter.author.remove_roles(yellow_role)
                            if invisible_role in inter.author.roles:
                                await inter.author.remove_roles(invisible_role)
                            if turquoise_role in inter.author.roles:
                                await inter.author.remove_roles(turquoise_role)
                            if celestial_role in inter.author.roles:
                                await inter.author.remove_roles(celestial_role)
                            if marine_role in inter.author.roles:
                                await inter.author.remove_roles(marine_role)
                            if black_role in inter.author.roles:
                                await inter.author.remove_roles(black_role)
                            if grey_role in inter.author.roles:
                                await inter.author.remove_roles(grey_role)

                            await inter.send(content=f"Роль {eye_role.mention} выдана.", ephemeral=True)
                            await inter.author.add_roles(eye_role)
                            return
                        
                        await inter.send(content="У вас нет доступа к данной функции.", ephemeral=True)

                    if "akimov_role_option" in inter.values:
                        if inter.author.guild_permissions.administrator or administration_assistant_role in inter.author.roles or moderator_role in inter.author.roles or helper_role in inter.author.roles or overseer_role in inter.author.roles or overseer_isp_role in inter.author.roles or bot_adjuster_role in inter.author.roles or booster_role in inter.author.roles or custom_color_role in inter.author.roles:
                            await inter.response.defer()

                            if akimov_role in inter.author.roles:
                                await inter.send(content=f"Роль {eye_role.mention} убрана.", ephemeral=True)
                                await inter.author.remove_roles(akimov_role)
                                return

                            if zxc_role in inter.author.roles:
                                await inter.author.remove_roles(zxc_role)
                            if white_role in inter.author.roles:
                                await inter.author.remove_roles(white_role)
                            if eye_role in inter.author.roles:
                                await inter.author.remove_roles(eye_role)
                            if red_role in inter.author.roles:
                                await inter.author.remove_roles(red_role)
                            if blue_role in inter.author.roles:
                                await inter.author.remove_roles(blue_role)
                            if pink_role in inter.author.roles:
                                await inter.author.remove_roles(pink_role)
                            if purple_role in inter.author.roles:
                                await inter.author.remove_roles(purple_role)
                            if lime_role in inter.author.roles:
                                await inter.author.remove_roles(lime_role)
                            if orange_role in inter.author.roles:
                                await inter.author.remove_roles(orange_role)
                            if orange_yellow_role in inter.author.roles:
                                await inter.author.remove_roles(orange_yellow_role)
                            if yellow_role in inter.author.roles:
                                await inter.author.remove_roles(yellow_role)
                            if invisible_role in inter.author.roles:
                                await inter.author.remove_roles(invisible_role)
                            if turquoise_role in inter.author.roles:
                                await inter.author.remove_roles(turquoise_role)
                            if celestial_role in inter.author.roles:
                                await inter.author.remove_roles(celestial_role)
                            if marine_role in inter.author.roles:
                                await inter.author.remove_roles(marine_role)
                            if black_role in inter.author.roles:
                                await inter.author.remove_roles(black_role)
                            if grey_role in inter.author.roles:
                                await inter.author.remove_roles(grey_role)

                            await inter.send(content=f"Роль {akimov_role.mention} выдана.", ephemeral=True)
                            await inter.author.add_roles(akimov_role)
                            return

                        await inter.send(content="У вас нет доступа к данной функции.", ephemeral=True)

                    if "red_role_option" in inter.values:
                        if inter.author.guild_permissions.administrator or administration_assistant_role in inter.author.roles or moderator_role in inter.author.roles or helper_role in inter.author.roles or overseer_role in inter.author.roles or overseer_isp_role in inter.author.roles or bot_adjuster_role in inter.author.roles or booster_role in inter.author.roles or custom_color_role in inter.author.roles:
                            await inter.response.defer()

                            if red_role in inter.author.roles:
                                await inter.send(content=f"Роль {red_role.mention} убрана.", ephemeral=True)
                                await inter.author.remove_roles(red_role)
                                return

                            if zxc_role in inter.author.roles:
                                await inter.author.remove_roles(zxc_role)
                            if white_role in inter.author.roles:
                                await inter.author.remove_roles(white_role)
                            if eye_role in inter.author.roles:
                                await inter.author.remove_roles(eye_role)
                            if akimov_role in inter.author.roles:
                                await inter.author.remove_roles(akimov_role)
                            if blue_role in inter.author.roles:
                                await inter.author.remove_roles(blue_role)
                            if pink_role in inter.author.roles:
                                await inter.author.remove_roles(pink_role)
                            if purple_role in inter.author.roles:
                                await inter.author.remove_roles(purple_role)
                            if lime_role in inter.author.roles:
                                await inter.author.remove_roles(lime_role)
                            if orange_role in inter.author.roles:
                                await inter.author.remove_roles(orange_role)
                            if orange_yellow_role in inter.author.roles:
                                await inter.author.remove_roles(orange_yellow_role)
                            if yellow_role in inter.author.roles:
                                await inter.author.remove_roles(yellow_role)
                            if invisible_role in inter.author.roles:
                                await inter.author.remove_roles(invisible_role)
                            if turquoise_role in inter.author.roles:
                                await inter.author.remove_roles(turquoise_role)
                            if celestial_role in inter.author.roles:
                                await inter.author.remove_roles(celestial_role)
                            if marine_role in inter.author.roles:
                                await inter.author.remove_roles(marine_role)
                            if black_role in inter.author.roles:
                                await inter.author.remove_roles(black_role)
                            if grey_role in inter.author.roles:
                                await inter.author.remove_roles(grey_role)

                            await inter.send(content=f"Роль {red_role.mention} выдана.", ephemeral=True)
                            await inter.author.add_roles(red_role)
                            return
                        
                        await inter.send(content="У вас нет доступа к данной функции.", ephemeral=True)

                    if "blue_role_option" in inter.values:
                        if inter.author.guild_permissions.administrator or administration_assistant_role in inter.author.roles or moderator_role in inter.author.roles or helper_role in inter.author.roles or overseer_role in inter.author.roles or overseer_isp_role in inter.author.roles or bot_adjuster_role in inter.author.roles or booster_role in inter.author.roles or custom_color_role in inter.author.roles:
                            await inter.response.defer()

                            if blue_role in inter.author.roles:
                                await inter.send(content=f"Роль {blue_role.mention} убрана.", ephemeral=True)
                                await inter.author.remove_roles(blue_role)
                                return

                            if zxc_role in inter.author.roles:
                                await inter.author.remove_roles(zxc_role)
                            if white_role in inter.author.roles:
                                await inter.author.remove_roles(white_role)
                            if eye_role in inter.author.roles:
                                await inter.author.remove_roles(eye_role)
                            if akimov_role in inter.author.roles:
                                await inter.author.remove_roles(akimov_role)
                            if red_role in inter.author.roles:
                                await inter.author.remove_roles(red_role)
                            if pink_role in inter.author.roles:
                                await inter.author.remove_roles(pink_role)
                            if purple_role in inter.author.roles:
                                await inter.author.remove_roles(purple_role)
                            if lime_role in inter.author.roles:
                                await inter.author.remove_roles(lime_role)
                            if orange_role in inter.author.roles:
                                await inter.author.remove_roles(orange_role)
                            if orange_yellow_role in inter.author.roles:
                                await inter.author.remove_roles(orange_yellow_role)
                            if yellow_role in inter.author.roles:
                                await inter.author.remove_roles(yellow_role)
                            if invisible_role in inter.author.roles:
                                await inter.author.remove_roles(invisible_role)
                            if turquoise_role in inter.author.roles:
                                await inter.author.remove_roles(turquoise_role)
                            if celestial_role in inter.author.roles:
                                await inter.author.remove_roles(celestial_role)
                            if marine_role in inter.author.roles:
                                await inter.author.remove_roles(marine_role)
                            if black_role in inter.author.roles:
                                await inter.author.remove_roles(black_role)
                            if grey_role in inter.author.roles:
                                await inter.author.remove_roles(grey_role)

                            await inter.send(content=f"Роль {blue_role.mention} выдана.", ephemeral=True)
                            await inter.author.add_roles(blue_role)
                            return

                        await inter.send(content="У вас нет доступа к данной функции.", ephemeral=True)

                    if "pink_role_option" in inter.values:
                        if inter.author.guild_permissions.administrator or administration_assistant_role in inter.author.roles or moderator_role in inter.author.roles or helper_role in inter.author.roles or overseer_role in inter.author.roles or overseer_isp_role in inter.author.roles or bot_adjuster_role in inter.author.roles or booster_role in inter.author.roles or custom_color_role in inter.author.roles:
                            await inter.response.defer()

                            if pink_role in inter.author.roles:
                                await inter.send(content=f"Роль {pink_role.mention} убрана.", ephemeral=True)
                                await inter.author.remove_roles(pink_role)
                                return

                            if zxc_role in inter.author.roles:
                                await inter.author.remove_roles(zxc_role)
                            if white_role in inter.author.roles:
                                await inter.author.remove_roles(white_role)
                            if eye_role in inter.author.roles:
                                await inter.author.remove_roles(eye_role)
                            if akimov_role in inter.author.roles:
                                await inter.author.remove_roles(akimov_role)
                            if red_role in inter.author.roles:
                                await inter.author.remove_roles(red_role)
                            if blue_role in inter.author.roles:
                                await inter.author.remove_roles(blue_role)
                            if purple_role in inter.author.roles:
                                await inter.author.remove_roles(purple_role)
                            if lime_role in inter.author.roles:
                                await inter.author.remove_roles(lime_role)
                            if orange_role in inter.author.roles:
                                await inter.author.remove_roles(orange_role)
                            if orange_yellow_role in inter.author.roles:
                                await inter.author.remove_roles(orange_yellow_role)
                            if yellow_role in inter.author.roles:
                                await inter.author.remove_roles(yellow_role)
                            if invisible_role in inter.author.roles:
                                await inter.author.remove_roles(invisible_role)
                            if turquoise_role in inter.author.roles:
                                await inter.author.remove_roles(turquoise_role)
                            if celestial_role in inter.author.roles:
                                await inter.author.remove_roles(celestial_role)
                            if marine_role in inter.author.roles:
                                await inter.author.remove_roles(marine_role)
                            if black_role in inter.author.roles:
                                await inter.author.remove_roles(black_role)
                            if grey_role in inter.author.roles:
                                await inter.author.remove_roles(grey_role)

                            await inter.send(content=f"Роль {pink_role.mention} выдана.", ephemeral=True)
                            await inter.author.add_roles(pink_role)
                            return

                        await inter.send(content="У вас нет доступа к данной функции.", ephemeral=True)

                    if "purple_role_option" in inter.values:
                        if inter.author.guild_permissions.administrator or administration_assistant_role in inter.author.roles or moderator_role in inter.author.roles or helper_role in inter.author.roles or overseer_role in inter.author.roles or overseer_isp_role in inter.author.roles or bot_adjuster_role in inter.author.roles or booster_role in inter.author.roles or custom_color_role in inter.author.roles:
                            await inter.response.defer()
                            
                            if purple_role in inter.author.roles:
                                await inter.send(content=f"Роль {purple_role.mention} убрана.", ephemeral=True)
                                await inter.author.remove_roles(purple_role)
                                return

                            if zxc_role in inter.author.roles:
                                await inter.author.remove_roles(zxc_role)
                            if white_role in inter.author.roles:
                                await inter.author.remove_roles(white_role)
                            if eye_role in inter.author.roles:
                                await inter.author.remove_roles(eye_role)
                            if akimov_role in inter.author.roles:
                                await inter.author.remove_roles(akimov_role)
                            if red_role in inter.author.roles:
                                await inter.author.remove_roles(red_role)
                            if blue_role in inter.author.roles:
                                await inter.author.remove_roles(blue_role)
                            if pink_role in inter.author.roles:
                                await inter.author.remove_roles(pink_role)
                            if lime_role in inter.author.roles:
                                await inter.author.remove_roles(lime_role)
                            if orange_role in inter.author.roles:
                                await inter.author.remove_roles(orange_role)
                            if orange_yellow_role in inter.author.roles:
                                await inter.author.remove_roles(orange_yellow_role)
                            if yellow_role in inter.author.roles:
                                await inter.author.remove_roles(yellow_role)
                            if invisible_role in inter.author.roles:
                                await inter.author.remove_roles(invisible_role)
                            if turquoise_role in inter.author.roles:
                                await inter.author.remove_roles(turquoise_role)
                            if celestial_role in inter.author.roles:
                                await inter.author.remove_roles(celestial_role)
                            if marine_role in inter.author.roles:
                                await inter.author.remove_roles(marine_role)
                            if black_role in inter.author.roles:
                                await inter.author.remove_roles(black_role)
                            if grey_role in inter.author.roles:
                                await inter.author.remove_roles(grey_role)

                            await inter.send(content=f"Роль {purple_role.mention} выдана.", ephemeral=True)
                            await inter.author.add_roles(purple_role)
                            return
                        
                        await inter.send(content="У вас нет доступа к данной функции.", ephemeral=True)

                    if "lime_role_option" in inter.values:
                        if inter.author.guild_permissions.administrator or administration_assistant_role in inter.author.roles or moderator_role in inter.author.roles or helper_role in inter.author.roles or overseer_role in inter.author.roles or overseer_isp_role in inter.author.roles or bot_adjuster_role in inter.author.roles or booster_role in inter.author.roles or custom_color_role in inter.author.roles:
                            await inter.response.defer()

                            if lime_role in inter.author.roles:
                                await inter.send(content=f"Роль {lime_role.mention} убрана.", ephemeral=True)
                                await inter.author.remove_roles(lime_role)
                                return

                            if zxc_role in inter.author.roles:
                                await inter.author.remove_roles(zxc_role)
                            if white_role in inter.author.roles:
                                await inter.author.remove_roles(white_role)
                            if eye_role in inter.author.roles:
                                await inter.author.remove_roles(eye_role)
                            if akimov_role in inter.author.roles:
                                await inter.author.remove_roles(akimov_role)
                            if red_role in inter.author.roles:
                                await inter.author.remove_roles(red_role)
                            if blue_role in inter.author.roles:
                                await inter.author.remove_roles(blue_role)
                            if pink_role in inter.author.roles:
                                await inter.author.remove_roles(pink_role)
                            if purple_role in inter.author.roles:
                                await inter.author.remove_roles(purple_role)
                            if orange_role in inter.author.roles:
                                await inter.author.remove_roles(orange_role)
                            if orange_yellow_role in inter.author.roles:
                                await inter.author.remove_roles(orange_yellow_role)
                            if yellow_role in inter.author.roles:
                                await inter.author.remove_roles(yellow_role)
                            if invisible_role in inter.author.roles:
                                await inter.author.remove_roles(invisible_role)
                            if turquoise_role in inter.author.roles:
                                await inter.author.remove_roles(turquoise_role)
                            if celestial_role in inter.author.roles:
                                await inter.author.remove_roles(celestial_role)
                            if marine_role in inter.author.roles:
                                await inter.author.remove_roles(marine_role)
                            if black_role in inter.author.roles:
                                await inter.author.remove_roles(black_role)
                            if grey_role in inter.author.roles:
                                await inter.author.remove_roles(grey_role)

                            await inter.send(content=f"Роль {lime_role.mention} выдана.", ephemeral=True)
                            await inter.author.add_roles(lime_role)
                            return

                        await inter.send(content="У вас нет доступа к данной функции.", ephemeral=True)

                    if "orange_role_option" in inter.values:
                        if inter.author.guild_permissions.administrator or administration_assistant_role in inter.author.roles or moderator_role in inter.author.roles or helper_role in inter.author.roles or overseer_role in inter.author.roles or overseer_isp_role in inter.author.roles or bot_adjuster_role in inter.author.roles or booster_role in inter.author.roles or custom_color_role in inter.author.roles:
                            await inter.response.defer()

                            if orange_role in inter.author.roles:
                                await inter.send(content=f"Роль {orange_role.mention} убрана.", ephemeral=True)
                                await inter.author.remove_roles(orange_role)
                                return

                            if zxc_role in inter.author.roles:
                                await inter.author.remove_roles(zxc_role)
                            if white_role in inter.author.roles:
                                await inter.author.remove_roles(white_role)
                            if eye_role in inter.author.roles:
                                await inter.author.remove_roles(eye_role)
                            if akimov_role in inter.author.roles:
                                await inter.author.remove_roles(akimov_role)
                            if red_role in inter.author.roles:
                                await inter.author.remove_roles(red_role)
                            if blue_role in inter.author.roles:
                                await inter.author.remove_roles(blue_role)
                            if pink_role in inter.author.roles:
                                await inter.author.remove_roles(pink_role)
                            if purple_role in inter.author.roles:
                                await inter.author.remove_roles(purple_role)
                            if lime_role in inter.author.roles:
                                await inter.author.remove_roles(lime_role)
                            if orange_yellow_role in inter.author.roles:
                                await inter.author.remove_roles(orange_yellow_role)
                            if yellow_role in inter.author.roles:
                                await inter.author.remove_roles(yellow_role)
                            if invisible_role in inter.author.roles:
                                await inter.author.remove_roles(invisible_role)
                            if turquoise_role in inter.author.roles:
                                await inter.author.remove_roles(turquoise_role)
                            if celestial_role in inter.author.roles:
                                await inter.author.remove_roles(celestial_role)
                            if marine_role in inter.author.roles:
                                await inter.author.remove_roles(marine_role)
                            if black_role in inter.author.roles:
                                await inter.author.remove_roles(black_role)
                            if grey_role in inter.author.roles:
                                await inter.author.remove_roles(grey_role)

                            await inter.send(content=f"Роль {orange_role.mention} выдана.", ephemeral=True)
                            await inter.author.add_roles(orange_role)
                            return

                        await inter.send(content="У вас нет доступа к данной функции.", ephemeral=True)

                    if "orange_yellow_role_option" in inter.values:
                        if inter.author.guild_permissions.administrator or administration_assistant_role in inter.author.roles or moderator_role in inter.author.roles or helper_role in inter.author.roles or overseer_role in inter.author.roles or overseer_isp_role in inter.author.roles or bot_adjuster_role in inter.author.roles or booster_role in inter.author.roles or custom_color_role in inter.author.roles:
                            await inter.response.defer()

                            if orange_yellow_role in inter.author.roles:
                                await inter.send(content=f"Роль {orange_yellow_role.mention} убрана.", ephemeral=True)
                                await inter.author.remove_roles(orange_yellow_role)
                                return

                            if zxc_role in inter.author.roles:
                                await inter.author.remove_roles(zxc_role)
                            if white_role in inter.author.roles:
                                await inter.author.remove_roles(white_role)
                            if eye_role in inter.author.roles:
                                await inter.author.remove_roles(eye_role)
                            if akimov_role in inter.author.roles:
                                await inter.author.remove_roles(akimov_role)
                            if red_role in inter.author.roles:
                                await inter.author.remove_roles(red_role)
                            if blue_role in inter.author.roles:
                                await inter.author.remove_roles(blue_role)
                            if pink_role in inter.author.roles:
                                await inter.author.remove_roles(pink_role)
                            if purple_role in inter.author.roles:
                                await inter.author.remove_roles(purple_role)
                            if lime_role in inter.author.roles:
                                await inter.author.remove_roles(lime_role)
                            if orange_role in inter.author.roles:
                                await inter.author.remove_roles(orange_role)
                            if yellow_role in inter.author.roles:
                                await inter.author.remove_roles(yellow_role)
                            if invisible_role in inter.author.roles:
                                await inter.author.remove_roles(invisible_role)
                            if turquoise_role in inter.author.roles:
                                await inter.author.remove_roles(turquoise_role)
                            if celestial_role in inter.author.roles:
                                await inter.author.remove_roles(celestial_role)
                            if marine_role in inter.author.roles:
                                await inter.author.remove_roles(marine_role)
                            if black_role in inter.author.roles:
                                await inter.author.remove_roles(black_role)
                            if grey_role in inter.author.roles:
                                await inter.author.remove_roles(grey_role)

                            await inter.send(content=f"Роль {orange_yellow_role.mention} выдана.", ephemeral=True)
                            await inter.author.add_roles(orange_yellow_role)
                            return

                        await inter.send(content="У вас нет доступа к данной функции.", ephemeral=True)

                    if "yellow_role_option" in inter.values:
                        if inter.author.guild_permissions.administrator or administration_assistant_role in inter.author.roles or moderator_role in inter.author.roles or helper_role in inter.author.roles or overseer_role in inter.author.roles or overseer_isp_role in inter.author.roles or bot_adjuster_role in inter.author.roles or booster_role in inter.author.roles or custom_color_role in inter.author.roles:
                            await inter.response.defer()

                            if yellow_role in inter.author.roles:
                                await inter.send(content=f"Роль {yellow_role.mention} убрана.", ephemeral=True)
                                await inter.author.remove_roles(yellow_role)
                                return

                            if zxc_role in inter.author.roles:
                                await inter.author.remove_roles(zxc_role)
                            if white_role in inter.author.roles:
                                await inter.author.remove_roles(white_role)
                            if eye_role in inter.author.roles:
                                await inter.author.remove_roles(eye_role)
                            if akimov_role in inter.author.roles:
                                await inter.author.remove_roles(akimov_role)
                            if red_role in inter.author.roles:
                                await inter.author.remove_roles(red_role)
                            if blue_role in inter.author.roles:
                                await inter.author.remove_roles(blue_role)
                            if pink_role in inter.author.roles:
                                await inter.author.remove_roles(pink_role)
                            if purple_role in inter.author.roles:
                                await inter.author.remove_roles(purple_role)
                            if lime_role in inter.author.roles:
                                await inter.author.remove_roles(lime_role)
                            if orange_role in inter.author.roles:
                                await inter.author.remove_roles(orange_role)
                            if orange_yellow_role in inter.author.roles:
                                await inter.author.remove_roles(orange_yellow_role)
                            if invisible_role in inter.author.roles:
                                await inter.author.remove_roles(invisible_role)
                            if turquoise_role in inter.author.roles:
                                await inter.author.remove_roles(turquoise_role)
                            if celestial_role in inter.author.roles:
                                await inter.author.remove_roles(celestial_role)
                            if marine_role in inter.author.roles:
                                await inter.author.remove_roles(marine_role)
                            if black_role in inter.author.roles:
                                await inter.author.remove_roles(black_role)
                            if grey_role in inter.author.roles:
                                await inter.author.remove_roles(grey_role)

                            await inter.send(content=f"Роль {yellow_role.mention} выдана.", ephemeral=True)
                            await inter.author.add_roles(yellow_role)
                            return
                        
                        await inter.send(content="У вас нет доступа к данной функции.", ephemeral=True)

                    if "invisible_role_option" in inter.values:
                        if inter.author.guild_permissions.administrator or administration_assistant_role in inter.author.roles or moderator_role in inter.author.roles or helper_role in inter.author.roles or overseer_role in inter.author.roles or overseer_isp_role in inter.author.roles or bot_adjuster_role in inter.author.roles or booster_role in inter.author.roles or custom_color_role in inter.author.roles:
                            await inter.response.defer()

                            if invisible_role in inter.author.roles:
                                await inter.send(content=f"Роль {invisible_role.mention} убрана.", ephemeral=True)
                                await inter.author.remove_roles(invisible_role)
                                return

                            if zxc_role in inter.author.roles:
                                await inter.author.remove_roles(zxc_role)
                            if white_role in inter.author.roles:
                                await inter.author.remove_roles(white_role)
                            if eye_role in inter.author.roles:
                                await inter.author.remove_roles(eye_role)
                            if akimov_role in inter.author.roles:
                                await inter.author.remove_roles(akimov_role)
                            if red_role in inter.author.roles:
                                await inter.author.remove_roles(red_role)
                            if blue_role in inter.author.roles:
                                await inter.author.remove_roles(blue_role)
                            if pink_role in inter.author.roles:
                                await inter.author.remove_roles(pink_role)
                            if purple_role in inter.author.roles:
                                await inter.author.remove_roles(purple_role)
                            if lime_role in inter.author.roles:
                                await inter.author.remove_roles(lime_role)
                            if orange_role in inter.author.roles:
                                await inter.author.remove_roles(orange_role)
                            if orange_yellow_role in inter.author.roles:
                                await inter.author.remove_roles(orange_yellow_role)
                            if yellow_role in inter.author.roles:
                                await inter.author.remove_roles(yellow_role)
                            if turquoise_role in inter.author.roles:
                                await inter.author.remove_roles(turquoise_role)
                            if celestial_role in inter.author.roles:
                                await inter.author.remove_roles(celestial_role)
                            if marine_role in inter.author.roles:
                                await inter.author.remove_roles(marine_role)
                            if black_role in inter.author.roles:
                                await inter.author.remove_roles(black_role)
                            if grey_role in inter.author.roles:
                                await inter.author.remove_roles(grey_role)

                            await inter.send(content=f"Роль {invisible_role.mention} выдана.", ephemeral=True)
                            await inter.author.add_roles(invisible_role)
                            return

                        await inter.send(content="У вас нет доступа к данной функции.", ephemeral=True)

                    if "turquoise_role_option" in inter.values:
                        if inter.author.guild_permissions.administrator or administration_assistant_role in inter.author.roles or moderator_role in inter.author.roles or helper_role in inter.author.roles or overseer_role in inter.author.roles or overseer_isp_role in inter.author.roles or bot_adjuster_role in inter.author.roles or booster_role in inter.author.roles or custom_color_role in inter.author.roles:
                            await inter.response.defer()

                            if turquoise_role in inter.author.roles:
                                await inter.send(content=f"Роль {turquoise_role.mention} убрана.", ephemeral=True)
                                await inter.author.remove_roles(turquoise_role)
                                return

                            if zxc_role in inter.author.roles:
                                await inter.author.remove_roles(zxc_role)
                            if white_role in inter.author.roles:
                                await inter.author.remove_roles(white_role)
                            if eye_role in inter.author.roles:
                                await inter.author.remove_roles(eye_role)
                            if akimov_role in inter.author.roles:
                                await inter.author.remove_roles(akimov_role)
                            if red_role in inter.author.roles:
                                await inter.author.remove_roles(red_role)
                            if blue_role in inter.author.roles:
                                await inter.author.remove_roles(blue_role)
                            if pink_role in inter.author.roles:
                                await inter.author.remove_roles(pink_role)
                            if purple_role in inter.author.roles:
                                await inter.author.remove_roles(purple_role)
                            if lime_role in inter.author.roles:
                                await inter.author.remove_roles(lime_role)
                            if orange_role in inter.author.roles:
                                await inter.author.remove_roles(orange_role)
                            if orange_yellow_role in inter.author.roles:
                                await inter.author.remove_roles(orange_yellow_role)
                            if yellow_role in inter.author.roles:
                                await inter.author.remove_roles(yellow_role)
                            if invisible_role in inter.author.roles:
                                await inter.author.remove_roles(invisible_role)
                            if celestial_role in inter.author.roles:
                                await inter.author.remove_roles(celestial_role)
                            if marine_role in inter.author.roles:
                                await inter.author.remove_roles(marine_role)
                            if black_role in inter.author.roles:
                                await inter.author.remove_roles(black_role)
                            if grey_role in inter.author.roles:
                                await inter.author.remove_roles(grey_role)

                            await inter.send(content=f"Роль {turquoise_role.mention} выдана.", ephemeral=True)
                            await inter.author.add_roles(turquoise_role)
                            return

                        await inter.send(content="У вас нет доступа к данной функции.", ephemeral=True)

                    if "celestial_role_option" in inter.values:
                        if inter.author.guild_permissions.administrator or administration_assistant_role in inter.author.roles or moderator_role in inter.author.roles or helper_role in inter.author.roles or overseer_role in inter.author.roles or overseer_isp_role in inter.author.roles or bot_adjuster_role in inter.author.roles or booster_role in inter.author.roles or custom_color_role in inter.author.roles:
                            await inter.response.defer()

                            if celestial_role in inter.author.roles:
                                await inter.send(content=f"Роль {celestial_role.mention} убрана.", ephemeral=True)
                                await inter.author.remove_roles(celestial_role)
                                return

                            if zxc_role in inter.author.roles:
                                await inter.author.remove_roles(zxc_role)
                            if white_role in inter.author.roles:
                                await inter.author.remove_roles(white_role)
                            if eye_role in inter.author.roles:
                                await inter.author.remove_roles(eye_role)
                            if akimov_role in inter.author.roles:
                                await inter.author.remove_roles(akimov_role)
                            if red_role in inter.author.roles:
                                await inter.author.remove_roles(red_role)
                            if blue_role in inter.author.roles:
                                await inter.author.remove_roles(blue_role)
                            if pink_role in inter.author.roles:
                                await inter.author.remove_roles(pink_role)
                            if purple_role in inter.author.roles:
                                await inter.author.remove_roles(purple_role)
                            if lime_role in inter.author.roles:
                                await inter.author.remove_roles(lime_role)
                            if orange_role in inter.author.roles:
                                await inter.author.remove_roles(orange_role)
                            if orange_yellow_role in inter.author.roles:
                                await inter.author.remove_roles(orange_yellow_role)
                            if yellow_role in inter.author.roles:
                                await inter.author.remove_roles(yellow_role)
                            if invisible_role in inter.author.roles:
                                await inter.author.remove_roles(invisible_role)
                            if turquoise_role in inter.author.roles:
                                await inter.author.remove_roles(turquoise_role)
                            if marine_role in inter.author.roles:
                                await inter.author.remove_roles(marine_role)
                            if black_role in inter.author.roles:
                                await inter.author.remove_roles(black_role)
                            if grey_role in inter.author.roles:
                                await inter.author.remove_roles(grey_role)

                            await inter.send(content=f"Роль {celestial_role.mention} выдана.", ephemeral=True)
                            await inter.author.add_roles(celestial_role)
                            return

                        await inter.send(content="У вас нет доступа к данной функции.", ephemeral=True)

                    if "marine_role_option" in inter.values:
                        if inter.author.guild_permissions.administrator or administration_assistant_role in inter.author.roles or moderator_role in inter.author.roles or helper_role in inter.author.roles or overseer_role in inter.author.roles or overseer_isp_role in inter.author.roles or bot_adjuster_role in inter.author.roles or booster_role in inter.author.roles or custom_color_role in inter.author.roles:
                            await inter.response.defer()

                            if marine_role in inter.author.roles:
                                await inter.send(content=f"Роль {marine_role.mention} убрана.", ephemeral=True)
                                await inter.author.remove_roles(marine_role)
                                return

                            if zxc_role in inter.author.roles:
                                await inter.author.remove_roles(zxc_role)
                            if white_role in inter.author.roles:
                                await inter.author.remove_roles(white_role)
                            if eye_role in inter.author.roles:
                                await inter.author.remove_roles(eye_role)
                            if akimov_role in inter.author.roles:
                                await inter.author.remove_roles(akimov_role)
                            if red_role in inter.author.roles:
                                await inter.author.remove_roles(red_role)
                            if blue_role in inter.author.roles:
                                await inter.author.remove_roles(blue_role)
                            if pink_role in inter.author.roles:
                                await inter.author.remove_roles(pink_role)
                            if purple_role in inter.author.roles:
                                await inter.author.remove_roles(purple_role)
                            if lime_role in inter.author.roles:
                                await inter.author.remove_roles(lime_role)
                            if orange_role in inter.author.roles:
                                await inter.author.remove_roles(orange_role)
                            if orange_yellow_role in inter.author.roles:
                                await inter.author.remove_roles(orange_yellow_role)
                            if yellow_role in inter.author.roles:
                                await inter.author.remove_roles(yellow_role)
                            if invisible_role in inter.author.roles:
                                await inter.author.remove_roles(invisible_role)
                            if turquoise_role in inter.author.roles:
                                await inter.author.remove_roles(turquoise_role)
                            if celestial_role in inter.author.roles:
                                await inter.author.remove_roles(celestial_role)
                            if black_role in inter.author.roles:
                                await inter.author.remove_roles(black_role)
                            if grey_role in inter.author.roles:
                                await inter.author.remove_roles(grey_role)

                            await inter.send(content=f"Роль {marine_role.mention} выдана.", ephemeral=True)
                            await inter.author.add_roles(marine_role)
                            return

                        await inter.send(content="У вас нет доступа к данной функции.", ephemeral=True)

                    if "black_role_option" in inter.values:
                        if inter.author.guild_permissions.administrator or administration_assistant_role in inter.author.roles or moderator_role in inter.author.roles or helper_role in inter.author.roles or overseer_role in inter.author.roles or overseer_isp_role in inter.author.roles or bot_adjuster_role in inter.author.roles or booster_role in inter.author.roles or custom_color_role in inter.author.roles:
                            await inter.response.defer()

                            if black_role in inter.author.roles:
                                await inter.send(content=f"Роль {black_role.mention} убрана.", ephemeral=True)
                                await inter.author.remove_roles(black_role)
                                return

                            if zxc_role in inter.author.roles:
                                await inter.author.remove_roles(zxc_role)
                            if white_role in inter.author.roles:
                                await inter.author.remove_roles(white_role)
                            if eye_role in inter.author.roles:
                                await inter.author.remove_roles(eye_role)
                            if akimov_role in inter.author.roles:
                                await inter.author.remove_roles(akimov_role)
                            if red_role in inter.author.roles:
                                await inter.author.remove_roles(red_role)
                            if blue_role in inter.author.roles:
                                await inter.author.remove_roles(blue_role)
                            if pink_role in inter.author.roles:
                                await inter.author.remove_roles(pink_role)
                            if purple_role in inter.author.roles:
                                await inter.author.remove_roles(purple_role)
                            if lime_role in inter.author.roles:
                                await inter.author.remove_roles(lime_role)
                            if orange_role in inter.author.roles:
                                await inter.author.remove_roles(orange_role)
                            if orange_yellow_role in inter.author.roles:
                                await inter.author.remove_roles(orange_yellow_role)
                            if yellow_role in inter.author.roles:
                                await inter.author.remove_roles(yellow_role)
                            if invisible_role in inter.author.roles:
                                await inter.author.remove_roles(invisible_role)
                            if turquoise_role in inter.author.roles:
                                await inter.author.remove_roles(turquoise_role)
                            if celestial_role in inter.author.roles:
                                await inter.author.remove_roles(celestial_role)
                            if marine_role in inter.author.roles:
                                await inter.author.remove_roles(marine_role)
                            if grey_role in inter.author.roles:
                                await inter.author.remove_roles(grey_role)

                            await inter.send(content=f"Роль {black_role.mention} выдана.", ephemeral=True)
                            await inter.author.add_roles(black_role)
                            return

                        await inter.send(content="У вас нет доступа к данной функции.", ephemeral=True)

                    if "grey_role_option" in inter.values:
                        if inter.author.guild_permissions.administrator or administration_assistant_role in inter.author.roles or moderator_role in inter.author.roles or helper_role in inter.author.roles or overseer_role in inter.author.roles or overseer_isp_role in inter.author.roles or bot_adjuster_role in inter.author.roles or booster_role in inter.author.roles or custom_color_role in inter.author.roles:
                            await inter.response.defer()
                            
                            if grey_role in inter.author.roles:
                                await inter.send(content=f"Роль {grey_role.mention} убрана.", ephemeral=True)
                                await inter.author.remove_roles(grey_role)
                                return

                            if zxc_role in inter.author.roles:
                                await inter.author.remove_roles(zxc_role)
                            if white_role in inter.author.roles:
                                await inter.author.remove_roles(white_role)
                            if eye_role in inter.author.roles:
                                await inter.author.remove_roles(eye_role)
                            if akimov_role in inter.author.roles:
                                await inter.author.remove_roles(akimov_role)
                            if red_role in inter.author.roles:
                                await inter.author.remove_roles(red_role)
                            if blue_role in inter.author.roles:
                                await inter.author.remove_roles(blue_role)
                            if pink_role in inter.author.roles:
                                await inter.author.remove_roles(pink_role)
                            if purple_role in inter.author.roles:
                                await inter.author.remove_roles(purple_role)
                            if lime_role in inter.author.roles:
                                await inter.author.remove_roles(lime_role)
                            if orange_role in inter.author.roles:
                                await inter.author.remove_roles(orange_role)
                            if orange_yellow_role in inter.author.roles:
                                await inter.author.remove_roles(orange_yellow_role)
                            if yellow_role in inter.author.roles:
                                await inter.author.remove_roles(yellow_role)
                            if invisible_role in inter.author.roles:
                                await inter.author.remove_roles(invisible_role)
                            if turquoise_role in inter.author.roles:
                                await inter.author.remove_roles(turquoise_role)
                            if celestial_role in inter.author.roles:
                                await inter.author.remove_roles(celestial_role)
                            if marine_role in inter.author.roles:
                                await inter.author.remove_roles(marine_role)
                            if black_role in inter.author.roles:
                                await inter.author.remove_roles(black_role)

                            await inter.send(content=f"Роль {grey_role.mention} выдана.", ephemeral=True)
                            await inter.author.add_roles(grey_role)
                            return

                        await inter.send(content="У вас нет доступа к данной функции.", ephemeral=True)
                        

    # editr.set_image(url = "https://i.imgur.com/xsnzCnW.png"


def setup(bot):
    bot.add_cog(GreetingModule(bot))
