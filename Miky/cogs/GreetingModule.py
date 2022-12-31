import disnake
import sqlite3
from disnake import ButtonStyle
from disnake.ext import commands
from disnake.ui import View, Button, Select
from cogs.InteractionDatabase import natame_guild

with sqlite3.connect("database (Miky).db") as db:
    cursor = db.cursor()

    class GreetingModule(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.command(name="welcome")
        async def welcometotheclub(self, ctx):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            guild_na = self.bot.get_guild(natame_guild)

            if perms_owner is not None or perms_dev is not None:
                if ctx.guild == guild_na:
                    channel_welcome = self.bot.get_channel(1006514841529360474)
                    channel_memo = self.bot.get_channel(1006514988929777664)
                    channel_rules = self.bot.get_channel(990994445568725132)
                    channel_photobook = self.bot.get_channel(1006515450789777489)

                    await ctx.message.delete()
                    menu_journey = View()
                    menu_journey.add_item(Select(placeholder="Выбери свой путь", custom_id="journey_menu",
                    options = [disnake.SelectOption(emoji="📜", label="Каналы", value="channels_option"),
                                disnake.SelectOption(emoji="✨", label="Роли", value="roles_option"),
                                disnake.SelectOption(emoji="📝", label="Правила", value="rules_option"),
                                disnake.SelectOption(emoji="📔", label="Бот", value="bots_option")]))

                    welcome = disnake.Embed(
                        color=0x2f3136)
                    welcome.set_image(
                        url="https://media.discordapp.net/attachments/681153476889280532/1006648547434827856/51af8b5eec1e472a4e147cbbcb26662c.gif")

                    welcome1 = disnake.Embed(
                        color=0x2f3136,
                        title="Приветствую тебя, друг!",
                        description="Прежде чем начать общение с нашими участниками, рекомендуем ознакомиться с пунктами ниже, чтобы сервер стал вам понятнее и ближе.")
                    welcome1.add_field(name="Выбери раздел, нажав на него в меню выбора:", value="**📜 Каналы** - информация о каналах сервер.\n✨ **Роли** - информация о ролях сервера.\n📝 **Правила** - свод здешних правил нахождения.\n📔 **Бот** - команды серверного и других ботов.", inline=False)
                    welcome1.set_image(
                        url="https://cdn.discordapp.com/attachments/838848278858039336/1002270493749027006/linia.png")

                    await channel_welcome.send(embeds=[welcome, welcome1], view=menu_journey)

                    menu_gender = View()
                    menu_gender.add_item(Select(placeholder="Выберите свой гендер", custom_id="gender_menu",
                    options = [disnake.SelectOption(emoji="<a:No_Check:877264845366517770>", label="Не выбрано", value="default_option", default=True),
                                disnake.SelectOption(emoji="<:icons8480:1006928743102689352>", label="Девочка", value="female_option"),
                                disnake.SelectOption(emoji="<:icons8480:1006928741622100040>", label="Мальчик", value="male_option")]))

                    menu_alert = View()
                    menu_alert.add_item(Select(placeholder="Серверные оповещения", custom_id="alert_menu",
                    options = [disnake.SelectOption(emoji="<a:No_Check:877264845366517770>", label="Не выбрано", value="default_option", default=True),
                                disnake.SelectOption(emoji="<:icons890:1006928773456859267>", label="Изменения на сервере", value="server_change_option"),
                                disnake.SelectOption(emoji="<:icons890:1006928771707846697>", label="Набор в персонал", value="staff_alert_option")]))

                    menu_event = View()
                    menu_event.add_item(Select(placeholder="Ивентовые оповещения", custom_id="event_menu",
                    options = [disnake.SelectOption(emoji="<a:No_Check:877264845366517770>", label="Не выбрано", value="default_option", default=True),
                                disnake.SelectOption(emoji="<:icons890:1006928778204815520>", label="Gartic Phone", value="gartic_phone_option"),
                                disnake.SelectOption(emoji="<:icons890:1006928779526033439>", label="Among Us", value="among_us_option"),
                                disnake.SelectOption(emoji="<:icons890:1006928780947886190>", label="Глобальные мероприятия", value="global_event_option"),
                                disnake.SelectOption(emoji="<:icons8oculusrift90:1006928776808116337>", label="Фильмы", value="film_option"),
                                disnake.SelectOption(emoji="<:icons890:1006928775176540180>", label="Мафия", value="mafia_option")]))

                    memo = disnake.Embed(
                        color=0x2f3136)
                    memo.set_image(
                        url="https://media.discordapp.net/attachments/1006517992777072692/1006925062852587600/8b601d3c95b31cb3.png")

                    memo1 = disnake.Embed(
                        color=0x2f3136)
                    memo1.set_image(
                        url="https://media.discordapp.net/attachments/1006517992777072692/1006925062382813224/59d92660daf5a29b.png")

                    memo2 = disnake.Embed(
                        color=0x2f3136)
                    memo2.set_image(
                        url="https://media.discordapp.net/attachments/1006517992777072692/1006925061955006554/4fb310256f0e37c6.png")

                    await channel_memo.send(embed=memo, view=menu_gender)
                    await channel_memo.send(embed=memo1, view=menu_alert)
                    await channel_memo.send(embed=memo2, view=menu_event)

                    rules_1_1 = disnake.Embed(
                        color=0x2f3136,
                        title="Пункт правил — 1.1",
                        description="Запрещено распространение взрослого контента, оскорбительного и шок контента.\nЗапрещено совращение несовершеннолетних.")
                    rules_1_1.add_field(name="Вид наказания:", value="```Бан```")
                    rules_1_1.add_field(name="Длительность:", value="```Навсегда```")
                    rules_1_1.set_image(
                        url="https://cdn.discordapp.com/attachments/838848278858039336/1002270493749027006/linia.png")

                    rules_1_2 = disnake.Embed(
                        color=0x2f3136,
                        title="Пункт правил — 1.2",
                        description="Запрещена реклама любых сторонних ресурсов, а также любая коммерческая деятельность без согласования с администрацией сервера.")
                    rules_1_2.add_field(name="Вид наказания:", value="```Бан```")
                    rules_1_2.add_field(name="Длительность:", value="```Навсегда```")
                    rules_1_2.set_image(
                        url="https://cdn.discordapp.com/attachments/838848278858039336/1002270493749027006/linia.png")

                    rules_1_3 = disnake.Embed(
                        color=0x2f3136,
                        title="Пункт правил — 1.3",
                        description="Запрещены мошеннические действия в отношении участников сервера, а также распространение их личной информации. Запрещены деструктивные действия по отношению к серверу, администрации и модерации.")
                    rules_1_3.add_field(name="Вид наказания:", value="```Мут/Бан```")
                    rules_1_3.add_field(name="Длительность:", value="```До 24 часов/Навсегда```")
                    rules_1_3.set_image(
                        url="https://cdn.discordapp.com/attachments/838848278858039336/1002270493749027006/linia.png")

                    rules_1_4 = disnake.Embed(
                        color=0x2f3136,
                        title="Пункт правил — 1.4",
                        description="Запрещено беспричинное упоминание ролей или злоупотребления упоминаниями пользователей.")
                    rules_1_4.add_field(name="Вид наказания:", value="```Мут```")
                    rules_1_4.add_field(name="Длительность:", value="```До 3 дней```")
                    rules_1_4.set_image(
                        url="https://cdn.discordapp.com/attachments/838848278858039336/1002270493749027006/linia.png")

                    rules_1_5 = disnake.Embed(
                        color=0x2f3136,
                        title="Пункт правил — 1.5",
                        description="Запрещены нелинкабельные никнеймы, намеренное копирование профилей и ролей, а также оскорбительные или провокационные никнеймы со статусами.")
                    rules_1_5.add_field(name="Вид наказания:", value="```Бан```")
                    rules_1_5.add_field(name="Длительность:", value="```До 30 дней```")
                    rules_1_5.set_image(
                        url="https://cdn.discordapp.com/attachments/838848278858039336/1002270493749027006/linia.png")

                    rules_1_6 = disnake.Embed(
                        color=0x2f3136,
                        title="Пункт правил — 1.6",
                        description="Запрещено использование другой учетной записи, чтобы избежать наложенных на вас санкций или фарма валюты сервера.")
                    rules_1_6.add_field(name="Вид наказания:", value="```Бан```")
                    rules_1_6.add_field(name="Длительность:", value="```До 7 дней```")
                    rules_1_6.set_image(
                        url="https://cdn.discordapp.com/attachments/838848278858039336/1002270493749027006/linia.png")

                    rules_1_7 = disnake.Embed(
                        color=0x2f3136,
                        title="Пункт правил — 1.7",
                        description="Запрещен капс (9+), спам (5+), флуд (11+), мультипост (3+) в любых его проявлениях, а также несоблюдение тематики чата.")
                    rules_1_7.add_field(name="Вид наказания:", value="```Мут```")
                    rules_1_7.add_field(name="Длительность:", value="```До 4 часов```")
                    rules_1_7.set_image(
                        url="https://cdn.discordapp.com/attachments/838848278858039336/1002270493749027006/linia.png")

                    rules_1_8 = disnake.Embed(
                        color=0x2f3136,
                        title="Пункт правил — 1.8",
                        description="Запрещён SoundPad и его аналоги, громкие мешающие звуки, увеличение громкости микрофона, использование программ для изменения голоса.")
                    rules_1_8.add_field(name="Вид наказания:", value="```Мут```")
                    rules_1_8.add_field(name="Длительность:", value="```До 12 часов```")
                    rules_1_8.set_image(
                        url="https://cdn.discordapp.com/attachments/838848278858039336/1002270493749027006/linia.png")

                    rules_1_9 = disnake.Embed(
                        color=0x2f3136,
                        title="Пункт правил — 1.9",
                        description="Запрещено неадекватное поведение в любом его виде: оскорбления, оскорбление/упоминание родителей, провокации, дискриминация, угрозы, крики и тому подобные действия. Запрещено разжигание конфликтов, споров.")
                    rules_1_9.add_field(name="Вид наказания:", value="```Мут```")
                    rules_1_9.add_field(name="Длительность:", value="```До 12 часов```")
                    rules_1_9.set_image(
                        url="https://cdn.discordapp.com/attachments/838848278858039336/1002270493749027006/linia.png")

                    await channel_rules.send(embeds=[rules_1_1, rules_1_2, rules_1_3, rules_1_4, rules_1_5, rules_1_6, rules_1_7, rules_1_8, rules_1_9])
                    
                    photobook_button = View()
                    photobook_button.add_item(
                        Button(
                            style=ButtonStyle.url,
                            emoji="📱",
                            url="https://discord.com/channels/990994236306509995/1006831525251256500"))
                    photobook_button.add_item(
                        Button(
                            style=ButtonStyle.url,
                            emoji="📸",
                            url="https://discord.com/channels/990994236306509995/1006831623930662912"))
                    photobook_button.add_item(
                        Button(
                            style=ButtonStyle.url,
                            emoji="💫",
                            url="https://discord.com/channels/990994236306509995/1006831731644567552"))
                    photobook_button.add_item(
                        Button(
                            style=ButtonStyle.url,
                            emoji="🎨",
                            url="https://discord.com/channels/990994236306509995/1006831810908536832"))

                    photobook = disnake.Embed(
                        color=0x2f3136,
                        title="• Добро пожаловать в твой фотоальбом 📔",
                        description="Здесь ты сможешь ознакомиться с нашим и твоим фотоальбомом!\n\nЗдесь ты можешь полюбоваться фотографиями как связанными с эстетикой, так и просто полюбоваться нашими участниками.")
                    photobook.set_image(
                        url="https://i.pinimg.com/originals/8c/ff/24/8cff247307b062baa15eda2e8a2a3140.gif")

                    photobook1 = disnake.Embed(
                        color=0x2f3136,
                        title="Доступные фотоальбомы:",
                        description="`📱` - селфи наших участников.\n`📸` - ваши фотографии.\n`💫` - эстетика вашего мира.\n`🎨` - ваше творчество.")
                    photobook1.set_image(
                        url="https://cdn.discordapp.com/attachments/838848278858039336/1002270493749027006/linia.png")

                    photobook2 = disnake.Embed(
                        color=0x2f3136,
                        title="Если у вас есть желание пополнить его, переходите по кнопкам и наслаждайтесь ❤️")
                    photobook2.set_image(
                        url="https://cdn.discordapp.com/attachments/838848278858039336/1002270493749027006/linia.png")

                    await channel_photobook.send(embeds=[photobook, photobook1, photobook2], view=photobook_button)
                    return

            await ctx.message.delete(delay=5)
            await ctx.reply(content="Права на использование есть только у разработчика бота.", delete_after=5)

        @commands.Cog.listener()
        async def on_dropdown(self, inter: disnake.MessageInteraction):
            guild_na = self.bot.get_guild(natame_guild)
                
            if inter.guild == guild_na:
                female_role = disnake.utils.get(inter.guild.roles, id=1006871226968453162)
                male_role = disnake.utils.get(inter.guild.roles, id=1006873929488543764)

                server_change_role = disnake.utils.get(inter.guild.roles, id=1006927177331257356)
                staff_alert_role = disnake.utils.get(inter.guild.roles, id=1006927177830387744)

                gartic_phone_role = disnake.utils.get(inter.guild.roles, id=1006927119185621002)
                among_us_role = disnake.utils.get(inter.guild.roles, id=1006927173812228196)
                global_event_role = disnake.utils.get(inter.guild.roles, id=1006927174864998450)
                film_role = disnake.utils.get(inter.guild.roles, id=1006927175343149137)
                mafia_role = disnake.utils.get(inter.guild.roles, id=1006927176492400741)

                if inter.component.custom_id == "journey_menu":
                    await inter.send(content="Функция недоступна.", ephemeral=True)
                    return

                    if "channels_option" in inter.values:
                        channel_embed = disnake.Embed(
                            color=0x2f3136,
                            description="> **Воу, ты здесь впервые?**\n> **Тебе стоит познакомиться с нами.**\n> **Уверен, тебе здесь понравится.**\n\n"
                            "<#1006514841529360474> — навигация по серверу.\n"
                            "<#1006514988929777664> — информация о сервере.\n"
                            "<#1006515049763983452> — новости сервера.\n"
                            "<#1006515074631991316> — анонсы ивентов.\n"
                            "<#1006515016175980547> - набор в состав.\n\n"
                            "<#1006515165572890674> — чатик сервера.\n"
                            "<#1006515298905620611> — чат для команд.\n"
                            "<#1006515381659250738> — знакомства.\n"
                            "<#1006515450789777489> - фотоальбом сервера.\n\n"
                            "<#1006534806483501066> - правила гильдий.\n"
                            "<#1006547748532801627> - поиск гильдии.")

                        await inter.send(content="Идёт загрузка...", ephemeral=True)
                        msg = await inter.original_message()
                        await msg.edit(content=None, embed=channel_embed)

                    if "roles_option" in inter.values:
                        role_embed = disnake.Embed(
                            color=0x2f3136,
                            description="``Администрация``\n"
                            "<@&1006618270457139210> — администрация сервера.\n"
                            "<@&1006622416648274041> — разработчики ботов.\n"
                            "<@&1006622510822989996> — кураторы модерации.\n"
                            "``Персонал``\n"
                            "<@&1006622598748188834> — помощь по серверу.\n"
                            "<@&1006624193510645921> — пиар сервера.\n"
                            "``Обслуживание кланов``\n"
                            "<@&1006622699080142969> — клановый модератор.\n"
                            "<@&1006542116350079036> — лидеры кланов.\n"
                            "``Ивентеры``\n"
                            "<@&1006623065192546314> — куратор ивентов.\n"
                            "<@&1006623032363728896> — ивентер.")

                        await inter.send(content="Идёт загрузка...", ephemeral=True)
                        msg = await inter.original_message()
                        await msg.edit(content=None, embed=role_embed)

                    if "rules_option" in inter.values:
                        rules_embed = disnake.Embed(
                            color=0x2f3136)
                        rules_embed.add_field(name="Сервер модерируется согласно:",
                                            value="<a:tochka_anim1:978740315676631092> [Правилам сообщества](https://discord.com/guidelines)\n"
                                            "<a:tochka_anim1:978740315676631092> [Серверным правилам](https://discord.com/channels/990994236306509995/990994445568725132)\n\n"
                                            "<a:tochka_anim1:978740315676631092> Для того чтобы отправить жалоба на пользоватея сервера, воспользуйтесь командой ``/report``\n"
                                            "<a:tochka_anim1:978740315676631092> Учтите, что причину нужно указать корректную и понятную, в инном случаи ваш репорт будет закрыт, без его рассмотрения.\n"
                                            "<a:tochka_anim1:978740315676631092> За абьюз репортов можно получить наказание до 2 дней, в зависимости от частоты использования, без на того причины.\n\n"
                                            "<a:tochka_anim1:978740315676631092> Ознакомление с правилами - одна из важных частей пребывание на любом сервере! Незнание правил не освобождает от ответственности.",
                                            inline=False)

                        await inter.send(content="Идёт загрузка...", ephemeral=True)
                        msg = await inter.original_message()
                        await msg.edit(content=None, embed=rules_embed)

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
                
                if inter.component.custom_id == "gender_menu":
                    await inter.send(content="Функция недоступна.", ephemeral=True)
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

                    if "male_option" in inter.values:
                        if male_role in inter.author.roles:
                            await inter.send(content="Вы уже выбрали эту роль.", ephemeral=True)
                            return

                        if female_role in inter.author.roles:
                            await inter.author.remove_roles(female_role)

                        await inter.send(content=f"Роль {male_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(male_role)
                        return

                if inter.component.custom_id == "alert_menu":
                    await inter.send(content="Функция недоступна.", ephemeral=True)
                    return

                    if "server_change_option" in inter.values:
                        if server_change_role in inter.author.roles:
                            await inter.send(content=f"Роль {server_change_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(server_change_role)
                            return

                        await inter.send(content=f"Роль {server_change_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(server_change_role)

                    if "staff_alert_option" in inter.values:
                        if staff_alert_role in inter.author.roles:
                            await inter.send(content=f"Роль {staff_alert_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(staff_alert_role)
                            return

                        await inter.send(content=f"Роль {staff_alert_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(staff_alert_role)

                if inter.component.custom_id == "event_menu":
                    await inter.send(content="Функция недоступна.", ephemeral=True)
                    return
                    
                    if "gartic_phone_option" in inter.values:
                        if gartic_phone_role in inter.author.roles:
                            await inter.send(content=f"Роль {gartic_phone_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(gartic_phone_role)
                            return

                        await inter.send(content=f"Роль {gartic_phone_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(gartic_phone_role)

                    if "among_us_option" in inter.values:
                        if among_us_role in inter.author.roles:
                            await inter.send(content=f"Роль {among_us_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(among_us_role)
                            return

                        await inter.send(content=f"Роль {among_us_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(among_us_role)

                    if "global_event_option" in inter.values:
                        if global_event_role in inter.author.roles:
                            await inter.send(content=f"Роль {global_event_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(global_event_role)
                            return

                        await inter.send(content=f"Роль {global_event_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(global_event_role)

                    if "film_option" in inter.values:
                        if film_role in inter.author.roles:
                            await inter.send(content=f"Роль {film_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(film_role)
                            return

                        await inter.send(content=f"Роль {film_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(film_role)

                    if "mafia_option" in inter.values:
                        if mafia_role in inter.author.roles:
                            await inter.send(content=f"Роль {mafia_role.mention} убрана.", ephemeral=True)
                            await inter.author.remove_roles(mafia_role)
                            return

                        await inter.send(content=f"Роль {mafia_role.mention} выдана.", ephemeral=True)
                        await inter.author.add_roles(mafia_role)
                        

    # editr.set_image(url = "https://i.imgur.com/xsnzCnW.png"


def setup(bot):
    bot.add_cog(GreetingModule(bot))
