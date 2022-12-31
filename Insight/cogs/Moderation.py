import disnake
import sqlite3
from disnake.ext import commands


with sqlite3.connect("database (Insight).db") as db:
    cursor = db.cursor()

    class Moderation(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        async def check_status_personal(self, member):
            if member.status == disnake.Status.offline:
                return '<:offline:892647180559597568>'
            if member.status == disnake.Status.online:
                return '<:online:892647180614123540>'
            if member.status == disnake.Status.dnd:
                return '<:dnd:893597424579391529>'
            if member.status == disnake.Status.idle:
                return '<:idle:893597436155691038>'


        @commands.slash_command(name="staff",
                                description="Посмотреть онлайн Персонала Discord",
                                guild_ids=[387409949442965506])
        async def stafflist(self, ctx):
            sostav = []

            kopanda_role = disnake.utils.get(ctx.guild.roles, id=387454972851257345)
            administrator_role = disnake.utils.get(ctx.guild.roles, id=600258400978468874)
            tech_administrator_role = disnake.utils.get(ctx.guild.roles, id=926155535391264809)
            curator_role = disnake.utils.get(ctx.guild.roles, id=927329713431646228)
            support_administration_role = disnake.utils.get(ctx.guild.roles, id=423159755117166592)
            moderator_role = disnake.utils.get(ctx.guild.roles, id=593799068606660619)
            helper_role = disnake.utils.get(ctx.guild.roles, id=485843253481177091)
            overseer_role = disnake.utils.get(ctx.guild.roles, id=538725888276168735)
            overseer_isp_role = disnake.utils.get(ctx.guild.roles, id=575666099408994316)

            for member in kopanda_role.members:
                sostav.append(f'{await self.check_status_personal(member)} **`{member}`** <a:tochka_anim1:978740315676631092> {kopanda_role.mention}')

            for member in administrator_role.members:
                sostav.append(f'{await self.check_status_personal(member)} **`{member}`** <a:tochka_anim1:978740315676631092> {administrator_role.mention}')

            for member in tech_administrator_role.members:
                sostav.append(f'{await self.check_status_personal(member)} **`{member}`** <a:tochka_anim1:978740315676631092> {tech_administrator_role.mention}')

            for member in curator_role.members:
                sostav.append(f'{await self.check_status_personal(member)} **`{member}`** <a:tochka_anim1:978740315676631092> {curator_role.mention}')

            for member in support_administration_role.members:
                sostav.append(f'{await self.check_status_personal(member)} **`{member}`** <a:tochka_anim1:978740315676631092> {support_administration_role.mention}')

            for member in moderator_role.members:
                sostav.append(f'{await self.check_status_personal(member)} **`{member}`** <a:tochka_anim1:978740315676631092> {moderator_role.mention}')

            for member in helper_role.members:
                sostav.append(f'{await self.check_status_personal(member)} **`{member}`** <a:tochka_anim1:978740315676631092> {helper_role.mention}')

            for member in overseer_role.members:
                sostav.append(f'{await self.check_status_personal(member)} **`{member}`** <a:tochka_anim1:978740315676631092> {overseer_role.mention}')

            for member in overseer_isp_role.members:
                sostav.append(f'{await self.check_status_personal(member)} **`{member}`** <a:tochka_anim1:978740315676631092> {overseer_isp_role.mention}')

            personal = f'{str(sostav)}'.replace('[', '').replace(']', '').replace(',', '\n').replace("'", "").replace('"', '')
                
            embed_end = disnake.Embed(
                title="Персонал сервера",
                description=f"{personal}",
                color=0x2f3136)
            embed_end.set_image(
                url="https://cdn.discordapp.com/attachments/834837020056616992/992091846257950782/typo_staff.gif")

            await ctx.response.defer()
            await ctx.send(embed=embed_end)

def setup(bot):
    bot.add_cog(Moderation(bot))