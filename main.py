import nextcord
import requests
import datetime
from datetime import timedelta
import os
import logging
import openai
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
from nextcord.errors import Forbidden
import asyncio
import time
import sys
import shutil
from win10toast import ToastNotifier
import sqlite3
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# import flet as ft
intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.bans = True
intents.moderation = True
logging.basicConfig(filename="log.log",
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

client_discord = nextcord.Client(intents=intents)
scheduler = AsyncIOScheduler()

API_Weather = 'get your api key on openweathermap.org/api'
Forbidden_words = ['enter you list of forbidden words']
guild_owner_emodji_id = 'add id of your emodji'
guild_owner_emodji = f"<:customemoji:{guild_owner_emodji_id}>"
verification_level_emodji_id = 'add id of your emodji'
verification_level_emodji = f"<:customemoji:{verification_level_emodji_id}>"
created_since_emodji_id = 'add id of your emodji'
created_since_emodji = f"<:customemoji:{created_since_emodji_id}>"
all_categories_emodji_id = 'add id of your emodji'
all_categories_emodji = f"<:customemoji:{all_categories_emodji_id}>"
categories_emodji_id = 'add id of your emodji'
categories_emodji = f"<:customemoji:{categories_emodji_id}>"
members_emodji_id = 'add id of your emodji'
members_emodji = f"<:customemoji:{members_emodji_id}>"
boost_emodji_id = 'add id of your emodji'
boost_emodji = f"<:customemoji:{boost_emodji_id}>"
voice_emodji_id = 'add id of your emodji'
voice_emodji = f"<:customemoji:{voice_emodji_id}>"
stack_emodji_id = 'add id of your emodji'
stack_emodji = f"<:customemoji:{stack_emodji_id}>"
slide_emodji_id = 'add id of your emodji'
slide_emodji = f"<:customemoji:{slide_emodji_id}>"
reason_emodji_id = 'add id of your emodji'
reason_emodji = f"<:customemoji:{reason_emodji_id}>"
telegram_channels_link = 'Your link to telegram chat/channel'
discord_server_link = 'Your link to discord server'
servername_to_footer = 'enter name of server'
servername_database = 'enter name of server'
channel_stat = 'enter your statistic channel id'
try:
    with open('Openai_API.txt', 'r') as f:
        openai.api_key = f.read().strip()
except FileNotFoundError:
    openai.api_key = input("Введите ваш апи для ChatGPT: ")
    with open('Openai_API.txt', 'w') as f:
        f.write(openai.api_key)

try:
    with open('token.txt', 'r') as f:
        TOKEN = f.read().strip()
except FileNotFoundError:
    TOKEN = input("Введите ваш токен Discord: ")
    with open('token.txt', 'w') as f:
        f.write(TOKEN)

def win_notification(title, message):
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=0, threaded=True)

async def send_server_info():
    logger = logging.getLogger(__name__)
    logger.info(f'Отправка информации о сервере | {datetime.datetime.now().replace(microsecond=0)}')
    channel = client_discord.get_channel(channel_stat)
    if channel:
        guild = channel.guild
    else:
        logger.error(f'Канал с айди {channel} не найден!')
    async for msg in channel.history(limit=1):
        await msg.delete()
    bots = sum(1 for member in guild.members if member.bot)
    total_members = guild.member_count
    without_bot = total_members - bots
    time = datetime.datetime.now().replace(microsecond=0)

    server_owner = guild.owner.mention
    if server_owner == None:
        server_owner = 'Не указано'
    verification_level = guild.verification_level
    if verification_level == guild.verification_level.low:
        verification_level_show = 'Низкий'
    elif verification_level == guild.verification_level.medium:
        verification_level_show = 'Средний'
    elif verification_level == guild.verification_level.high:
        verification_level_show = 'Высокий'
    else:
        verification_level_show = 'Нет'
    created_at = guild.created_at
    now = datetime.datetime.now(nextcord.utils.utcnow().tzinfo)
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    categories = len(guild.categories)

    embed = nextcord.Embed(title=guild.name, color=0x6fa8dc)
    embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name='Основное', value=f'{guild_owner_emodji} Владелец: {server_owner}\n'
                                           f'{verification_level_emodji} Уровень проверки: {verification_level_show}\n'
                                           f'{created_since_emodji} Создан: <t:{int(created_at.timestamp())}:F>\n(<t:{int(created_at.timestamp())}:R>)\n'
                                           f'{all_categories_emodji} Всего {text_channels + voice_channels + categories} каналов\n'
                                           f'{stack_emodji} {all_categories_emodji} Текстовые каналы: {text_channels}\n'
                                           f'{stack_emodji} {voice_emodji} Голосовые каналы: {voice_channels}\n'
                                           f'{slide_emodji} {categories_emodji} Категории: {categories}\n')
    embed.add_field(name='Пользователи', value=f'{members_emodji} Всего {total_members} участников\n'
                                               f'{stack_emodji} Ботов: {bots}\n'
                                               f'{slide_emodji} Участников: {without_bot}\n')
    boost_level = guild.premium_tier
    embed.add_field(name='Бусты',
                    value=f'{boost_emodji} Уровень: {boost_level} (бустов - {guild.premium_subscription_count})\n')
    embed.add_field(name='Ссылки',
                    value=f'📲Telegram-канал: {telegram_channels_link} \n👾Discord-сервер: {discord_server_link}\n')
    embed.set_footer(text=f'• {servername_to_footer} Info {time}',
                     icon_url=guild.icon.url)
    await channel.send(embed=embed)
async def warn(interaction, guild_id, user_id, user_name, guild):
    database_location = sqlite3.connect(f'{servername_database}_discord.db')
    cursor = database_location.cursor()
    cursor.execute("SELECT warns FROM warn_list WHERE guild_id=? AND user_id=?",
                   (guild_id, user_id))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO warn_list (guild_id, user_id, warns) VALUES (?, ?, ?)",
                       (guild_id, user_id, 1))
    else:
        current_warns = result[0]
        cursor.execute("UPDATE warn_list SET warns=?, last_warn_time=? WHERE guild_id=? AND user_id=?",
                       (current_warns + 1, datetime.datetime.now(), guild_id, user_id))
    cursor.execute("SELECT warns FROM warn_list WHERE guild_id=? AND user_id=?",
                   (guild_id, user_id))
    result = cursor.fetchone()
    warn_count = result[0]
    database_location.commit()
    database_location.close()
    reason = 'некорректная причина выдачи наказания!'
    embed = nextcord.Embed(title='Предупреждение', color=nextcord.Color.dark_purple())
    embed.add_field(name=f'{user_name} ваш было выдано предупреждение\nПричина: {reason}\nУ вас {warn_count} предупреждений ', value='')
    embed.set_footer(text=f'• {servername_to_footer} Warn | {datetime.datetime.now().replace(microsecond=0)}',
                     icon_url=interaction.guild.icon.url)
    await interaction.channel.send(embed=embed)
