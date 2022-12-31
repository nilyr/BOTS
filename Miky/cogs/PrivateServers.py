import disnake
import sqlite3
from disnake.ext import commands

with sqlite3.connect("database (Miky).db") as db:
    cursor = db.cursor()

    class PrivateServers(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_member_join(self, member):
            тестирование = self.bot.get_guild(878021276491452426)
            переходник = self.bot.get_guild(1010557429458681956)
            badges = self.bot.get_guild(1012043772047130756)
            emoji_1 = self.bot.get_guild(877241361882026005)
            emoji_2 = self.bot.get_guild(1010557334759682088)

            oni = self.bot.get_user(783391011966550076)
            danielo = self.bot.get_user(335416744212693002)

            if member.guild == тестирование:
                user_role = disnake.utils.get(member.guild.roles, id=1010546509747585136)
                bot_role = disnake.utils.get(member.guild.roles, id=1010546497378603109)

                god_role = disnake.utils.get(member.guild.roles, id=878021824536010805)
                admin_role = disnake.utils.get(member.guild.roles, id=1012097326682222682)

                if member.bot:
                    await member.add_roles(bot_role)
                    return
                
                if member == oni:
                    await member.add_roles(god_role)
                    return

                if member == admin_role:
                    await member.add_roles(son_role)
                    return

                await member.add_roles(user_role)

            if member.guild == переходник:
                user_role = disnake.utils.get(member.guild.roles, id=1010557429458681959)
                bot_role = disnake.utils.get(member.guild.roles, id=1011200061675421776)

                god_role = disnake.utils.get(member.guild.roles, id=1010557429458681961)

                if member.bot:
                    await member.add_roles(bot_role)
                    return
                
                if member == oni:
                    await member.add_roles(god_role)
                    return

                await member.add_roles(user_role)

            if member.guild == badges:
                user_role = disnake.utils.get(member.guild.roles, id=1012043772047130759)
                bot_role = disnake.utils.get(member.guild.roles, id=1012043772047130758)

                god_role = disnake.utils.get(member.guild.roles, id=1012043772047130761)
                son_role = disnake.utils.get(member.guild.roles, id=1012043772047130760)

                if member.bot:
                    await member.add_roles(bot_role)
                    return
                
                if member == oni:
                    await member.add_roles(god_role)
                    return

                if member == danielo:
                    await member.add_roles(son_role)
                    return

                await member.add_roles(user_role)

            if member.guild == emoji_1:
                user_role = disnake.utils.get(member.guild.roles, id=1010540982825127976)
                bot_role = disnake.utils.get(member.guild.roles, id=1010539957963726850)

                god_role = disnake.utils.get(member.guild.roles, id=877263160015486987)
                son_role = disnake.utils.get(member.guild.roles, id=1010539065688469545)

                if member.bot:
                    await member.add_roles(bot_role)
                    return
                
                if member == oni:
                    await member.add_roles(god_role)
                    return

                if member == danielo:
                    await member.add_roles(son_role)
                    return

                await member.add_roles(user_role)

            if member.guild == emoji_2:
                user_role = disnake.utils.get(member.guild.roles, id=1010557334759682091)
                bot_role = disnake.utils.get(member.guild.roles, id=1010557334759682090)

                god_role = disnake.utils.get(member.guild.roles, id=1010557334759682093)
                son_role = disnake.utils.get(member.guild.roles, id=1010557334759682092)

                if member.bot:
                    await member.add_roles(bot_role)
                    return
                
                if member == oni:
                    await member.add_roles(god_role)
                    return

                if member == danielo:
                    await member.add_roles(son_role)
                    return

                await member.add_roles(user_role)

        @commands.command(name="emojis")
        async def emojimessage(self, ctx):
            perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()
            perms_dev = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'DEV'""").fetchone()

            channel_bagdes = self.bot.get_channel(1012043772911173703)
            channel_server1 = self.bot.get_channel(877241362381172749)
            channel_server2 = self.bot.get_channel(1010557335225241611)

            bagdes_embed_info = disnake.Embed(
                color=0x2f3136,
                title="Эмодзи для ботов")
            bagdes_embed_info.set_author(name="Bagdes Miky")

            bagdes_embed_emoji1 = disnake.Embed(
                color=0x2f3136,
                description="<:media_badge:1014164260936503426> \<:media_badge:1014164260936503426>\n"
                "<:staff_badge:1014164262182211705> \<:staff_badge:1014164262182211705>\n"
                "<:friend_badge:1014164259560759296> \<:friend_badge:1014164259560759296>\n"
                "<:moderation_badge:1014164263557943417> \<:moderation_badge:1014164263557943417>")

            bagdes_embed_icons = disnake.Embed(
                color=0x2f3136,
                description="<a:verify:1014164258298265652> \<a:verify:1014164258298265652>\n\n"
                "<:owner:1014175967499014217> \<:owner:1014175967499014217> | https://cdn.discordapp.com/emojis/1014175967499014217.png\n\n"
                "<:developer:1014175969180930078> \<:developer:1014175969180930078> | https://cdn.discordapp.com/emojis/1014175969180930078.png\n\n"
                "<:admin:1014176927768125530> \<:admin:1014176927768125530> | https://cdn.discordapp.com/emojis/1014176927768125530.png")

            server1_embed_info = disnake.Embed(
                color=0x2f3136,
                title="Эмодзи для ботов")
            server1_embed_info.set_author(name="Сервер #1")

            server1_embed_emoji1 = disnake.Embed(
                color=0x2f3136,
                description="<:Boost1:886482964890923018> \<:Boost1:886482964890923018>\n"
                "<:Boost2:886482964869963827> \<:Boost2:886482964869963827>\n"
                "<:Female:985985786476384268> \<:Female:985985786476384268>\n"
                "<:Male:985985761679642725> \<:Male:985985761679642725>\n"
                "<a:No_Check:877264845366517770> \<a:No_Check:877264845366517770>\n"
                "<a:RightArrow1:919166915048517712> \<a:RightArrow1:919166915048517712>\n"
                "<a:Yes_Check:877264845504917565> \<a:Yes_Check:877264845504917565>\n"
                "<a:beloe_serdze:985883774220894238> \<a:beloe_serdze:985883774220894238>\n"
                "<a:boost:877264845815304212> \<a:boost:877264845815304212>\n"
                "<:boost_1:885624936822095902> \<:boost_1:885624936822095902>\n"
                "<:boost_2:885624936788541441> \<:boost_2:885624936788541441>\n"
                "<:boost_3:885624937090539591> \<:boost_3:885624937090539591>\n"
                "<:boosters:885624936876609607> \<:boosters:885624936876609607>\n"
                "<a:boosting:916001610319155210> \<a:boosting:916001610319155210>\n"
                "<a:boosting_blue:916001609182486559> \<a:boosting_blue:916001609182486559>\n"
                "<:bot:885624937015033947> \<:bot:885624937015033947>\n"
                "<:branding:1004492631117664287> \<:branding:1004492631117664287>\n"
                "<:category:885624936922742834> \<:category:885624936922742834>\n"
                "<:channel_text:885624937002434640> \<:channel_text:885624937002434640>\n"
                "<:channel_voice:885624936926945372> \<:channel_voice:885624936926945372>")

            server1_embed_emoji2 = disnake.Embed(
                color=0x2f3136,
                description="<:dev:877264842967363614> \<:dev:877264842967363614>\n"
                "<:discord:877264842715701269> \<:discord:877264842715701269>\n"
                "<:dislike:877264842921222204> \<:dislike:877264842921222204>\n"
                "<:dnd:893597424579391529> \<:dnd:893597424579391529>\n"
                "<a:ecomoney:916001609341894766> \<a:ecomoney:916001609341894766>\n"
                "<:emoji:885624936658501693> \<:emoji:885624936658501693>\n"
                "<:eto_che:985881657854808154> \<:eto_che:985881657854808154>\n"
                "<:hm:877264842656972801> \<:hm:877264842656972801>\n"
                "<:idea:877264842933825566> \<:idea:877264842933825566>\n"
                "<:idle:893597436155691038> \<:idle:893597436155691038>\n"
                "<:instagram:903327117188689990> \<:instagram:903327117188689990>\n"
                "<:like:877264843156123731> \<:like:877264843156123731>\n"
                "<a:loops:898905497820880926> \<a:loops:898905497820880926>\n"
                "<:members:885624936901787738> \<:members:885624936901787738>\n"
                "<a:nitro:877264844921929749> \<a:nitro:877264844921929749>\n"
                "<:no_minecraft:958081430435541012> \<:no_minecraft:958081430435541012>\n"
                "<:off:892647180521836605> \<:off:892647180521836605>\n"
                "<:offline:892647180559597568> \<:offline:892647180559597568>\n"
                "<:online:892647180614123540> \<:online:892647180614123540>\n"
                "<:onn:892647180542808084> \<:onn:892647180542808084>")

            server1_embed_emoji3 = disnake.Embed(
                color=0x2f3136,
                description="<:partner:877264842950594580> \<:partner:877264842950594580>\n"
                "<:ping:919166899076599849> \<:ping:919166899076599849>\n"
                "<:ptichka:1005122804879982673> \<:ptichka:1005122804879982673>\n"
                "<a:question_purple:916001629122207875> \<a:question_purple:916001629122207875>\n"
                "<a:question_red:916001629122216036> \<a:question_red:916001629122216036>\n"
                "<:rarecandy:877264843026096199> \<:rarecandy:877264843026096199>\n"
                "<:roles:885624937015033916> \<:roles:885624937015033916>\n"
                "<:rules:885624936910168094> \<:rules:885624936910168094>\n"
                "<:settings:885624936570425415> \<:settings:885624936570425415>\n"
                "<:slash:885624937015021568> \<:slash:885624937015021568>\n"
                "<:stage_channel:906947237559537804> \<:stage_channel:906947237559537804>\n"
                "<:store:885624936926949386> \<:store:885624936926949386>\n"
                "<:tochka:903713219032518746> \<:tochka:903713219032518746>\n"
                "<:tochka1:952246149467734016> \<:tochka1:952246149467734016>\n"
                "<a:tochka_anim:965680033807101952> \<a:tochka_anim:965680033807101952>\n"
                "<a:tochka_anim1:978740315676631092> \<a:tochka_anim1:978740315676631092>\n"
                "<:vk:903327129905803314> \<:vk:903327129905803314>\n"
                "<a:waiting:1011657420860293180> \<a:waiting:1011657420860293180>\n"
                "<a:warnings:877264842854113322> \<a:warnings:877264842854113322>\n"
                "<:yes_minecraft:958081418641149954> \<:yes_minecraft:958081418641149954>\n\n"
                "<:youtube:877264843009318972> \<:youtube:877264843009318972>")

            server2_embed_info = disnake.Embed(
                color=0x2f3136,
                title="Эмодзи для ботов")
            server2_embed_info.set_author(name="Сервер #2 | Badges Akane")

            server2_embed_emoji1 = disnake.Embed(
                color=0x2f3136,
                description="<:boost_8:1010585300172550264> \<:boost_8:1010585300172550264>\n"
                "<:bughunter:1010585441017286806> \<:bughunter:1010585441017286806>\n"
                "<:early_supporter:1010585382527709224> \<:early_supporter:1010585382527709224>\n"
                "<:hypesquad_events:1010585314458353764> \<:hypesquad_events:1010585314458353764>\n"
                "<:moderator:1010585454707478548> \<:moderator:1010585454707478548>\n"
                "<:nitro:1010585286004183130> \<:nitro:1010585286004183130>\n"
                "<:owner:1010585426920230952> \<:owner:1010585426920230952>\n"
                "<a:partner_gif:1010580758311731201> \<a:partner_gif:1010580758311731201>\n"
                "<:staff:1010585404996587531> \<:staff:1010585404996587531>\n"
                "<:verified:1010585268794957994> \<:verified:1010585268794957994>\n"
                "<:premium:1012422219240063016> \<:premium:1012422219240063016>")
            
            if perms_owner is not None or perms_dev is not None:
                await ctx.message.delete()
                await channel_bagdes.send(embeds=[bagdes_embed_info, bagdes_embed_emoji1])
                await channel_bagdes.send(embed=bagdes_embed_icons)
                await channel_server1.send(embeds=[server1_embed_info, server1_embed_emoji1, server1_embed_emoji2, server1_embed_emoji3])
                await channel_server2.send(embeds=[server2_embed_info, server2_embed_emoji1])


def setup(bot):
    bot.add_cog(PrivateServers(bot))