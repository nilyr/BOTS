import os
import disnake
import sqlite3
from disnake.ext import commands
from datetime import datetime, timezone, timedelta

bot = commands.Bot(
    command_prefix="+",
    intents=disnake.Intents.all(),
    case_insensitive=True,
    help_command=None,
    allowed_mentions=disnake.AllowedMentions.all())


@bot.event
async def on_ready():
    channel_status = bot.get_channel(1025508312034332772)
    now = datetime.now(timezone(timedelta(hours=+3)))

    embed = disnake.Embed(
        color=0x2f3136,
        title=f"Бот {bot.user.name} запущен!",
        timestamp=now)

    await channel_status.send(embed=embed)

    print(f"Бот {bot.user.name} запущен!")

with sqlite3.connect("database (Hell).db") as db:
    cursor = db.cursor()

    @bot.command(name="load")
    async def load(ctx, extension=None):
        perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()

        if perms_owner is not None:
            if extension is None:
                await ctx.message.delete(delay=5)
                await ctx.reply(content="Вы не указали название модуля.", delete_after=5)
                return
            try:
                bot.load_extension(f"cogs.{extension}")
                await ctx.message.delete(delay=10)
                await ctx.reply(content=f"Модуль **{extension}** загружен.", delete_after=10)
                return
            except BaseException:
                await ctx.message.delete(delay=5)
                await ctx.reply(content="Вы указали неправильное название модуля.", delete_after=5)
                return

        await ctx.message.delete(delay=5)
        await ctx.reply(content="Права на использование есть только у разработчика бота, уровень прав которого равен **1**.", delete_after=5)


    @bot.command(name="unload")
    async def unload(ctx, extension=None):
        perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()

        if perms_owner is not None:
            if extension is None:
                await ctx.message.delete(delay=5)
                await ctx.reply(content="Вы не указали название модуля.", delete_after=5)
                return
            try:
                bot.unload_extension(f"cogs.{extension}")
                await ctx.message.delete(delay=10)
                await ctx.reply(content=f"Модуль **{extension}** отключён.", delete_after=10)
                return
            except BaseException:
                await ctx.message.delete(delay=5)
                await ctx.reply(content="Вы указали неправильное название модуля.", delete_after=5)
                return

        await ctx.message.delete(delay=5)
        await ctx.reply(content="Права на использование есть только у разработчика бота, уровень прав которого равен **1**.", delete_after=5)


    @bot.command(name="reload")
    async def reload(ctx, extension=None):
        perms_owner = cursor.execute(f"""SELECT * FROM perms WHERE user_id = {ctx.author.id} AND lvl_rights = 'OWN'""").fetchone()

        if perms_owner is not None:
            if extension is None:
                await ctx.message.delete(delay=5)
                await ctx.reply(content="Вы не указали название модуля.", delete_after=5)
                return
            try:
                bot.reload_extension(f"cogs.{extension}")
                await ctx.message.delete(delay=10)
                await ctx.reply(content=f"Модуль **{extension}** перезагружен.", delete_after=10)
                return
            except BaseException:
                await ctx.message.delete(delay=5)
                await ctx.reply(content="Вы указали неправильное название модуля.", delete_after=5)
                return

        await ctx.message.delete(delay=5)
        await ctx.reply(content="Права на использование есть только у разработчика бота, уровень прав которого равен **1**.", delete_after=5)


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

token = open("token.txt", "r").readline()

bot.run(token)
