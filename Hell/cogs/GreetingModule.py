import disnake
import sqlite3
from disnake import ButtonStyle
from disnake.ext import commands
from disnake.ui import View, Button, Select

with sqlite3.connect("database (Hell).db") as db:
    cursor = db.cursor()

    class GreetingModule(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.command(name="welcome")
        async def welcometotheclub(self, ctx):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            guild_tc = self.bot.get_guild(614081676116754465)

            if perms_owner is not None or perms_dev is not None:
                if ctx.guild == guild_tc:
                    channel_welcome = self.bot.get_channel(986717719980286072)
                    channel_rules = self.bot.get_channel(986717826654023761)
                    channel_command = self.bot.get_channel(986718635630428212)
                    channel_donate_roles = self.bot.get_channel(986718704643477564)
                    channel_roles = self.bot.get_channel(986718724239294505)
                    channel_complaints = self.bot.get_channel(986720609419546665)

                    await ctx.message.delete()
                    welcome = disnake.Embed(
                        color=0x2f3136
                    )

                    welcome.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/979713112141885480/d431fec67f71983e.png")

                    welcome1 = disnake.Embed(
                        color=0x2f3136,
                        description="Обязательно прочти правила, нажав на **Правила сервера**"
                        "\nПолучи необходимые роли, нажав на **Роли сервера**"
                        "\nПознакомься с нашими ботами, нажав на **Команды**"
                    )

                    welcome1.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/979713111223312384/linia.png")

                    welcome_button = View()
                    welcome_button.add_item(
                        Button(
                            style=ButtonStyle.url,
                            label="Правила сервера",
                            url="https://discord.com/channels/798615610204356651/986717826654023761/986961455305871390"))
                    welcome_button.add_item(
                        Button(
                            style=ButtonStyle.url,
                            label="Роли сервера",
                            url="https://discord.com/channels/798615610204356651/986718724239294505/986961459076562964"))
                    welcome_button.add_item(
                        Button(
                            style=ButtonStyle.url,
                            label="Команды",
                            url="https://discord.com/channels/798615610204356651/986718635630428212/986961456274755656"))

                    welcome2 = disnake.Embed(
                        color=0x2f3136
                    )

                    welcome2.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/979713112364171294/a57285cc07ff1b99.png")

                    welcome3 = disnake.Embed(
                        color=0x2f3136,
                        description="> **Перед тобой небольшая навигация,**\n> **Тебе стоит побывать в каждом канале**\n"
                        "\n**<#986719163466805319>** — общая статистика серверов."
                    )

                    welcome3.add_field(
                        name="━━・Знакомство",
                        value="**<#986717719980286072>** — путеводитель по серверу.\n**<#986717826654023761>** — правила сервера.",
                        inline=False)
                    welcome3.add_field(name="━━・Информация", value="**<#986718614470164540>** — новости проекта.\n**<#986718635630428212>** — информация о командах сервера.\n**<#986718889297715210>** — изменения в составе проекта.\n**<#986718654647390288>** — оповещения о наборах в персонал сервера.", inline=False)
                    welcome3.add_field(
                        name="━━・Полезное",
                        value="**<#986718704643477564>** — получение роли за донат на сервере.\n**<#986718724239294505>** — получение кастомных ролей.\n**<#986718739829514250>** — техническая поддержка проекта в дискорде.",
                        inline=False)
                    welcome3.add_field(
                        name="━━・Прочее",
                        value="**<#986720609419546665>** — жалобы на персонал сервера.\n**<#986720634887344168>** — оповещения о новых бустерах.",
                        inline=False)
                    welcome3.add_field(
                        name="━━・Приватки",
                        value="**<#986716217958084658>** — создание приватной комнаты.",
                        inline=False)

                    welcome3.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/979713111223312384/linia.png")

                    welcome4 = disnake.Embed(
                        color=0x2f3136
                    )

                    welcome4.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/979713112594841630/5220af4f5389d1de.png")

                    welcome5 = disnake.Embed(
                        color=0x2f3136,
                        description="```md\n# Администрация Discord\n```\n**<@&986724535594270792>** **<@&986712810992062514>** — высшая администрация.\n**<@&986725465400172585>** — администрация.\n"
                        "\n```md\n# Администрация Сервера\n```\n**<@&986724535594270792>** **<@&986724218634899537>** — высшая администрация.\n**<@&986714300393594950>** — администрация.\n"
                        "\n```md\n# Служебные (Discord)\n```\n**<@&986725459591069697>** — кураторы модераторов.\n**<@&986725462539657287>** — старшая модерация.\n**<@&986725455052824646>** — младшая модерация.\n"
                        "\n```md\n# Служебные (Сервер)\n```\n**<@&986724234086723655>** — главная модерация.\n**<@&986724236435542086>** — старшая модерация.\n**<@&986724984393195540>** — основной состав модерации.\n**<@&986724987647950918>** — старший помощник.\n**<@&986724990592356483>** — основной состав помощников."
                    )

                    welcome5.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/979713111223312384/linia.png")

                    menu_roles = View()
                    menu_roles.add_item(Select(placeholder="Нажмите, чтобы посмотреть остальные роли", custom_id="roles_menu",
                    options = [disnake.SelectOption(emoji="<a:No_Check:877264845366517770>", label="Не выбрано", value="default_option", default=True),
                            disnake.SelectOption(emoji="<:roles:885624937015033916>", label="Остальные роли", value="roles_option")]))

                    welcome6 = disnake.Embed(
                        color=0x2f3136,
                        title="Полезные ресурсы",
                        description="Это все нужные и полезные ресурсы связанные с UnicMine'ом о которых вам нужно знать! Все слова кликабельны, или нажав Правой Кнопкой Мыши вы можете скопировать адрес ссылки."
                        "\n\nАйпи: mc.unicmine.ru\nCайт: [unicmine.ru](https://unicmine.ru)"
                    )

                    welcome6.add_field(
                        name="ВКонтакте",
                        value="<:vk:903327129905803314> [Основная Группа](https://vk.com/unicmine)\n<:vk:903327129905803314> [Группа Технической поддержки](https://vk.com/tech_unicmine)",
                        inline=False)

                    welcome6.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/979713111223312384/linia.png")

                    await channel_welcome.send(embeds=[welcome, welcome1], view=welcome_button)
                    await channel_welcome.send(embeds=[welcome2, welcome3, welcome4, welcome5], view=menu_roles)
                    await channel_welcome.send(embed=welcome6)
                    await channel_welcome.send("<:discord:877264842715701269> Ссылка для приглашения: https://discord.gg/BcVuFv7mrf")

                    rules_img = disnake.Embed(
                        color=0x2f3136
                    )

                    rules_img.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/979713111823114250/e28f7f0c392aa7eb.png")

                    rules_politics = disnake.Embed(
                        color=0x2f3136,
                        description="Наш сервер в первую очередь принимает [Условия предоставления сервисов Discord](https://discord.com/terms) и [Политику конфиденциальности компании Discord](https://discord.com/privacy).\n"
                        "\nСервер модерируется согласно [Правилам сообщества Discord](https://discord.com/guidelines) и [серверным правилам](https://lantoy.notion.site/UM-Discord-Rules-2a0349d6437f4ce99870c5e4bbcb9a41)."
                    )

                    rules_politics.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/985902838414708736/543af4badc673c4abb9999122b0e3983.gif")

                    await channel_rules.send(embeds=[rules_img, rules_politics])

                    command = disnake.Embed(
                        color=0x2f3136
                    )

                    command.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/979713111567237130/6cc6a8987a23f9d4.png")

                    command1 = disnake.Embed(
                        color=0x2f3136,
                        description="**```yaml\nОсновные:\n```**\n<:tochka:903713219032518746> `/uinfo` — информация о пользователе.\n<:tochka:903713219032518746> `/sinfo` — информация о сервере.\n<:tochka:903713219032518746> `/avatar` — посмотреть аватар пользователя.\n<:tochka:903713219032518746> `/ping` — показать пинг бота.\n<:tochka:903713219032518746> `/online` — информация об онлайне на сервере.\n<:tochka:903713219032518746> `/ponli` — информация об онлайне персонала Discord.\n<:tochka:903713219032518746> `/sos` — сообщить о нарушении.\n\n"

                        "**```yaml\nЭкономика:\n```**\n<:tochka:903713219032518746> `-bal` — посмотреть свой баланс.\n<:tochka:903713219032518746> `-top` — показать топ по конфеткам.\n<:tochka:903713219032518746> `-give` — передать пользователю конфетки.\n<:tochka:903713219032518746> `-dep` — положить деньги в банк.\n<:tochka:903713219032518746> `-with` — снять деньги с банка.\n<:tochka:903713219032518746> `-work` — поработать в шахте.\n<:tochka:903713219032518746> `-slut` — поработать в клубе проституткой.\n<:tochka:903713219032518746> `-crime` — ограбить известную компанию.\n"
                        "<:tochka:903713219032518746> `-buy` — купить предмет в магазине.\n"
                        "<:tochka:903713219032518746> `-shop` — посмотреть предметы в магазине.\n"
                        "<:tochka:903713219032518746> `-collect` — взять вознаграждение за роль."
                    )

                    command1.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/979713111223312384/linia.png")

                    command2 = disnake.Embed(
                        color=0x2f3136, description="**```yaml\nПриватки:\n```**\n<:tochka:903713219032518746> `/room name` — изменить название приватного канала.\n<:tochka:903713219032518746> `/room limit` — изменить лимит пользователей приватного канала.\n<:tochka:903713219032518746> `/room kick` — кикнуть пользователя из приватного канала.\n<:tochka:903713219032518746> `/room lock` — закрыть доступ к приватному каналу.\n<:tochka:903713219032518746> `/room unlock` — открыть доступ к приватному каналу.\n\n"
                        "**```yaml\nРейтинг:\n```**\n<:tochka:903713219032518746> `/rank` — посмотреть рейтинг пользователя.\n<:tochka:903713219032518746> `/leaders` — показать топ рейтинга пользователей.\n\n"
                        "**```yaml\nVK Музыка:\n```**\n<:tochka:903713219032518746> `-vp` — добавить в очередь трек.\n<:tochka:903713219032518746> `-vs` — остановить вопроизведение.\n<:tochka:903713219032518746> `-vn` — пропуск текущего трека.\n<:tochka:903713219032518746> `-vps` — поставить текущий трек на паузу.\n<:tochka:903713219032518746> `-vsearch` — искать трек в базе ВКонтакте.\n<:tochka:903713219032518746> `-vq` — просмотр очереди.\n<:tochka:903713219032518746> `-vl` — зацикливание.\n<:tochka:903713219032518746> `-vleave` — выход из канала.\n\n"
                        "**```yaml\nРеакции:\n```**\n<:tochka:903713219032518746> `/hug` — обнять пользователя.\n<:tochka:903713219032518746> `/kiss` — поцеловать пользователя.\n<:tochka:903713219032518746> `/punch` — ударить пользователя.\n<:tochka:903713219032518746> `/bite` — укусить пользователя.")

                    command2.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/979713111223312384/linia.png")

                    await channel_command.send(embeds=[command, command1, command2])

                    DonateRoles_button = View()
                    DonateRoles_button.add_item(
                        Button(
                            style=ButtonStyle.grey,
                            label="Подать заявку",
                            custom_id="DonateRoles_button"))

                    DonateRolesInfo = disnake.Embed(
                        color=0x2f3136,
                        title="Заявка на донат-роли",
                        description="Нажмите на кнопку, чтобы подать заявку на донат-роль")

                    DonateRolesInfo.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/913478422167183371/9d531539ede488a8f2eca3f34bc753ee_1.gif")
                    DonateRolesInfo.set_footer(
                        text="При создании заявки без причины вам может быть выдано наказание!")

                    await channel_donate_roles.send(embed=DonateRolesInfo, view=DonateRoles_button)

                    menu_gender = View()
                    menu_gender.add_item(Select(placeholder="Выберите свой гендер", custom_id="gender_menu",
                    options = [disnake.SelectOption(emoji="<a:No_Check:877264845366517770>", label="Не выбрано", value="default_option", default=True),
                                disnake.SelectOption(emoji="<:Male:985985761679642725>", label="Мальчик", value="male_option"),
                                disnake.SelectOption(emoji="<:Female:985985786476384268>", label="Девочка", value="female_option")]))

                    menu_color = View()
                    menu_color.add_item(Select(placeholder="Выберите цвет ника", custom_id="color_menu",
                    options = [disnake.SelectOption(emoji="<a:No_Check:877264845366517770>", label="Не выбрано", value="default_option", default=True),
                                disnake.SelectOption(label="Белый", value="white_role_option"),
                                disnake.SelectOption(label="Чёрный", value="black_role_option"),
                                disnake.SelectOption(label="Светло-серый", value="light_grey_role_option"),
                                disnake.SelectOption(label="Серый", value="grey_role_option"),
                                disnake.SelectOption(label="Фиолетовый", value="purple_role_option"),
                                disnake.SelectOption(label="Синий", value="blue_role_option"),
                                disnake.SelectOption(label="Голубой", value="light_blue_role_option"),
                                disnake.SelectOption(label="Зелёный", value="green_role_option"),
                                disnake.SelectOption(label="Мята", value="mint_role_option"),
                                disnake.SelectOption(label="Бордовый", value="burgundy_role_option"),
                                disnake.SelectOption(label="Красный", value="red_role_option"),
                                disnake.SelectOption(label="Оранжевый", value="orange_role_option"),
                                disnake.SelectOption(label="Жёлтый", value="yellow_role_option")]))

                    menu_alert = View()
                    menu_alert.add_item(Select(placeholder="Важные оповещения", custom_id="alert_menu",
                    options = [disnake.SelectOption(emoji="<a:No_Check:877264845366517770>", label="Не выбрано", value="default_option", default=True),
                                disnake.SelectOption(emoji="🔔", label="Новости сервера", value="news_discord_option"),
                                disnake.SelectOption(emoji="📣", label="Новости VK группы и Minecraft сервера", value="news_vk_option"),
                                disnake.SelectOption(emoji="📢", label="Обновления в персонале", value="news_personal_project_option")]))

                    alert_img = disnake.Embed(
                        color=0x2f3136
                    )

                    alert_img.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/979713110938124288/9015f6069dfc8bfa.png")

                    alert = disnake.Embed(
                        color=0x2f3136,
                        description="<:eto_che:985881657854808154>\n<a:tochka_anim1:978740315676631092> Выбирайте любую роль внизу под этим сообщением есть меню.\n"
                        "<a:tochka_anim1:978740315676631092> Вы не сможете выбрать сразу 2 гендера, также их снять."
                    )
                    alert.set_author(
                        name="Выбор гендерных ролей"
                    )
                    alert.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/979713111223312384/linia.png")

                    alert_1 = disnake.Embed(
                        color=0x2f3136,
                        description="<:eto_che:985881657854808154>\n<a:tochka_anim1:978740315676631092> Вы можете выбрать **любой цвет** вашего ника, для этого внизу есть панель (меню), где вы можете выбрать себе какой хотите цвет.\n"
                        "<a:tochka_anim1:978740315676631092> Вы не сможете выбрать сразу 2 цвета.\n"
                        "<a:tochka_anim1:978740315676631092> Эти роли можно снять, повторным нажатием."
                    )
                    alert_1.set_author(
                        name="Выбор цвета вашего ника"
                    )
                    alert_1.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/979713111223312384/linia.png")

                    alert_2 = disnake.Embed(
                        color=0x2f3136,
                        description="<:eto_che:985881657854808154>\n<a:tochka_anim1:978740315676631092> Вы можете выбрать **любую роль** для получения уведомления о серверных оповещениях, для этого внизу есть панель (меню).\n"
                        "<a:tochka_anim1:978740315676631092> Эти роли можно снять, повторным нажатием."
                    )
                    alert_2.set_author(
                        name="Уведомления о серверных оповещениях"
                    )
                    alert_2.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/979713111223312384/linia.png")

                    await channel_roles.send(embeds=[alert_img, alert], view=menu_gender)
                    await channel_roles.send(embed=alert_1, view=menu_color)
                    await channel_roles.send(embed=alert_2, view=menu_alert)

                    complaints = disnake.Embed(
                        color=0x2f3136,
                        title="Жалобы Discord сервера",
                        description="Здесь вы можете оставить жалобу на участника Discord сервера, либо на персонал Discord сервера.\n**Оставить жалобу можно только по форма подачи!**"
                    )

                    complaints.add_field(
                        name="Форма подачи:",
                        value="1. Discord нарушителя.\n2. Причина написания жалобы.\n3. Доказательства.\n4. Примерное время нарушения.",
                        inline=False)

                    await channel_complaints.send(embed=complaints)
                    return

            await ctx.message.delete(delay=5)
            await ctx.reply(content="Права на использование есть только у разработчика бота.", delete_after=5)

        @commands.Cog.listener()
        async def on_dropdown(self, inter: disnake.MessageInteraction):
            guild_tc = self.bot.get_guild(614081676116754465)

            if inter.guild == guild_tc:
                male_role = disnake.utils.get(inter.guild.roles, id=986714188019814420)
                female_role = disnake.utils.get(inter.guild.roles, id=986714191106814012)

                white_role = disnake.utils.get(inter.guild.roles, id=986959518560833546)
                black_role = disnake.utils.get(inter.guild.roles, id=986959523652718662)
                light_grey_role = disnake.utils.get(inter.guild.roles, id=986959528794947584)
                grey_role = disnake.utils.get(inter.guild.roles, id=986959533597401128)
                purple_role = disnake.utils.get(inter.guild.roles, id=986959531487690792)
                blue_role = disnake.utils.get(inter.guild.roles, id=986959541704990760)
                light_blue_role = disnake.utils.get(inter.guild.roles, id=986959538760613929)
                green_role = disnake.utils.get(inter.guild.roles, id=986959536302747659)
                mint_role = disnake.utils.get(inter.guild.roles, id=986959526135738418)
                burgundy_role = disnake.utils.get(inter.guild.roles, id=986959554011090986)
                red_role = disnake.utils.get(inter.guild.roles, id=986959521014493194)
                orange_role = disnake.utils.get(inter.guild.roles, id=986959551649697812)
                yellow_role = disnake.utils.get(inter.guild.roles, id=986959515939393537)

                news_discord_role = disnake.utils.get(inter.guild.roles, id=986731297156243496)
                news_vk_role = disnake.utils.get(inter.guild.roles, id=986731299278557206)
                news_personal_project_role = disnake.utils.get(inter.guild.roles, id=986731301769973821)

                if inter.component.custom_id == "gender_menu":
                    if "male_option" in inter.values:
                        if male_role in inter.author.roles:
                            await inter.send(content="Вы уже выбрали эту роль.", ephemeral=True)
                            return

                        if female_role in inter.author.roles:
                            await inter.author.remove_roles(female_role)

                        await inter.send(content=f"Роль {male_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(male_role)
                        return

                    if "female_option" in inter.values:
                        if female_role in inter.author.roles:
                            await inter.send(content="Вы уже выбрали эту роль.", ephemeral=True)
                            return

                        if male_role in inter.author.roles:
                            await inter.author.remove_roles(male_role)

                        await inter.send(content=f"Роль {female_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(female_role)
                        return

                if inter.component.custom_id == "color_menu":
                    if "white_role_option" in inter.values:
                        if white_role in inter.author.roles:
                            await inter.send(content=f"Роль {white_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(white_role)
                            return

                        if black_role in inter.author.roles:
                            await inter.author.remove_roles(black_role)
                        if light_grey_role in inter.author.roles:
                            await inter.author.remove_roles(light_grey_role)
                        if grey_role in inter.author.roles:
                            await inter.author.remove_roles(grey_role)
                        if purple_role in inter.author.roles:
                            await inter.author.remove_roles(purple_role)
                        if blue_role in inter.author.roles:
                            await inter.author.remove_roles(blue_role)
                        if light_blue_role in inter.author.roles:
                            await inter.author.remove_roles(light_blue_role)
                        if green_role in inter.author.roles:
                            await inter.author.remove_roles(green_role)
                        if mint_role in inter.author.roles:
                            await inter.author.remove_roles(mint_role)
                        if burgundy_role in inter.author.roles:
                            await inter.author.remove_roles(burgundy_role)
                        if red_role in inter.author.roles:
                            await inter.author.remove_roles(red_role)
                        if orange_role in inter.author.roles:
                            await inter.author.remove_roles(orange_role)
                        if yellow_role in inter.author.roles:
                            await inter.author.remove_roles(yellow_role)

                        await inter.send(content=f"Роль {white_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(white_role)

                    if "black_role_option" in inter.values:
                        if black_role in inter.author.roles:
                            await inter.send(content=f"Роль {black_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(black_role)
                            return

                        if white_role in inter.author.roles:
                            await inter.author.remove_roles(white_role)
                        if light_grey_role in inter.author.roles:
                            await inter.author.remove_roles(light_grey_role)
                        if grey_role in inter.author.roles:
                            await inter.author.remove_roles(grey_role)
                        if purple_role in inter.author.roles:
                            await inter.author.remove_roles(purple_role)
                        if blue_role in inter.author.roles:
                            await inter.author.remove_roles(blue_role)
                        if light_blue_role in inter.author.roles:
                            await inter.author.remove_roles(light_blue_role)
                        if green_role in inter.author.roles:
                            await inter.author.remove_roles(green_role)
                        if mint_role in inter.author.roles:
                            await inter.author.remove_roles(mint_role)
                        if burgundy_role in inter.author.roles:
                            await inter.author.remove_roles(burgundy_role)
                        if red_role in inter.author.roles:
                            await inter.author.remove_roles(red_role)
                        if orange_role in inter.author.roles:
                            await inter.author.remove_roles(orange_role)
                        if yellow_role in inter.author.roles:
                            await inter.author.remove_roles(yellow_role)

                        await inter.send(content=f"Роль {black_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(black_role)

                    if "light_grey_role_option" in inter.values:
                        if light_grey_role in inter.author.roles:
                            await inter.send(content=f"Роль {light_grey_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(light_grey_role)
                            return

                        if white_role in inter.author.roles:
                            await inter.author.remove_roles(white_role)
                        if black_role in inter.author.roles:
                            await inter.author.remove_roles(black_role)
                        if grey_role in inter.author.roles:
                            await inter.author.remove_roles(grey_role)
                        if purple_role in inter.author.roles:
                            await inter.author.remove_roles(purple_role)
                        if blue_role in inter.author.roles:
                            await inter.author.remove_roles(blue_role)
                        if light_blue_role in inter.author.roles:
                            await inter.author.remove_roles(light_blue_role)
                        if green_role in inter.author.roles:
                            await inter.author.remove_roles(green_role)
                        if mint_role in inter.author.roles:
                            await inter.author.remove_roles(mint_role)
                        if burgundy_role in inter.author.roles:
                            await inter.author.remove_roles(burgundy_role)
                        if red_role in inter.author.roles:
                            await inter.author.remove_roles(red_role)
                        if orange_role in inter.author.roles:
                            await inter.author.remove_roles(orange_role)
                        if yellow_role in inter.author.roles:
                            await inter.author.remove_roles(yellow_role)

                        await inter.send(content=f"Роль {light_grey_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(light_grey_role)

                    if "grey_role_option" in inter.values:
                        if grey_role in inter.author.roles:
                            await inter.send(content=f"Роль {grey_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(grey_role)
                            return

                        if white_role in inter.author.roles:
                            await inter.author.remove_roles(white_role)
                        if black_role in inter.author.roles:
                            await inter.author.remove_roles(black_role)
                        if light_grey_role in inter.author.roles:
                            await inter.author.remove_roles(light_grey_role)
                        if purple_role in inter.author.roles:
                            await inter.author.remove_roles(purple_role)
                        if blue_role in inter.author.roles:
                            await inter.author.remove_roles(blue_role)
                        if light_blue_role in inter.author.roles:
                            await inter.author.remove_roles(light_blue_role)
                        if green_role in inter.author.roles:
                            await inter.author.remove_roles(green_role)
                        if mint_role in inter.author.roles:
                            await inter.author.remove_roles(mint_role)
                        if burgundy_role in inter.author.roles:
                            await inter.author.remove_roles(burgundy_role)
                        if red_role in inter.author.roles:
                            await inter.author.remove_roles(red_role)
                        if orange_role in inter.author.roles:
                            await inter.author.remove_roles(orange_role)
                        if yellow_role in inter.author.roles:
                            await inter.author.remove_roles(yellow_role)

                        await inter.send(content=f"Роль {grey_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(grey_role)

                    if "purple_role_option" in inter.values:
                        if purple_role in inter.author.roles:
                            await inter.send(content=f"Роль {purple_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(purple_role)
                            return

                        if white_role in inter.author.roles:
                            await inter.author.remove_roles(white_role)
                        if black_role in inter.author.roles:
                            await inter.author.remove_roles(black_role)
                        if light_grey_role in inter.author.roles:
                            await inter.author.remove_roles(light_grey_role)
                        if grey_role in inter.author.roles:
                            await inter.author.remove_roles(grey_role)
                        if blue_role in inter.author.roles:
                            await inter.author.remove_roles(blue_role)
                        if light_blue_role in inter.author.roles:
                            await inter.author.remove_roles(light_blue_role)
                        if green_role in inter.author.roles:
                            await inter.author.remove_roles(green_role)
                        if mint_role in inter.author.roles:
                            await inter.author.remove_roles(mint_role)
                        if burgundy_role in inter.author.roles:
                            await inter.author.remove_roles(burgundy_role)
                        if red_role in inter.author.roles:
                            await inter.author.remove_roles(red_role)
                        if orange_role in inter.author.roles:
                            await inter.author.remove_roles(orange_role)
                        if yellow_role in inter.author.roles:
                            await inter.author.remove_roles(yellow_role)

                        await inter.send(content=f"Роль {purple_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(purple_role)

                    if "blue_role_option" in inter.values:
                        if blue_role in inter.author.roles:
                            await inter.send(content=f"Роль {blue_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(blue_role)
                            return

                        if white_role in inter.author.roles:
                            await inter.author.remove_roles(white_role)
                        if black_role in inter.author.roles:
                            await inter.author.remove_roles(black_role)
                        if light_grey_role in inter.author.roles:
                            await inter.author.remove_roles(light_grey_role)
                        if grey_role in inter.author.roles:
                            await inter.author.remove_roles(grey_role)
                        if purple_role in inter.author.roles:
                            await inter.author.remove_roles(purple_role)
                        if light_blue_role in inter.author.roles:
                            await inter.author.remove_roles(light_blue_role)
                        if green_role in inter.author.roles:
                            await inter.author.remove_roles(green_role)
                        if mint_role in inter.author.roles:
                            await inter.author.remove_roles(mint_role)
                        if burgundy_role in inter.author.roles:
                            await inter.author.remove_roles(burgundy_role)
                        if red_role in inter.author.roles:
                            await inter.author.remove_roles(red_role)
                        if orange_role in inter.author.roles:
                            await inter.author.remove_roles(orange_role)
                        if yellow_role in inter.author.roles:
                            await inter.author.remove_roles(yellow_role)

                        await inter.send(content=f"Роль {blue_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(blue_role)

                    if "light_blue_role_option" in inter.values:
                        if light_blue_role in inter.author.roles:
                            await inter.send(content=f"Роль {light_blue_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(light_blue_role)
                            return

                        if white_role in inter.author.roles:
                            await inter.author.remove_roles(white_role)
                        if black_role in inter.author.roles:
                            await inter.author.remove_roles(black_role)
                        if light_grey_role in inter.author.roles:
                            await inter.author.remove_roles(light_grey_role)
                        if grey_role in inter.author.roles:
                            await inter.author.remove_roles(grey_role)
                        if purple_role in inter.author.roles:
                            await inter.author.remove_roles(purple_role)
                        if blue_role in inter.author.roles:
                            await inter.author.remove_roles(blue_role)
                        if green_role in inter.author.roles:
                            await inter.author.remove_roles(green_role)
                        if mint_role in inter.author.roles:
                            await inter.author.remove_roles(mint_role)
                        if burgundy_role in inter.author.roles:
                            await inter.author.remove_roles(burgundy_role)
                        if red_role in inter.author.roles:
                            await inter.author.remove_roles(red_role)
                        if orange_role in inter.author.roles:
                            await inter.author.remove_roles(orange_role)
                        if yellow_role in inter.author.roles:
                            await inter.author.remove_roles(yellow_role)

                        await inter.send(content=f"Роль {light_blue_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(light_blue_role)

                    if "green_role_option" in inter.values:
                        if green_role in inter.author.roles:
                            await inter.send(content=f"Роль {green_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(green_role)
                            return

                        if white_role in inter.author.roles:
                            await inter.author.remove_roles(white_role)
                        if black_role in inter.author.roles:
                            await inter.author.remove_roles(black_role)
                        if light_grey_role in inter.author.roles:
                            await inter.author.remove_roles(light_grey_role)
                        if grey_role in inter.author.roles:
                            await inter.author.remove_roles(grey_role)
                        if purple_role in inter.author.roles:
                            await inter.author.remove_roles(purple_role)
                        if blue_role in inter.author.roles:
                            await inter.author.remove_roles(blue_role)
                        if light_blue_role in inter.author.roles:
                            await inter.author.remove_roles(light_blue_role)
                        if mint_role in inter.author.roles:
                            await inter.author.remove_roles(mint_role)
                        if burgundy_role in inter.author.roles:
                            await inter.author.remove_roles(burgundy_role)
                        if red_role in inter.author.roles:
                            await inter.author.remove_roles(red_role)
                        if orange_role in inter.author.roles:
                            await inter.author.remove_roles(orange_role)
                        if yellow_role in inter.author.roles:
                            await inter.author.remove_roles(yellow_role)

                        await inter.send(content=f"Роль {green_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(green_role)

                    if "mint_role_option" in inter.values:
                        if mint_role in inter.author.roles:
                            await inter.send(content=f"Роль {mint_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(mint_role)
                            return

                        if white_role in inter.author.roles:
                            await inter.author.remove_roles(white_role)
                        if black_role in inter.author.roles:
                            await inter.author.remove_roles(black_role)
                        if light_grey_role in inter.author.roles:
                            await inter.author.remove_roles(light_grey_role)
                        if grey_role in inter.author.roles:
                            await inter.author.remove_roles(grey_role)
                        if purple_role in inter.author.roles:
                            await inter.author.remove_roles(purple_role)
                        if blue_role in inter.author.roles:
                            await inter.author.remove_roles(blue_role)
                        if light_blue_role in inter.author.roles:
                            await inter.author.remove_roles(light_blue_role)
                        if green_role in inter.author.roles:
                            await inter.author.remove_roles(green_role)
                        if burgundy_role in inter.author.roles:
                            await inter.author.remove_roles(burgundy_role)
                        if red_role in inter.author.roles:
                            await inter.author.remove_roles(red_role)
                        if orange_role in inter.author.roles:
                            await inter.author.remove_roles(orange_role)
                        if yellow_role in inter.author.roles:
                            await inter.author.remove_roles(yellow_role)

                        await inter.send(content=f"Роль {mint_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(mint_role)

                    if "burgundy_role_option" in inter.values:
                        if burgundy_role in inter.author.roles:
                            await inter.send(content=f"Роль {burgundy_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(burgundy_role)
                            return

                        if white_role in inter.author.roles:
                            await inter.author.remove_roles(white_role)
                        if black_role in inter.author.roles:
                            await inter.author.remove_roles(black_role)
                        if light_grey_role in inter.author.roles:
                            await inter.author.remove_roles(light_grey_role)
                        if grey_role in inter.author.roles:
                            await inter.author.remove_roles(grey_role)
                        if purple_role in inter.author.roles:
                            await inter.author.remove_roles(purple_role)
                        if blue_role in inter.author.roles:
                            await inter.author.remove_roles(blue_role)
                        if light_blue_role in inter.author.roles:
                            await inter.author.remove_roles(light_blue_role)
                        if green_role in inter.author.roles:
                            await inter.author.remove_roles(green_role)
                        if mint_role in inter.author.roles:
                            await inter.author.remove_roles(mint_role)
                        if red_role in inter.author.roles:
                            await inter.author.remove_roles(red_role)
                        if orange_role in inter.author.roles:
                            await inter.author.remove_roles(orange_role)
                        if yellow_role in inter.author.roles:
                            await inter.author.remove_roles(yellow_role)

                        await inter.send(content=f"Роль {burgundy_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(burgundy_role)

                    if "red_role_option" in inter.values:
                        if red_role in inter.author.roles:
                            await inter.send(content=f"Роль {red_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(red_role)
                            return

                        if white_role in inter.author.roles:
                            await inter.author.remove_roles(white_role)
                        if black_role in inter.author.roles:
                            await inter.author.remove_roles(black_role)
                        if light_grey_role in inter.author.roles:
                            await inter.author.remove_roles(light_grey_role)
                        if grey_role in inter.author.roles:
                            await inter.author.remove_roles(grey_role)
                        if purple_role in inter.author.roles:
                            await inter.author.remove_roles(purple_role)
                        if blue_role in inter.author.roles:
                            await inter.author.remove_roles(blue_role)
                        if light_blue_role in inter.author.roles:
                            await inter.author.remove_roles(light_blue_role)
                        if green_role in inter.author.roles:
                            await inter.author.remove_roles(green_role)
                        if mint_role in inter.author.roles:
                            await inter.author.remove_roles(mint_role)
                        if burgundy_role in inter.author.roles:
                            await inter.author.remove_roles(burgundy_role)
                        if orange_role in inter.author.roles:
                            await inter.author.remove_roles(orange_role)
                        if yellow_role in inter.author.roles:
                            await inter.author.remove_roles(yellow_role)

                        await inter.send(content=f"Роль {red_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(red_role)

                    if "orange_role_option" in inter.values:
                        if orange_role in inter.author.roles:
                            await inter.send(content=f"Роль {orange_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(orange_role)
                            return

                        if white_role in inter.author.roles:
                            await inter.author.remove_roles(white_role)
                        if black_role in inter.author.roles:
                            await inter.author.remove_roles(black_role)
                        if light_grey_role in inter.author.roles:
                            await inter.author.remove_roles(light_grey_role)
                        if grey_role in inter.author.roles:
                            await inter.author.remove_roles(grey_role)
                        if purple_role in inter.author.roles:
                            await inter.author.remove_roles(purple_role)
                        if blue_role in inter.author.roles:
                            await inter.author.remove_roles(blue_role)
                        if light_blue_role in inter.author.roles:
                            await inter.author.remove_roles(light_blue_role)
                        if green_role in inter.author.roles:
                            await inter.author.remove_roles(green_role)
                        if mint_role in inter.author.roles:
                            await inter.author.remove_roles(mint_role)
                        if burgundy_role in inter.author.roles:
                            await inter.author.remove_roles(burgundy_role)
                        if red_role in inter.author.roles:
                            await inter.author.remove_roles(red_role)
                        if yellow_role in inter.author.roles:
                            await inter.author.remove_roles(yellow_role)

                        await inter.send(content=f"Роль {orange_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(orange_role)

                    if "yellow_role_option" in inter.values:
                        if yellow_role in inter.author.roles:
                            await inter.send(content=f"Роль {yellow_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(yellow_role)
                            return

                        if white_role in inter.author.roles:
                            await inter.author.remove_roles(white_role)
                        if black_role in inter.author.roles:
                            await inter.author.remove_roles(black_role)
                        if light_grey_role in inter.author.roles:
                            await inter.author.remove_roles(light_grey_role)
                        if grey_role in inter.author.roles:
                            await inter.author.remove_roles(grey_role)
                        if purple_role in inter.author.roles:
                            await inter.author.remove_roles(purple_role)
                        if blue_role in inter.author.roles:
                            await inter.author.remove_roles(blue_role)
                        if light_blue_role in inter.author.roles:
                            await inter.author.remove_roles(light_blue_role)
                        if green_role in inter.author.roles:
                            await inter.author.remove_roles(green_role)
                        if mint_role in inter.author.roles:
                            await inter.author.remove_roles(mint_role)
                        if burgundy_role in inter.author.roles:
                            await inter.author.remove_roles(burgundy_role)
                        if red_role in inter.author.roles:
                            await inter.author.remove_roles(red_role)
                        if orange_role in inter.author.roles:
                            await inter.author.remove_roles(orange_role)

                        await inter.send(content=f"Роль {yellow_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(yellow_role)
                
                if inter.component.custom_id == "alert_menu":
                    if "news_discord_option" in inter.values:
                        if news_discord_role in inter.author.roles:
                            await inter.send(content=f"Роль {news_discord_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(news_discord_role)
                            return

                        await inter.send(content=f"Роль {news_discord_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(news_discord_role)

                    if "news_vk_option" in inter.values:
                        if news_vk_role in inter.author.roles:
                            await inter.send(content=f"Роль {news_vk_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(news_vk_role)
                            return

                        await inter.send(content=f"Роль {news_vk_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(news_vk_role)

                    if "news_personal_project_option" in inter.values:
                        if news_personal_project_role in inter.author.roles:
                            await inter.send(content=f"Роль {news_personal_project_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(news_personal_project_role)
                            return

                        await inter.send(content=f"Роль {news_personal_project_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(news_personal_project_role)

                if inter.component.custom_id == "roles_menu":
                    welcome_roles = disnake.Embed(
                        color=0x2f3136,
                        description="\n```md\n# Уровневые\n```\n"
                        "**<@&986956896806268928>** — Роль за 100 лвл.\n<a:tochka_anim1:978740315676631092> Только мертвец может получить данную роль.\n\n"
                        "**<@&986956901881360464>** — Роль за 70 лвл.\n\n"
                        "**<@&986956967962624040>** — Роль за 40 лвл.\n\n"
                        "**<@&986956973822066688>** — Роль за 20 лвл.\n\n"
                        "**<@&986956976850354176>** — Роль за 10 лвл.")

                    welcome_roles.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/979713111223312384/linia.png")
                    welcome_roles.set_footer(
                        text="Все роли в этой категории дают возможность кидать файлы в чат.")

                    welcome_roles1 = disnake.Embed(
                        color=0x2f3136,
                        description="\n```md\n# Донат-роли Сервера\n```\n"
                        "**<@&986923867601772565>** — Донат-роль Эндера.\n\n"
                        "**<@&986923875470290954>** — Донат-роль Фантома.\n\n"
                        "**<@&986923881635917844>** — Донат-роль Гардиана.\n\n"
                        "**<@&986923878305640468>** — Донат-роль Шалкера.\n\n"
                        "**<@&986928604334141480>** — Роль игрока.\n<:tochka1:952246149467734016> Даётся всем участникам после прохождения верификации.")

                    welcome_roles1.set_footer(
                        text="""Почти все роли в этой категории можно получить, подав заявку в канале "донат-роли".""")
                    welcome_roles1.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/979713111223312384/linia.png")

                    welcome_roles2 = disnake.Embed(
                        color=0x2f3136)
                    welcome_roles2.set_image(
                        url="https://cdn.discordapp.com/attachments/834837020056616992/979713110938124288/9015f6069dfc8bfa.png")

                    if "roles_option" in inter.values:
                        await inter.send(embeds=[welcome_roles, welcome_roles1, welcome_roles2], ephemeral=True)


def setup(bot):
    bot.add_cog(GreetingModule(bot))