@client_discord.event
async def on_ready():
    print(f'{client_discord.user} запущен')
    print(' ')
    message = f"Блокировка: /ban Нарушитель причина \nРазблокировка: /unban Нарушитель причина \nУдаление: /kick Нарушитель причина \nОтчистка: /clear количество(можно любым количеством либо 0 для удаления всего) \nСписок всех учатников: /members \nВывод информации о сервере: /serverinfo \nЗаглушение участника: /mute Нарушитель причина"f" \nРазглушение участника: /unmute Нарушитель причина \nИнформация о участнике: /info Участник \nАватар участника: /avatar Участник \nИнформация о погоде: /weather Город(любой) \nВывод этого сообщения: /commands (в канал #bot-commands, не писать) \nОтправить сообщение: /say (сообщение)"
    print(message)
    scheduler.add_job(send_server_info, 'interval', days=7)
    scheduler.start()
    database_location = sqlite3.connect(f'{servername_database}_discord.db')
    cursor = database_location.cursor()
    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS users_list (
                            user_id INTEGER PRIMARY KEY,
                            user_name TEXT NOT NULL,
                            user_mention TEXT NOT NULL,
                            user_joined_date DATETIME NOT NULL
                        )
                    ''')
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS mod_actions (
                action_id INTEGER PRIMARY KEY AUTOINCREMENT,
                action_type TEXT NOT NULL,
                guild_id INTEGER NOT NULL,
                moderator_name TEXT NOT NULL,
                moderator_id INTEGER NOT NULL,
                target_user_name TEXT NOT NULL,
                target_user_id INTEGER NOT NULL,
                reason TEXT,
                action_time DATETIME NOT NULL
            )
        """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS warn_list (
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                warns INTEGER DEFAULT 0,
                last_warn_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    database_location.commit()
    database_location.close()
    win_notification("Bot Started", f"Дискорд бот запущен\n{servername_database}_discord.db started\nTime: {datetime.datetime.now().replace(microsecond=0)}")
@client_discord.event
async def on_member_join(member):
    user_id = member.id
    user_name = member.name
    user_mention = member.mention
    user_joined_date = member.joined_at

    logger = logging.getLogger(__name__)
    logger.info(f'К серверу подключился новый участник: {user_name}')

    try:
        database_location = sqlite3.connect(f'{servername_database}_discord.db')
        cursor = database_location.cursor()
        cursor.execute("INSERT INTO users_list (user_id, user_name, user_mention, user_joined_date) VALUES (?, ?, ?, ?)",
                       (user_id, user_name, user_mention, user_joined_date))
        database_location.commit()
    except sqlite3.Error as e:
        logger.error(f'Something went wrong. Error: {e}')
    finally:
        database_location.close()

    embed_server = nextcord.Embed(
        title=f'Привет, добро пожаловать на сервер "{servername_database}"',
        color=nextcord.Color.purple()
    )
    embed_server.set_thumbnail(url=member.avatar.url)
    embed_server.add_field(name='Информация', value='Ищи всю нужную информацию в канале "информация"')
    embed_server.set_footer(text=f'{servername_database} Welcome | {datetime.datetime.now().replace(microsecond=0)}')

    embed_user = nextcord.Embed(
        title=f'Привет, благодарим за присоединение к серверу "{servername_database}"',
        color=nextcord.Color.purple()
    )
    embed_user.set_thumbnail(url=member.avatar.url)
    embed_user.add_field(name='Информация', value=f'Всю необходимую информацию вы можете найти в канале "информация".')
    embed_user.set_footer(text=f'{servername_database} Welcome | {datetime.datetime.now().replace(microsecond=0)}')

    channel = nextcord.utils.get(member.guild.channels, name='добро-пожаловать')
    if channel:
        await channel.send(embed=embed_server)
    else:
        logger.error(f'Канал admin не найден, укажите верный канал!')

    await member.send(embed=embed_user)
@client_discord.event
async def on_member_leave(member):
    embed_server = nextcord.Embed(title=f'Удачи, участник {member.name} покинул сервер "{servername_database}"',
                                  color=nextcord.Color.dark_blue())
    embed_server.set_thumbnail(url=member.avatar.url)
    embed_server.add_field(name='', value='К сожалению пользователь покинул сервер, удачи ему!')
    embed_server.set_footer(text=f'{servername_database} Goodbye | {datetime.datetime.now().replace(microsecond=0)}')

    embed_user = nextcord.Embed(title=f'Удачи, вы покинули сервер "{servername_database}"',
                                color=nextcord.Color.purple())
    embed_user.set_thumbnail(url=member.avatar.url)
    embed_user.add_field(name=' ', value=f'К сожалению вы покинули сервер, удачи вам!')
    embed_user.set_footer(text=f'{servername_database} Goodbye | {datetime.datetime.now().replace(microsecond=0)}')
    channel = nextcord.utils.get(member.guild.channels, name='admin')
    if channel:
        await channel.send(embed=embed_server)
    else:
        logger.error(f'Канал {channel} не найден, укажите верный канал!')
    await member.send(embed=embed_user)
@client_discord.event
async def on_message(message):
    for word in Forbidden_words:
        if word in message.content:
            if any(role.name == "Администратор" for role in message.author.roles):
                return
            else:
                async for msg in message.channel.history(limit=1):
                    await msg.delete()
                await message.channel.send(f'{message.author.mention}. В вашем сообщении обнаружено запрещённое слово. Просьба больше не нарушать.')
                return

@client_discord.slash_command(name='ban', description='Блокирует участника')
async def ban(interaction: Interaction, member: nextcord.Member,
              reason: str = SlashOption(
                  description="Причина бана",
                  default="Причина не указана"
              )):
    logger = logging.getLogger(__name__)
    logger.info(f"Пользователь {interaction.user.mention} вызвал команду блокировки")
    if nextcord.utils.get(interaction.user.roles, name='Администратор') is not None:
        try:
            await member.ban(reason=reason)
            logger.info(f'Пользователь {member.mention} был заблокирован {interaction.user.mention} по причине: {reason}')
            try:
                database_location = sqlite3.connect(f'{servername_database}_discord.db')
                cursor = database_location.cursor()
                cursor.execute("""
                    INSERT INTO mod_actions (action_type, guild_id, moderator_name, moderator_id, target_user_name, target_user_id, reason, action_time) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, ('Ban', interaction.guild.id, interaction.user.name, interaction.user.id, member.name, member.id, reason,
                      datetime.datetime.now()))
                cursor.close()
                database_location.commit()
            except sqlite3.Error as e:
                logger.error(f'Something went wrong! Error: {e}')
            finally:
                database_location.close()
            if reason in ['Причина не указана']:
                await warn(interaction, interaction.guild.id, interaction.user.id,
                           interaction.user.name, interaction.guild)
            time = datetime.datetime.now().replace(microsecond=0)
            embed = nextcord.Embed(title="Информация о блокировке", color=nextcord.Color.dark_purple())
            embed.add_field(name=' ', value=f'Администратор: {interaction.user.mention}\n{reason_emodji} Причина: {reason}\nЗаблокированный: {member.mention}\n')
            embed.set_footer(text=f'• {servername_to_footer} Moderation | {datetime.datetime.now().replace(microsecond=0)}',
                             icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed)
        except nextcord.Forbidden:
            logger.error('У бота не достаточно прав для блокировки пользователя!')
            await interaction.response.send_message('У меня не достаточно прав для выполнения этой команды!', ephemeral=True)
    else:
        logger.info(f'У {interaction.user.mention} не достаточно прав для блокировки пользователя')
        await interaction.response.send_message('У вас не достаточно прав для использования этой команды!', ephemeral=True)
@client_discord.slash_command(name='warn', description='Выдаёт предупреждение участнику')
async def warn_command(interaction: Interaction, member: nextcord.Member,
                       action: str = SlashOption(description='Выберите действие',
                                                 choices=['show', 'give'],
                                                 default='show'),
                       reason: str = SlashOption(description='Причина предупреждения',
                                                 default='Причина не указана'
                       )):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.name} использовал команду для предупреждения участника')
    if nextcord.utils.get(interaction.user.roles, name='Администратор') is not None:
        if action == 'show':
            try:
                database_location = sqlite3.connect(f'{servername_database}_discord.db')
                cursor = database_location.cursor()
                cursor.execute("SELECT warns FROM warn_list WHERE guild_id=? AND user_id=?",
                               (interaction.guild.id, member.id))
                warn_count = cursor.fetchone()
                cursor.execute("SELECT last_warn_time FROM warn_list WHERE guild_id=? AND user_id=?",
                               (interaction.guild.id, member.id))
                warn_last = cursor.fetchone()
            except sqlite3.Error as e:
                await interaction.response.send_message(f'Произошла ошибка: {e}', ephemeral=True)
            try:
                embed = nextcord.Embed(title=f'Информация о {member.name}', color=nextcord.Color.dark_purple())
                embed.add_field(name=' ', value=f'Количество предупреждений: {warn_count[0]}\n'
                                                f'Последнее предупреждение: {warn_last[0]}')
                embed.set_footer(text=f'•{servername_to_footer} warn | {datetime.datetime.now().replace(microsecond=0)}',
                                 icon_url=interaction.guild.icon.url)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            except TypeError:
                embed = nextcord.Embed(title='Информация', color=nextcord.Color.dark_purple())
                embed.add_field(name='', value=f'{member.name} не найден в базе данных!')
                embed.set_footer(
                    text=f'•{servername_to_footer} Warn | {datetime.datetime.now().replace(microsecond=0)}',
                    icon_url=interaction.guild.icon.url)
        if action == 'give':
            try:
                database_location = sqlite3.connect(f'{servername_database}_discord.db')
                cursor = database_location.cursor()
                cursor.execute("SELECT warns FROM warn_list WHERE guild_id=? AND user_id=?",
                               (interaction.guild.id, member.id))
                result = cursor.fetchone()
                if result is None:
                    cursor.execute("INSERT INTO warn_list (guild_id, user_id, warns) VALUES (?, ?, ?)",
                                   (interaction.guild.id, member.id, 1))
                else:
                    current_warns = result[0]
                    cursor.execute("UPDATE warn_list SET warns=?, last_warn_time=? WHERE guild_id=? AND user_id=?",
                                   (current_warns + 1, datetime.datetime.now(), interaction.guild.id, member.id))
                database_location.commit()
                cursor.execute("SELECT warns FROM warn_list WHERE guild_id=? AND user_id=?",
                               (interaction.guild.id, member.id))
                embed_result = cursor.fetchone()
                database_location.close()
            except sqlite3.Error as e:
                logger.error(f'Something went w rong. Error: {e}')
                await interaction.response.send_message(f'Произошла ошибка: {e}')
            embed = nextcord.Embed(title='Предупреждение', color=nextcord.Color.dark_purple())
            embed.add_field(name='', value=f'Администратор: {interaction.user.mention}\n{reason_emodji} Причина: {reason}\nПредупреждённый: {member.mention}\nКоличество предупреждений: {embed_result[0]}')
            embed.set_footer(text=f'• {servername_to_footer} Warn | {datetime.datetime.now().replace(microsecond=0)}',
                             icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(f'У вас недостаточно прав для использования этой команды!', ephemeral=True)
@client_discord.slash_command(name='kick', description='Удаляет участника, участник сможет зайти повторно')
async def kick(interaction: Interaction, member: nextcord.Member, reason: str = SlashOption(description='Причина удаления', default="Причина не указана")):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.mention} вызвал команду удаления участника')
    if nextcord.utils.get(interaction.user.roles, name='Администратор') is not None:
        try:
            await member.kick(reason=reason)
            logger.info(f'Пользователь {member.mention} был удалён {interaction.user.mention} по причине: {reason}')
            try:
                database_location = sqlite3.connect(f'{servername_database}_discord.db')
                cursor = database_location.cursor()
                cursor.execute("""
                    INSERT INTO mod_actions (action_type, guild_id, moderator_name, moderator_id, target_user_name, target_user_id, reason, action_time) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, ('Kick', interaction.guild.id, interaction.user.name, interaction.user.id, member.name, member.id, reason,
                      datetime.datetime.now()))
                database_location.commit()
            except sqlite3.Error as e:
                logger.error(f'Something went wrong! Error: {e}')
            finally:
                database_location.close()
            if reason in ['Причина не указана']:
                await warn(interaction, interaction.guild.id, interaction.user.id,
                           interaction.user.name, interaction.guild)
            time = datetime.datetime.now().replace(microsecond=0)
            embed = nextcord.Embed(title="Информация о удалении", color=nextcord.Color.dark_purple())
            embed.add_field(name=' ', value=f'Администратор: {interaction.user.mention}\n{reason_emodji} Причина: {reason}\nУдалённый: {member.mention}')
            embed.set_footer(text=f'• {servername_to_footer} warn | {datetime.datetime.now().replace(microsecond=0)}',
                             icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed)
        except nextcord.Forbidden:
            logger.error('У бота не достаточно прав для удаления пользователя!')
            await interaction.response.send_message('У меня не достаточно прав для выполнения этой команды!',ephemeral=True)
    else:
        logger.info(f'У {interaction.user.mention} не достаточно прав для удаления пользователя')
        await interaction.response.send_message('У вас не достаточно прав для использования этой команды!',ephemeral=True)
@client_discord.slash_command(name='server-info', description='Выводит статистику сервера')
async def serverinfo(interaction: Interaction,
                     type: str = SlashOption(description='Выберите какой тип статистики вы хотите вывести: новая или старая',
                                               choices=['new', 'old'],
                                               default='new'
                                               )):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.mention} вызвал команду вывода статистики сервера')
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        if type == 'new':
            guild = interaction.guild
            bots = sum(1 for member in guild.members if member.bot)
            total_members = guild.member_count
            without_bot = total_members - bots
            time = datetime.datetime.now().replace(microsecond=0)

            server_owner = guild.owner.mention
            if server_owner == None:
                server_owner = 'Не указано'
            verification_level = guild.verification_level
            if verification_level == guild.verification_level.low:
                verification_level_show = 'Низкий'
            elif verification_level == guild.verification_level.medium:
                verification_level_show = 'Средний'
            elif verification_level == guild.verification_level.high:
                verification_level_show = 'Высокий'
            else:
                verification_level_show = 'Нет'
            created_at = guild.created_at
            now = datetime.datetime.now(nextcord.utils.utcnow().tzinfo)
            text_channels = len(guild.text_channels)
            voice_channels = len(guild.voice_channels)
            categories = len(guild.categories)

            embed = nextcord.Embed(title=guild.name, color=0x6fa8dc)
            embed.set_thumbnail(url=guild.icon.url)
            embed.add_field(name='Основное', value=f'{guild_owner_emodji} Владелец: {server_owner}\n'
                                              f'{verification_level_emodji} Уровень проверки: {verification_level_show}\n'
                                              f'{created_since_emodji} Создан: <t:{int(created_at.timestamp())}:F>\n(<t:{int(created_at.timestamp())}:R>)\n'
                                              f'{all_categories_emodji} Всего {text_channels + voice_channels + categories} каналов\n'
                                              f'{stack_emodji} {all_categories_emodji} Текстовые каналы: {text_channels}\n'
                                              f'{stack_emodji} {voice_emodji} Голосовые каналы: {voice_channels}\n'
                                              f'{slide_emodji} {categories_emodji} Категории: {categories}\n')
            embed.add_field(name='Пользователи', value=f'{members_emodji} Всего {total_members} участников\n'
                                                       f'{stack_emodji} Ботов: {bots}\n'
                                                       f'{slide_emodji} Участников: {without_bot}\n')
            boost_level = guild.premium_tier
            embed.add_field(name='Бусты', value=f'{boost_emodji} Уровень: {boost_level} (бустов - {guild.premium_subscription_count})\n')
            embed.add_field(name='Ссылки', value=f'📲Telegram-канал: {telegram_channels_link} \n👾Discord-сервер: {discord_server_link}\n')
            embed.set_footer(text=f'• Запрос от {interaction.user}\n• {servername_to_footer} Info {time}',
                             icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        if type == 'old':
            logger = logging.getLogger(__name__)
            logger.info(f'Пользователь {interaction.user.mention} вызвал команду вывода статистики сервера')
            if nextcord.utils.get(interaction.user.roles, name="Администратор") is not None:
                guild = nextcord.utils.get(client_discord.guilds, id=1171462603260821585)
                bots = sum(1 for member in guild.members if member.bot)
                admin_role = nextcord.utils.get(guild.roles, name="Администратор")
                admin_count = len([member for member in interaction.guild.members if admin_role in member.roles])
                verify_role = nextcord.utils.get(guild.roles, name="Верифицирован✅️")
                verify_count = len([member for member in interaction.guild.members if verify_role in member.roles])
                time = datetime.datetime.now().replace(microsecond=0)

                embed = nextcord.Embed(title="Информация о сервере", color=0xffffff)
                embed.set_thumbnail(url=guild.icon.url)
                embed.add_field(name="Дата создания: ", value=f'<t:{int(guild.created_at.timestamp())}:R>',
                                inline=False)
                embed.add_field(name="Участники",
                                value=f"Всего участников: {len(guild.members)} \n"
                                      f"Ботов: {str(bots)} \n"
                                      f"Администраторов: {admin_count} \n"
                                      f"Верифицировались: {verify_count}",
                                inline=False)
                embed.add_field(name="Каналы",
                                value=f"Текстовых каналов: {len(guild.text_channels)}\n"
                                      f"Голосовых каналов: {len(guild.voice_channels)}\n"
                                      f"Категорий: {len(guild.categories)} ",
                                inline=False)
                embed.add_field(name="Ссылки",
                                value=f"📲Telegram-канал: {telegram_channels_link} \n👾Discord-сервер: {discord_server_link}")
                embed.set_footer(text=f'• Запрос от {interaction.user}\n• {servername_to_footer} Info {time}',
                                 icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(
            'У вас недостаточно прав для вывода информации сервера. Пожалуйста перейдите в канал #статистика', ephemeral=True)
@client_discord.slash_command(name='clear', description='Удаляет сообщения')
async def clear(interaction: Interaction, limit: int = SlashOption(description='Количество сообщений (0 - удалить всё)')):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.mention} вызвал команду для очистки сообщений')
    if nextcord.utils.get(interaction.user.roles, name='Администратор') is not None:
        try:
            if limit == 0:
                await interaction.channel.purge(limit=None)
            else:
                await interaction.channel.purge(limit=limit)

            if interaction.response.is_done():
                await interaction.followup.send('Сообщения успешно очищены', ephemeral=True)
            else:
                await interaction.response.send_message('Сообщения успешно очищены', ephemeral=True)
        except nextcord.errors.Forbidden:
            if interaction.response.is_done():
                await interaction.followup.send('У меня недостаточно прав для очистки сообщений.', ephemeral=True)
            else:
                await interaction.response.send_message('У меня недостаточно прав для очистки сообщений.', ephemeral=True)
        except ValueError:
            if interaction.response.is_done():
                await interaction.followup.send('Вы ввели неправильное число', ephemeral=True)
            else:
                await interaction.response.send_message('Вы ввели неправильное число', ephemeral=True)
    else:
        if interaction.response.is_done():
            await interaction.followup.send('У вас недостаточно прав для очистки сообщений', ephemeral=True)
        else:
            await interaction.response.send_message('У вас недостаточно прав для очистки сообщений', ephemeral=True)

@client_discord.slash_command(name='members', description='Выводит список всех пользователей')
async def members(interaction: Interaction):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.mention} вызвал команду для вывода списка участника')
    if nextcord.utils.get(interaction.user.roles, name='Администратор') is not None:
        time = datetime.datetime.now().replace(microsecond=0)
        guild = interaction.guild
        members_info = [f"{member.mention}-{member.name} (ID: {member.id}) (Высшая роль: {member.top_role})" for member
                        in guild.members]

        embed = nextcord.Embed(title='Участники сервера', description='\n'.join(members_info), color=0xffffff)
        embed.set_footer(text=f'{servername_to_footer} Info {time}\nНа сервере {guild.member_count} участников')
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(f'{interaction.user.mention}. У вас недостаточно прав для использования этой команды!', ephemeral=True)



@client_discord.slash_command(name='help', description='Выводит список команд бота')
async def help(interaction: Interaction,
             rank: str = SlashOption(
                  name="rank",
                  description='Выберите ранг: mod или default',
                  choices=['default', 'mod'],
                  default='default'
             )
             ):
    logger = logging.getLogger(__name__)
    if rank == 'default':
        logger.info(f'Пользователь {interaction.user.mention} вызвал команду для вывода списка команд. Ранг: Участник')
        time = datetime.datetime.now().replace(microsecond=0)
        embed = nextcord.Embed(title="Доступные команды сервера", color=0xffffff)
        embed.add_field(name="Ранг: Участник", value=f"Информация о участнике: /info Участник \nАватар участника: /avatar Участник \n Информация о погоде: /weather Город(любой)\nВывести это сообщение: /help", inline=False)
        embed.set_footer(text=f'•{servername_to_footer} Help | {datetime.datetime.now().replace(microsecond=0)}',
                         icon_url=interaction.guild.icon.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    elif rank == 'mod':
        if nextcord.utils.get(interaction.user.roles, name='Администратор') is not None:
            logger.info(
                f'Пользователь {interaction.user.mention} вызвал команду для вывода списка команд. Ранг: Модерация')
            time = datetime.datetime.now().replace(microsecond=0)
            embed = nextcord.Embed(title="Доступные команды сервера", color=0xffffff)
            embed.add_field(
                name="Ранг: Модерация",
                value=f"Блокировка: /ban Нарушитель причина \nРазблокировка: /unban Нарушитель причина \nУдаление: /kick Нарушитель причина \nОтчистка: /clear количество(можно любым количеством либо 0 для удаления всего) \nСписок всех учатников: /members \nВывод информации о сервере: /serverinfo \nЗаглушение участника: /mute Нарушитель причина"f" \nРазглушение участника: /unmute Нарушитель причина \nИнформация о участнике: /info Участник \nАватар участника: /avatar Участник \nИнформация о погоде: /weather Город(любой) \nВывод этого сообщения: /help mod\nОтправить сообщение: /say (сообщение)\nДействия с логами: /log (download, archive, save)",
                inline=False)
            embed.set_footer(text=f' •{servername_to_footer} Help | {datetime.datetime.now().replace(microsecond=0)}',
                             icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message('У вас недостаточно прав для отправки команд', ephemeral=True)
@client_discord.slash_command(name='mute', description='Заглушает участника')
async def mute(interaction: Interaction, member: nextcord.Member, reason: str = SlashOption(description='Причина заглушения', default="Причина не указана")):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.mention} вызвал команду для заглушения участника')
    if nextcord.utils.get(interaction.user.roles, name='Администратор') is not None:
        try:
            mute_role = nextcord.utils.get(interaction.guild.roles, name="Muted")
            if not mute_role:
                mute_role = await interaction.guild.create_role(name="Muted",permissions=discord.Permissions(send_messages=False,speak=False))
                await mute_role.edit(position=1)
            await member.add_roles(mute_role, reason=reason)
            logger.info(f'Пользователь {member.mention} был заглушён {interaction.user.mention} по причине: {reason}')
            try:
                database_location = sqlite3.connect(f'{servername_database}_discord.db')
                cursor = database_location.cursor()
                cursor.execute("""
                    INSERT INTO mod_actions (action_type, guild_id, moderator_name, moderator_id, target_user_name, target_user_id, reason, action_time) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, ('Mute', interaction.guild.id, interaction.user.name, interaction.user.id, member.name, member.id, reason,
                      datetime.datetime.now()))
                database_location.commit()
            except sqlite3.Error as e:
                logger.error(f'Something went wrong! Error: {e}')
            finally:
                database_location.close()
            if reason in ['Причина не указана']:
                await warn(interaction, interaction.guild.id, interaction.user.id,
                           interaction.user.name, interaction.guild)
            time = datetime.datetime.now().replace(microsecond=0)
            embed = nextcord.Embed(title=f"Информация о заглушении", color=nextcord.Color.dark_purple())
            embed.add_field(name=' ', value=f'Администратор: {interaction.user.mention}\nПричина: {reason}\nЗаглушённый: {member.mention}')
            embed.set_footer(text=f' •{servername_to_footer} Moderation | {datetime.datetime.now().replace(microsecond=0)}',
                             icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed)
        except nextcord.Forbidden:
            logger.error('У бота не достаточно прав для заглушения пользователя!')
            await interaction.response.send_message('У меня не достаточно прав для выполнения этой команды!',
                                                    ephemeral=True)
    else:
        logger.info(f'У {interaction.user.mention} не достаточно прав для удаления пользователя')
        await interaction.response.send_message('У вас не достаточно прав для использования этой команды!',
                                                ephemeral=True)

@client_discord.slash_command(name='unmute', description='Снимает заглушение участника')
async def unmute(interaction: Interaction, member: nextcord.Member, reason: str = SlashOption(description='Причина заглушения', default="Причина не указана")):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.mention} вызвал команду для снятия заглушения участника')
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        try:
            mute_role = nextcord.utils.get(interaction.guild.roles, name="Muted")
            if not mute_role:
                mute_role = await interaction.guild.create_role(name="Muted",permissions=discord.Permissions(send_messages=False,speak=False))
                await mute_role.edit(position=1)
            await member.remove_roles(mute_role, reason=reason)
            logger.info(f'Пользователь {member.mention} был разглушён {interaction.user.mention} по причине: {reason}')
            try:
                database_location = sqlite3.connect(f'{servername_database}_discord.db')
                cursor = database_location.cursor()
                cursor.execute("""
                    INSERT INTO mod_actions (action_type, guild_id, moderator_name, moderator_id, target_user_name, target_user_id, reason, action_time) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, ('Unmute', interaction.guild.id, interaction.user.name, interaction.user.id, member.name, member.id, reason,
                      datetime.datetime.now()))
                database_location.commit()
            except sqlite3.Error as e:
                logger.error(f'Something went wrong! Error: {e}')
            finally:
                database_location.close()
            if reason in ['Причина не указана']:
                await warn(interaction, interaction.guild.id, interaction.user.id,
                           interaction.user.name, interaction.guild)
            time = datetime.datetime.now().replace(microsecond=0)
            embed = nextcord.Embed(title='Информации о разглушении', color=nextcord.Color.dark_purple())
            embed.add_field(name=' ', value=f'Администратор: {interaction.user.mention}\nПричина: {reason}\nРазглушённый: {member.mention}')
            embed.set_footer(text=f' •{servername_to_footer} Moderation | {datetime.datetime.now().replace(microsecond=0)}',
                             icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed)
        except nextcord.Forbidden:
            logger.error('У бота не достаточно прав для заглушения пользователя!')
            await interaction.response.send_message('У меня не достаточно прав для выполнения этой команды!',
                                                    ephemeral=True)
    else:
        logger.info(f'У {interaction.user.mention} не достаточно прав для удаления пользователя')
        await interaction.response.send_message('У вас не достаточно прав для использования этой команды!',
                                                ephemeral=True)

@client_discord.slash_command(name='unban', description='Снимает блокировку с пользователя')
async def unban(interaction: Interaction, user_id: str, reason: str = SlashOption(description='Причина блокировки', default='Причина не указана')):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.mention} вызвал команду для снятия блокировки с участника')

    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        try:
            user = await client_discord.fetch_user(int(user_id))
            await interaction.guild.unban(user, reason=reason)
            time = datetime.datetime.now().replace(microsecond=0)
            embed = nextcord.Embed(title='Информация о разблокировке', color=nextcord.Color.dark_purple())
            embed.add_field(name=' ', value=f'Администратор: {interaction.user.mention}\n'
                                            f'{reason_emodji} Причина: {reason}\n'
                                            f'Разблокированный: {user.mention}\n')
            embed.set_footer(
                text=f' •{servername_to_footer} Moderation | {datetime.datetime.now().replace(microsecond=0)}',
                icon_url=interaction.guild.icon.url)

            if reason == 'Причина не указана':
                await warn(interaction, interaction.guild.id, interaction.user.id,
                           interaction.user.name, interaction.guild)  # Используйте warn здесь

            try:
                database_location = sqlite3.connect(f'{servername_database}_discord.db')
                cursor = database_location.cursor()
                cursor.execute("""
                    INSERT INTO mod_actions (action_type, guild_id, moderator_name, moderator_id, target_user_name, target_user_id, reason, action_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, ('Unban', interaction.guild.id, interaction.user.name, interaction.user.id,
                      user.name, user.id, reason, datetime.datetime.now()))
                database_location.commit()
            except Exception as e:
                logger.error(f'Something went wrong! Error: {e}')
            finally:
                database_location.close()

            await interaction.response.send_message(embed=embed)
        except nextcord.errors.Forbidden:
            logger.error(f"Произошла ошибка: discord.errors.Forbidden")
            await interaction.response.send_message('У меня не достаточно прав', ephemeral=True)
        except nextcord.errors.NotFound:
            logger.error(f'Произошла ошибка: discord.errors.NotFound')
            await interaction.response.send_message('Участник не найден в списке заблокированных', ephemeral=True)
    else:
        await interaction.response.send_message('У вас не достаточно прав для использования данной команды', ephemeral=True)
@client_discord.slash_command(name='info', description='Отправляет информацию о участнике')
async def info(interaction: Interaction, member: nextcord.Member,
               hidden: str = SlashOption(
                   name="hidden",
                   description='Выберите как будет оправленно сообщение',
                   choices=['hidden', 'shown'],
                   default='hidden'
               )):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.mention} вызвал команду для вывода информации о участнике')
    time = datetime.datetime.now().replace(microsecond=0)
    excepted_roles = ["@everyone", "Member"]
    role_count = len([role.name for role in member.roles if role.name not in excepted_roles])
    roles = member.roles
    role_names = [role.name for role in roles if role.name not in excepted_roles]
    role_list = ' '.join(role_names)
    discriminator = member.discriminator
    if discriminator == 0:
        discriminator = None
    embed = nextcord.Embed(title=f"Информация о {member.name}", color=0xffffff)
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="Никнейм:", value=member.name, inline=True)
    embed.add_field(name="Профиль:", value=member.mention, inline=True)
    embed.add_field(name="Полное имя:", value=f'{member.name}#{discriminator}', inline=True)
    embed.add_field(name="ID:", value=member.id, inline=True)
    embed.add_field(name="Дата присоеденения:", value=f'<t:{int(member.joined_at.timestamp())}:R>', inline=True)
    embed.add_field(name='Дата создания профиля: ', value=f'<t:{int(member.created_at.timestamp())}:R>')
    embed.add_field(name="Роль:", value=member.top_role.name, inline=True)
    embed.add_field(name="Роли:", value=role_list)
    embed.add_field(name='Количество ролей:', value=role_count)
    embed.set_footer(text=f'• {servername_to_footer} Info | {datetime.datetime.now().replace(microsecond=0)}',
                     icon_url=interaction.guild.icon.url)
    if hidden == 'hidden':
        await interaction.response.send_message(embed=embed, ephemeral=True)
    elif hidden == 'shown':
        await interaction.response.send_message(embed=embed, ephemeral=False)

@client_discord.slash_command(name='say', description='Отправляет сообщение от имени бота')
async def say(interaction: Interaction, message: str = SlashOption(description='Отправляет текст введённый здесь')):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.mention} вызвал команду для отправки сообщения от имени бота')
    time = datetime.datetime.now().replace(microsecond=0)
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        await interaction.channel.send(message)
        await interaction.response.send_message('Сообщение успешно отправленно', ephemeral=True)
        logger.info(f'Пользователь {interaction.user.name} отправил ({message}) от имени бота')
    else:
        await interaction.response.send_message(f'У вас недостаточно прав для использования этой команды\n{servername_to_footer} Moderation {time}', ephemeral=True)
@client_discord.slash_command(name='avatar', description='Отпраляет аватарку пользователя')
async def avatar(interaction: Interaction, member: nextcord.Member):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.mention} использовал команду для вывода аватара пользователя')
    time = datetime.datetime.now().replace(microsecond=0)
    embed = nextcord.Embed(title=f'Аватар {member.name}', color=0xffffff)
    embed.set_image(url=member.avatar.url)
    embed.set_footer(text=f'• {servername_to_footer} Info | {datetime.datetime.now().replace(microsecond=0)}',
                     icon_url=interaction.guild.icon.url)
    await interaction.response.send_message(embed=embed)
@client_discord.slash_command(name='log', description='Отправляет действия с логами')
async def log(interaction: Interaction,
              content: str = SlashOption(
                  name="action",
                  description='Выберите действие которое хотите совершить с логами',
                  choices=['download',  'save', 'archive', 'delete']
              ),
              target: str = SlashOption(
                  name="target",
                  description='Выберите откуда будет загрузка: current, archive или любое другое название файла',
                  default='current'
              )
):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.mention} использовал команду для вывода логов')
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        if content.lower() in ['delete']:
            if target in ['archive']:
                if interaction.user.name == 'ivan_kem_twink':
                    folder_path = 'archive_logs'
                    if os.path.exists(folder_path):
                        for filename in os.listdir(folder_path):
                            file_path = os.path.join(folder_path, filename)
                            if os.path.isfile(file_path):
                                os.remove(file_path)
                        await interaction.response.send_message('Папка с архивом логов успешно отчищена', ephemeral=True)
                        win_notification('User clear archive logs', f'{interaction.user.name} cleared archive log files\nTime: {datetime.datetime.now().replace(microsecond=0)}')
                    else:
                        print(f"Папка '{folder_path}' не найдена.")
                else:
                    await interaction.response.send_message('Вас нет в списке разрешёных пользователей', ephemeral=True)
            if target in ['current']:
                if interaction.user.name == 'ivan_kem_twink':
                    logging.shutdown()
                    open('log.log', 'w').close()
                    logging.basicConfig(filename='log.log', level=logging.INFO)
                    await interaction.response.send_message(f'Действующий файл логов удалён', ephemeral=True)
                    win_notification('User clear current log', f'{interaction.user.name} cleared main logging file\nTime: {datetime.datetime.now().replace(microsecond=0)}')
        if content.lower() in ['download', 'Download', 'dowload', 'Dowload']:
            if content == 'download':
                if target == 'current':
                    logger.info(f'Пользователь {interaction.user.name} запросил базу скачивание логов!')
                    await interaction.response.send_message(file=nextcord.File(f'log.log'),
                                                            ephemeral=True)
                    win_notification('User downloaded log',
                                     f'Current log file downloaded by {interaction.user.name}')
                elif target in ['Archive', 'archive']:
                    archive_logs_dir = os.path.join(os.getcwd(), 'archive_logs')
                    files = os.listdir(archive_logs_dir)
                    await interaction.response.defer(ephemeral=True)
                    for file in files:
                        file_path = os.path.join(archive_logs_dir, file)
                        await interaction.followup.send(file=nextcord.File(file_path), ephemeral=True)
                    win_notification('User downloaded log',
                                     f'{interaction.user.name} downloaded archive log files\nTime: {datetime.datetime.now().replace(microsecond=0)}')
                else:
                    logger.info(f'Пользователь {interaction.user.name} запросил базу скачивание логов!')
                    try:
                        await interaction.response.send_message(file=nextcord.File(f'archive_logs\\{target}'),
                                                                ephemeral=True)
                    except FileNotFoundError:
                        await interaction.response.send_message(f'Файл не найден', ephemeral=True)
                    win_notification('User downloaded log', f'{target} downloaded by {interaction.user.name}')

            else:
                await interaction.response.send_message('Вы ввели не верное действие со скачиванием, попробуйте снова', ephemeral=True)
        elif content.lower() in ['save', 'Save']:
            log_channel = nextcord.utils.get(interaction.guild.channels, name='logs')
            if log_channel:
                file = 'log.log'
                with open(file, 'r') as file1:
                    first_line_temp = file1.readline()
                    first_line = first_line_temp.strip()
                log_datetime_str = first_line.split(' ', 1)[0]
                log_datetime = datetime.datetime.strptime(log_datetime_str, "%Y-%m-%d")

                last_change_time = os.path.getmtime('log.log')
                last_change_timestamp = int(last_change_time)

                try:
                    await log_channel.send(file=nextcord.File('log.log'))
                    await log_channel.send(
                        f'Это файл логов за время с последнего вызова.\n'
                        f'Вызвал: {interaction.user.mention}\n'
                        f'Дата создания: <t:{int(log_datetime.timestamp())}:R>\n'
                        f'Дата последнего изменения: <t:{last_change_timestamp}:R>'
                    )
                except nextcord.errors.Forbidden:
                    await interaction.response.send_message('У меня не достаточно прав для отправки файла с логами!', ephemeral=True)
                if not os.path.exists('archive_logs'):
                    os.makedirs('archive_logs')

                logging.shutdown()
                if not os.path.exists('archive_logs'):
                    os.makedirs('archive_logs')

                new_log_name = f"log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
                new_log_path = os.path.join('archive_logs', new_log_name)

                shutil.move('log.log', new_log_path)

                open('log.log', 'w').close()

                logging.basicConfig(filename='log.log', level=logging.INFO)
                await interaction.response.send_message(
                        f'Файл логов успешно отправлен администраторам в канал logs и перезаписан', ephemeral=True)
                win_notification('User rewrited (save) log',
                                 f'{interaction.user.name} rewrited current log file\nTime: {datetime.datetime.now().replace(microsecond=0)}')
            else:
                interaction.response.send_message('Не удалось найти файл логов!', ephemeral=True)
        elif content.lower() in ['archive', 'Archive']:
            archive_logs_dir = os.path.join(os.getcwd(), 'archive_logs')

            if not os.path.exists(archive_logs_dir) or not os.path.isdir(archive_logs_dir):
                await interaction.response.send_message("Папка archive_logs не найдена.", ephemeral=True)
                return

            files = os.listdir(archive_logs_dir)

            embed = nextcord.Embed(title="Список файлов в архиве логов", color=0xffffff)

            for file in files:
                file_path = os.path.join(archive_logs_dir, file)
                file_size = os.path.getsize(file_path)
                embed.add_field(name=file, value=f"Размер: {(file_size/1024.0):.2f}кб", inline=False)
                embed.set_footer(
                    text=f'• {servername_to_footer} Log | {datetime.datetime.now().replace(microsecond=0)}',
                    icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message('У вас недостаточно прав для использования этой команды',
                                                ephemeral=True)
@client_discord.slash_command(name='weather', description='Отправляет погоду в указанном городе')
async def weather(interaction: Interaction, city: str = SlashOption(description='Укажите город')):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.mention} использовал команду для отправки погоды')

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_Weather}&units=metric'
    time = datetime.datetime.now().replace(microsecond=0)
    response = requests.get(url)
    logger.info(f"Запрос к API OpenWeatherMap: {url}")

    if response.status_code == 200:
        weather_data = response.json()
        try:
            filtered_data = {
                "X": weather_data['coord']['lon'],
                "Y": weather_data['coord']['lat'],
                "Temp_min": weather_data['main']['temp_min'],
                "Temp_max": weather_data['main']['temp_max'],
                "Temp": weather_data['main']['temp'],
                "Feels_like": weather_data['main']['feels_like'],
                "Country": weather_data['sys']['country'],
                "Wind_speed": weather_data['wind']['speed'],
                "Humidity": weather_data['main']['humidity'],
                "City_id": weather_data['id']
            }
            logger.info(f"Данные погоды для города {city} получены успешно.")
        except KeyError:
            logger.error(f"Ошибка: Не удалось получить данные погоды для города {city}.")
            embed = nextcord.Embed(title=f"Ошибка", color=0xff0000)
            embed.add_field(name=f"Произошла ошибка!", value='Не удалось получить данные погоды.')
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            url_png = f"https://tile.openweathermap.org/map/temp_new/0/0/0.png?appid={API_Weather}"
            embed = nextcord.Embed(title=f"Погода в {city}", color=0x376abd)
            embed.set_thumbnail(url=url_png)
            embed.add_field(
                name=f"Город: {city}, Страна: {filtered_data['Country']}",
                value=f"Средняя температура: {filtered_data['Temp']}°C\n"
                      f"Минимальная температура: {filtered_data['Temp_min']}°C\n"
                      f"Максимальная температура: {filtered_data['Temp_max']}°C\n"
                      f"Температура по ощущениям: {filtered_data['Feels_like']}°C\n"
                      f"Скорость ветра: {filtered_data['Wind_speed']} м/с\n"
                      f"Влажность: {filtered_data['Humidity']}%\n"
                      f"Запрос выполнен: {time}\n"
                      f"Запросил: {interaction.user.mention}\n"
                      f"Источник: https://openweathermap.org/city/{filtered_data['City_id']}"
            )
            embed.set_footer(text=f'• {servername_to_footer} Weather | {datetime.datetime.now().replace(microsecond=0)}',
                             icon_url=interaction.guild.icon.url)
            logger.info(f"Прогноз погоды для города {city} успешно выведен.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except requests.exceptions.HTTPError as e:
            logger.error(f"Ошибка HTTP: {e}")
            embed = nextcord.Embed(title=f"Ошибка", color=0xff0000)
            embed.add_field(name=f"Ошибка получения данных", value='Сервер недоступен')
            embed.set_footer(
                text=f'• {servername_to_footer} Weather | {datetime.datetime.now().replace(microsecond=0)}',
                icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка запроса: {e}")
            embed = nextcord.Embed(title=f"Ошибка", color=0xff0000)
            embed.add_field(name=f"Ошибка получения данных", value='Ошибка с запросом попробуйте снова')
            embed.set_footer(
                text=f'• {servername_to_footer} Weather | {datetime.datetime.now().replace(microsecond=0)}',
                icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        logger.error(f"Ошибка: Не удалось получить данные погоды. Код ответа: {response.status_code}")
        embed = nextcord.Embed(title=f"Ошибка", color=0xff0000)
        embed.add_field(name=f"Ошибка получения данных", value='')
        embed.set_footer(text=f'• {servername_to_footer} Weather | {datetime.datetime.now().replace(microsecond=0)}',
                         icon_url=interaction.guild.icon.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='database', description='Управление базой данных сервера')
async def database(interaction: Interaction,
                   content: str = SlashOption(
                       name="action",
                       description='Действие с базой данных',
                       choices=['start', 'download', 'save', 'archive']
                   ),
                   target: str = SlashOption(
                       name='target',
                       description='Выберите какой файл хотите скачать',
                       default='current'
                   )):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.name} использовал команду /database.')
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        if content == 'start':
            try:
                database_location = sqlite3.connect(f'{servername_database}_discord.db')
                cursor = database_location.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users_list (
                        user_id INTEGER PRIMARY KEY,
                        user_name TEXT NOT NULL,
                        user_mention TEXT NOT NULL,
                        user_joined_date DATETIME NOT NULL
                    )
                ''')
                database_location.commit()
                users_data = [(member.id, member.name, member.mention, member.joined_at) for member in
                              interaction.guild.members]
                cursor.executemany(
                    "INSERT OR IGNORE INTO users_list (user_id, user_name, user_mention, user_joined_date) VALUES (?, ?, ?, ?)",
                    users_data)
                database_location.commit()

                await interaction.response.send_message(f'База данных {servername_database}_discord.db перезапущена.', ephemeral=True)

            except sqlite3.Error as e:
                logger.error(f'Ошибка при работе с базой данных: {e}')
                await interaction.response.send_message(f'Произошла ошибка при работе с базой данных: {e}')

            except Exception as e:
                logger.error(f'Ошибка: {e}')
                await interaction.response.send_message(f'Произошла ошибка: {e}')
        if content == 'download':
            if target == 'current':
                logger.info(f'Пользователь {interaction.user.name} запросил базу скачивание базы данных!')
                await interaction.response.send_message(file=nextcord.File(f'{servername_database}_discord.db'),
                                                        ephemeral=True)
                win_notification('Request database',
                                 f'{servername_database}_discord.db downloaded by {interaction.user.name}')
            else:
                logger.info(f'Пользователь {interaction.user.name} запросил базу скачивание базы данных!')
                try:
                    await interaction.response.send_message(file=nextcord.File(f'archive_database\\{target}'), ephemeral=True)
                except FileNotFoundError:
                    await interaction.response.send_message(f'Файл не найден', ephemeral=True)
                win_notification('Request database', f'{target} downloaded by {interaction.user.name}')
        if content == 'save':
            logger.warning(f'Пользователь {interaction.user.name} запросил отключения базы данных')
            database_location = sqlite3.connect(f'{servername_database}_discord.db')
            database_location.commit()
            database_location.close()
            logging.info(f'База данных {servername_database}_discord.db сохранена')
            win_notification('Database stopped', f'{servername_database}_discord.db saved!')
            await interaction.response.send_message(f'База данных {servername_database}_discord.db сохранена', ephemeral=True)
            try:
                shutil.copy2(f'{servername_database}_discord.db',
                             f'archive_database/{servername_database}_discord_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.db')
            except FileNotFoundError:
                logger.error(
                    f'Файл {servername_database}_discord.db не найден. Возможно, он был уже перемещен в архив.')
            except OSError as e:
                logger.error(f'Ошибка при копировании файла: {e}')
            database_channel = nextcord.utils.get(interaction.guild.channels, name='database')
            if database_channel:
                last_change_time = os.path.getmtime(f'{servername_database}_discord.db')
                last_change_timestamp = int(last_change_time)
                try:
                    await database_channel.send(file=nextcord.File(f'{servername_database}_discord.db'))
                    await database_channel.send(
                        f'Это файл базы данных последнего сохранения.\n'
                        f'Вызвал: {interaction.user.mention}\n'
                        f'Дата последнего изменения: <t:{last_change_timestamp}:R>'
                    )
                except FileNotFoundError:
                    await interaction.response.send_message('Файл не найден', ephemeral=True)
        if content.lower() in ['archive', 'Archive']:
            archive_database_dir = os.path.join(os.getcwd(), 'archive_database')

            if not os.path.exists(archive_database_dir) or not os.path.isdir(archive_database_dir):
                await interaction.response.send_message("Папка archive_database не найдена.", ephemeral=True)
                return

            files = os.listdir(archive_database_dir)

            embed = nextcord.Embed(title="Список файлов в архиве баз данных", color=0xffffff)

            for file in files:
                file_path = os.path.join(archive_database_dir, file)
                file_size = os.path.getsize(file_path)
                embed.add_field(name=file, value=f"Размер: {(file_size/1024.0):.2f}кб\n", inline=False)
                embed.set_footer(
                    text=f'• {servername_to_footer} Database | {datetime.datetime.now().replace(microsecond=0)}',
                    icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message('У вас нет прав для выполнения этой команды.')
try:
    client_discord.run(TOKEN)
except Exception as e:
    print(f'Error {e}')
    client_discord.run(TOKEN)
