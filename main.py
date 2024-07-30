import nextcord
import requests
import datetime
from datetime import timedelta
import os
import logging
import openai
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption, ButtonStyle, ChannelType
from nextcord.errors import Forbidden
from nextcord.ui import Button, View, UserSelect, Select, TextInput, Modal
import asyncio
import time
import sys
import shutil
from win10toast import ToastNotifier
import sqlite3
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import json
# import flet as ft
intents = nextcord.Intents.default()
intents.invites = True
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
API_Crypto = 'get your api key on https://pro.coinmarketcap.com/account'
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
member_emodji_id = 'add id of your emodji'
member_emodji = f"<:customemoji:{member_emodji_id}>"
boost_emodji_id = 'add id of your emodji'
boost_emodji = f"<:customemoji:{boost_emodji_id}>"
voice_emodji_id = 'add id of your emodji'
voice_emodji = f"<:customemoji:{voice_emodji_id}>"
reason_emodji_id = 'add id of your emodji'
reason_emodji = f"<:customemoji:{reason_emodji_id}>"
telegram_channels_link = 'Your link to telegram chat/channel'
discord_server_link = 'Your link to discord server'
servername_to_footer = 'enter name of server'
servername_database = 'enter name of server'
staff_emodji_id = 'add id of your emodji'
staff_emodji = f"<:customemoji:{staff_emodji_id}>"
warn_emodji_id = 'add id of your emodji'
warn_emodji = f"<:customemoji:{warn_emodji_id}>"
time_emodji_id = 'add id of your emodji'
time_emodji = f"<:customemoji:{time_emodji_id}>"
text_emodji_id = 'add id of your emodji'
text_emodji = f"<:customemoji:{text_emodji_id}>"
slash_emodji_id = 'add id of your emodji'
slash_emodji = f"<:customemoji:{slash_emodji_id}>"
bot_emodji_id = 'add id of your emodji'
bot_emodji = f"<:customemoji:{bot_emodji_id}>"
telegram_emodji_id = 'add id of your emodji'
telegram_emodji = f"<:customemoji:{telegram_emodji_id}>"
discord_emodji_id = 'add id of your emodji'
discord_emodji = f"<:customemoji:{discord_emodji_id}>"
link_emodji_id = 'add id of your emodji'
link_emodji = f"<:customemoji:{link_emodji_id}>"
BTC_emodji_id = 'add id of your emodji'
BTC_emodji = f"<:customemoji:{BTC_emodji_id}>"
ETH_emodji_id = 'add id of your emodji'
ETH_emodji = f"<:customemoji:{ETH_emodji_id}>"
DOGE_emodji_id = 'add id of your emodji'
DOGE_emodji = f"<:customemoji:{DOGE_emodji_id}>"
RUB_emodji_id = 'add id of your emodji'
RUB_emodji = f"<:customemoji:{RUB_emodji_id}>"
USD_emodji_id = 'add id of your emodji'
USD_emodji = f"<:customemoji:{USD_emodji_id}>"
USDT_emodji_id = 'add id of your emodji'
USDT_emodji = f"<:customemoji:{USDT_emodji_id}>"
BUSD_emodji_id = 'add id of your emodji'
BUSD_emodji = f"<:customemoji:{BUSD_emodji_id}>"
SHIB_emodji_id = 'add id of your emodji'
SHIB_emodji = f"<:customemoji:{SHIB_emodji_id}>"
ELON_emodji_id = 'add id of your emodji'
ELON_emodji = f"<:customemoji:{ELON_emodji_id}>"
AKITA_emodji_id = 'add id of your emodji'
AKITA_emodji = f"<:customemoji:{AKITA_emodji_id}>"
Coinmarket_emodji_id = 'add id of your emodji'
Coinmarket_emodji = f"<:customemoji:{Coinmarket_emodji_id}>"
Right_emodji_id = 'add id of your emodji'
Right_emodji = f"<:customemoji:{Right_emodji_id}>"
LTC_emodji_id = 'add id of your emodji'
LTC_emodji = f"<:customemoji:{LTC_emodji_id}>"
SOL_emodji_id = 'add id of your emodji'
SOL_emodji = f"<:customemoji:{SOL_emodji_id}>"
BNB_emodji_id = 'add id of your emodji'
BNB_emodji = f"<:customemoji:{BNB_emodji_id}>"
USDC_emodji_id = 'add id of your emodji'
USDC_emodji = f"<:customemoji:{USDC_emodji_id}>"
XRP_emodji_id = 'add id of your emodji'
XRP_emodji = f"<:customemoji:{XRP_emodji_id}>"
HMSTR_emodji_id = 'add id of your emodji'
HMSTR_emodji = f"<:customemoji:{HMSTR_emodji_id}>"
TON_emodji_id = 'add id of your emodji'
TON_emodji = f"<:customemoji:{TON_emodji_id}>"
admin_tickets = "Enter you're admin tickets channel id"
link = {
    "main": "enter your link",
    "shedules": 'enter your link',
    "login": 'enter your link'
}
author_link = {
    "main": "https://github.com/Ivanskem",
    "bot-repositori": "https://github.com/Ivanskem/Python-discord-bot",
    "other-repositories": "https://github.com/Ivanskem?tab=repositories"
}

class Getrole(Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label="R-71", description="Нажмите чтобы получить группу Р-71",
                                  emoji="😉"),
            nextcord.SelectOption(label="R-72", description="Нажмите чтобы получить группу Р-72",
                                  emoji="😉"),
            nextcord.SelectOption(label="IE-71", description="Нажмите чтобы получить группу ИЭ-71",
                                  emoji="😉"),
            nextcord.SelectOption(label="IE-72", description="Нажмите чтобы получить группу ИЭ-72",
                                  emoji="😉"),
            nextcord.SelectOption(label="II-71", description="Нажмите чтобы получить группу ИИ-71",
                                  emoji="😉"),
            nextcord.SelectOption(label="II-72", description="Нажмите чтобы получить группу ИИ-72",
                                  emoji="😉")
        ]
        super().__init__(placeholder='Получить группу', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        R_71 = nextcord.utils.get(interaction.guild.roles, name='Ученик Р-71')
        R_72 = nextcord.utils.get(interaction.guild.roles, name='Ученик Р-72')
        IE_71 = nextcord.utils.get(interaction.guild.roles, name='Ученик ИЭ-71')
        IE_72 = nextcord.utils.get(interaction.guild.roles, name='Ученик ИЭ-72')
        II_71 = nextcord.utils.get(interaction.guild.roles, name='Ученик ИИ-71')
        II_72 = nextcord.utils.get(interaction.guild.roles, name='Ученик ИИ-72')

        picked_group = self.values[0]

        if picked_group == 'R-71':
            await interaction.user.add_roles(R_71, reason='Clicked getrole')
            await interaction.response.send_message(f'Вы выбрали группу Р-71 и она была выдана', ephemeral=True)
        elif picked_group == 'R-72':
            await interaction.user.add_roles(R_72, reason='Clicked getrole')
            await interaction.response.send_message(f'Вы выбрали группу Р-72 и она была выдана', ephemeral=True)
        elif picked_group == 'IE-71':
            await interaction.user.add_roles(IE_71, reason='Clicked getrole')
            await interaction.response.send_message(f'Вы выбрали группу ИЭ-71 и она была выдана', ephemeral=True)
        elif picked_group == 'IE-72':
            await interaction.user.add_roles(IE_72, reason='Clicked getrole')
            await interaction.response.send_message(f'Вы выбрали группу ИЭ-72 и она была выдана', ephemeral=True)
        elif picked_group == 'II-71':
            await interaction.user.add_roles(II_71, reason='Clicked getrole')
            await interaction.response.send_message(f'Вы выбрали группу ИИ-71 и она была выдана', ephemeral=True)
        elif picked_group == 'II-72':
            await interaction.user.add_roles(II_72, reason='Clicked getrole')
            await interaction.response.send_message(f'Вы выбрали группу ИИ-72 и она была выдана', ephemeral=True)


class GetroleView(View):
    def __init__(self):
        super().__init__()
        self.add_item(Getrole())


class Verify(Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label="Verify", description='Выдаёт роль "Верифицирован"',
                                  emoji="✔")
        ]
        super().__init__(placeholder="Пройти верификацию", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        verify_role = nextcord.utils.get(interaction.guild.roles, name='Верифицирован✅️')
        if nextcord.utils.get(interaction.user.roles, name=verify_role) is not None:
            await interaction.response.send_message(f'У вас уже есть эта роль', ephemeral=True)
        else:
            await interaction.user.add_roles(verify_role, reason='Clicked Verify')
            await interaction.response.send_message(f'{interaction.user.mention} Вам была выдана роль <@&1246041998054522880>', ephemeral=True)


class VerifyView(View):
    def __init__(self):
        super().__init__()
        self.add_item(Verify())


class Ticket(Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label='Support', description="Получение помощи от администрации или преподавателей",
                                  emoji="🛠"),
            nextcord.SelectOption(label="Bot", description="Получение помощи пользованием либо устройством бота",
                                  emoji="🤖")
        ]
        super().__init__(placeholder="Выберите категорию", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        category = self.values[0]
        await interaction.response.send_message(f'Вы выбрали {category}', ephemeral=True)
        await self.create_ticket(interaction, category)

    async def create_ticket(self, interaction: Interaction, category: str):
        channel_name = f'ticket-{interaction.user.name}'.replace(" ", "-").lower()
        member = interaction.user
        admin_role = nextcord.utils.get(interaction.guild.roles, name='Администратор')
        bot = interaction.guild.me
        default_role = interaction.guild.default_role
        overwrites = {
            default_role: nextcord.PermissionOverwrite(view_channel=False),
            member: nextcord.PermissionOverwrite(view_channel=True, send_messages=True),
            bot: nextcord.PermissionOverwrite(view_channel=True, send_messages=True),
            admin_role: nextcord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        category_channel = nextcord.utils.get(interaction.guild.categories, name='обращения')
        if category_channel is None:
            category_channel = await interaction.guild.create_category(name='обращения')

        ticket_channel = await interaction.guild.create_text_channel(name=channel_name, overwrites=overwrites,
                                                                     category=category_channel)
        action_view = TicketActionView()
        admin_tickets_id = await interaction.guild.fetch_channel(admin_tickets)
        channel_id = nextcord.utils.get(interaction.guild.channels, name=channel_name)
        embed = nextcord.Embed(title='Обращение', color=0xffffff)
        embed.add_field(name=f'{created_since_emodji} Обращение: {member.name}',
                        value=f'{slash_emodji} • Создано обращение на тему: {category}.\n'
                              f'{member_emodji} • Создал: {interaction.user.mention}')
        embed_admin = nextcord.Embed(title=f'Открытие обращения', color=0xffffff)
        embed_admin.add_field(name=f'{created_since_emodji} Тикет открыт: {interaction.user.name}',
                              value=f'{created_since_emodji} • Канал: <#{channel_id.id}>\n'
                                    f'{member_emodji} • Канал создал {interaction.user.name}')
        embed_admin.set_footer(
            text=f'• {servername_to_footer} Tickets | {datetime.datetime.now().replace(microsecond=0)}',
            icon_url=interaction.guild.icon.url)
        await admin_tickets_id.send(embed=embed_admin)
        await ticket_channel.send(embed=embed, view=action_view)


class TicketView(View):
    def __init__(self):
        super().__init__()
        self.add_item(Ticket())


class TicketAction(Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label='Close Ticket', description="Закрыть обращение.",
                                  emoji="❌"),
            nextcord.SelectOption(label="Leave Feedback", description="Оставить отзыв о работе администрации",
                                  emoji="✍")
        ]
        super().__init__(placeholder="Выберите действие", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        action = self.values[0]
        try:
            if action == 'Close Ticket':
                await interaction.response.send_modal(CloseTicketModal())
            elif action == 'Leave Feedback':
                await interaction.response.send_modal(FeedbackModal())
        except Exception:
            await interaction.response.send_message(f'Произошла ошибка с подключением попробуйте ещё раз!', ephemeral=True)


class TicketActionView(View):
    def __init__(self):
        super().__init__()
        self.add_item(TicketAction())


class CloseTicketModal(Modal):
    def __init__(self):
        super().__init__(title='Закрытие тикета')
        self.reason = TextInput(label='Причина закрытия', style=nextcord.TextInputStyle.paragraph)
        self.add_item(self.reason)

    async def callback(self, interaction: Interaction):
        logger = logging.getLogger(__name)
        reason = self.reason.value
        logger.info(f'Пользователь {interaction.user.name} закрыл тикет с причиной {reason}')
        database_location = sqlite3.connect(f'{servername_database}_discord.db')
        cursor = database_location.cursor()
        cursor.execute(
            "INSERT INTO tickets_history (guild_id, user_id, feedback_reason, close_date) VALUES (?, ?, ?, ?)",
            (interaction.guild.id, interaction.user.id, reason,
             datetime.datetime.now().replace(microsecond=0))
        )
        database_location.commit()
        database_location.close()

        channel_id = interaction.channel_id
        admin_tickets_id = await interaction.guild.fetch_channel(admin_tickets)
        embed_channel = nextcord.Embed(title=f'Закрытие обращения', color=0xffffff)
        embed_channel.add_field(name=f'{created_since_emodji} Тикет закрыл: {interaction.user.name}',
                                value=f'{slash_emodji} • Тикет был закрыт по причине: {reason}\n'
                                      f'{warn_emodji} • Тикет будет удалён через 10 минут')
        embed_channel.set_footer(
            text=f'• {servername_to_footer} Tickets | {datetime.datetime.now().replace(microsecond=0)}',
            icon_url=interaction.guild.icon.url)
        embed_admin = nextcord.Embed(title=f'Закрытие обращения', color=0xffffff)
        embed_admin.add_field(name=f'{created_since_emodji} Тикет закрыл: {interaction.user.name}',
                              value=f'{slash_emodji} • Тикет был закрыт по причине: {reason}\n'
                                    f'{created_since_emodji} • Канал: <#{channel_id}>')
        embed_admin.set_footer(
            text=f'• {servername_to_footer} Tickets | {datetime.datetime.now().replace(microsecond=0)}',
            icon_url=interaction.guild.icon.url)
        await interaction.channel.send(embed=embed_channel)
        await admin_tickets_id.send(embed=embed_admin)
        await asyncio.sleep(600)
        try:
            await interaction.channel.delete()
        except nextcord.errors.NotFound:
            logger.error(f'Произошла ошибка с удалением канала обращения!')


class FeedbackModal(Modal):
    def __init__(self):
        super().__init__(title="Оставить отзыв")
        self.feedback = TextInput(label="Отзыв", style=nextcord.TextInputStyle.paragraph)
        self.add_item(self.feedback)

    async def callback(self, interaction: nextcord.Interaction):
        logger = logging.getLogger(__name__)
        feedback = self.feedback.value
        logger.info(f'Пользователь {interaction.user.name} оставил отзыв {feedback}')
        database_location = sqlite3.connect(f'{servername_database}_discord.db')
        cursor = database_location.cursor()
        cursor.execute(
            "INSERT INTO tickets_history (guild_id, user_id, feedback_reason, close_date) VALUES (?, ?, ?, ?)",
            (interaction.guild.id, interaction.user.id, feedback,
             datetime.datetime.now().replace(microsecond=0))
        )
        database_location.commit()
        database_location.close()
        channel_id = interaction.channel_id
        admin_tickets_id = await interaction.guild.fetch_channel(admin_tickets)
        embed_channel = nextcord.Embed(title=f'Отзыв', color=0xffffff)
        embed_channel.add_field(name=f'{created_since_emodji} Отзыв оставил: {interaction.user.name}',
                                value=f'{slash_emodji} • Отзыв: {feedback}\n'
                                      f'{warn_emodji} • Просьба теперь закрыть обращение')
        embed_channel.set_footer(
            text=f'• {servername_to_footer} Tickets | {datetime.datetime.now().replace(microsecond=0)}',
            icon_url=interaction.guild.icon.url)
        embed_admin = nextcord.Embed(title=f'Отзыв', color=0xffffff)
        embed_admin.add_field(name=f'{created_since_emodji} Отзыв оставил: {interaction.user.name}',
                              value=f'{slash_emodji} • Отзыв: {feedback}\n'
                                    f'{created_since_emodji} • Канал: <#{channel_id}>')
        embed_admin.set_footer(
            text=f'• {servername_to_footer} Tickets | {datetime.datetime.now().replace(microsecond=0)}',
            icon_url=interaction.guild.icon.url)
        await interaction.channel.send(embed=embed_channel)
        await admin_tickets_id.send(embed=embed_admin)


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


def read_json(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


def giveaway_add(json_file, data):
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


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
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    categories = len(guild.categories)

    embed = nextcord.Embed(title=guild.name, color=0x6fa8dc)
    embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name='Основное', value=f'{guild_owner_emodji} Владелец: {server_owner}\n'
                                           f'{verification_level_emodji} Уровень проверки: {verification_level_show}\n'
                                           f'{created_since_emodji} Создан: <t:{int(created_at.timestamp())}:F>\n(<t:{int(created_at.timestamp())}:R>)\n'
                                           f'{slash_emodji} Всего {text_channels + voice_channels + categories} каналов\n'
                                           f'{text_emodji} Текстовые каналы: {text_channels}\n'
                                           f'{voice_emodji} Голосовые каналы: {voice_channels}\n'
                                           f'{categories_emodji} Категории: {categories}\n')
    embed.add_field(name='Пользователи', value=f'{members_emodji} Всего {total_members} участников\n'
                                               f'{bot_emodji} Ботов: {bots}\n'
                                               f'{member_emodji} Участников: {without_bot}\n')
    boost_level = guild.premium_tier
    embed.add_field(name='Бусты',
                    value=f'{boost_emodji} Уровень: {boost_level} (бустов - {guild.premium_subscription_count})\n')
    embed.add_field(name='Ссылки', value=f'{telegram_emodji} Telegram-канал: {telegram_channels_link} \n'
                                         f'{discord_emodji} Discord-сервер: {discord_server_link}\n')
    embed.set_footer(text=f'• Запрос от {interaction.user}\n• {servername_to_footer} Info {time}',
                     icon_url=interaction.user.avatar.url)
    await channel.send(embed=embed)


async def warn(interaction, guild_id, user_id, user_name, guild):
    admin_role = nextcord.utils.get(interaction.guild.roles, name="Администратор")
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
    reason = 'некорректная причина выдачи наказания!'
    embed = nextcord.Embed(title=f'{created_since_emodji} Предупреждение', color=nextcord.Color.dark_purple())
    embed.add_field(name=f'{member_emodji} {user_name} ваш было выдано предупреждение\n'
                         f'{reason_emodji} Причина: {reason}\n'
                         f'{warn_emodji} У вас {warn_count} предупреждений ', value='')
    embed.set_footer(text=f'• {servername_to_footer} Warn | {datetime.datetime.now().replace(microsecond=0)}',
                     icon_url=interaction.guild.icon.url)
    await interaction.channel.send(embed=embed)
    if warn_count >= 5:
        await interaction.user.remove_roles(admin_role, reason='too many warns')
        embed_warn = nextcord.Embed(title=f'{created_since_emodji} Снятие с администрации', color=nextcord.Color.red())
        embed_warn.add_field(name=f'{member_emodji} {user_name} Вы сняты с поста адниминистрации!',
                             value=f'{reason_emodji} Причина: Слишком много предупреждений\n'
                                   f'{warn_emodji} Чтобы оспорить наказание просим обратиться в обращения')
        embed.set_footer(text=f'• {servername_to_footer} Reset | {datetime.datetime.now().replace(microsecond=0)}',
                         icon_url=interaction.guild.icon.url)
        cursor.execute("UPDATE warn_list SET warns = 0 WHERE user_id = ?", (member.id,))
        database_location.commit()
        database_location.close()
        await interaction.channel.send(embed=embed_warn)


@client_discord.event
async def on_reaction_add(reaction: nextcord.Reaction, user: nextcord.User):
    if user.bot:
        return

    json_file = 'jsons/giveaway.json'
    giveaways = read_json(json_file)

    for giveaway in giveaways:
        if giveaway['message_id'] == reaction.message.id and reaction.emoji == '🎉':
            users = await reaction.users().flatten()
            users = [user for user in users if not user.bot]

            if users:
                winner = random.choice(users)
                await reaction.message.channel.send(
                    f'Поздравляем {winner.mention}, вы выиграли розыгрыш {giveaway["name"]}!')
            else:
                await reaction.message.channel.send('Участвующих пользователей нет!')
            giveaways.remove(giveaway)
            giveaway_add(json_file, giveaways)
            break


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
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets_history (
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                feedback_reason TEXT NOT NULL,
                close_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    database_location.commit()
    database_location.close()
    win_notification("Bot Started", f"Дискорд бот запущен\n{servername_database}_discord.db started\nTime: {datetime.datetime.now().replace(microsecond=0)}")


@client_discord.event
async def on_disconnect():
    scheduler.shutdown()
    print(f'Бот {client_discord.user} остановлен!, перезапуск')
    await asyncio.sleep(10)
    await client_discord.connect(reconnect=False)


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
    if member.avatar:
        embed_server.set_thumbnail(url=member.avatar.url)
    else:
        embed_server.set_thumbnail(url='https://cdn.discordapp.com/embed/avatars/0.png')

    embed_server.add_field(name='Информация', value='Ищи всю нужную информацию в канале "информация"')
    embed_server.set_footer(text=f'• {servername_to_footer} Welcome | {datetime.datetime.now().replace(microsecond=0)}',
                            icon_url=member.guild.icon.url)

    embed_user = nextcord.Embed(
        title=f'Привет, благодарим за присоединение к серверу "{servername_database}"',
        color=nextcord.Color.purple()
    )
    if member.avatar:
        embed_user.set_thumbnail(url=member.avatar.url)
    else:
        embed_user.set_thumbnail(url='https://cdn.discordapp.com/embed/avatars/0.png')
    embed_user.add_field(name='Информация', value=f'Всю необходимую информацию вы можете найти в канале "информация".')
    embed_user.set_footer(text=f'• {servername_to_footer} Welcome | {datetime.datetime.now().replace(microsecond=0)}',
                          icon_url=member.guild.icon.url)

    channel = nextcord.utils.get(member.guild.channels, name='добро-пожаловать')
    if channel:
        await channel.send(embed=embed_server)
    else:
        logger.error(f'Канал admin не найден, укажите верный канал!')
    try:
        await member.send(embed=embed_user)
    except nextcord.errors.HTTPException:
        logger.warning(f'Произошла ошибка отправки сообщения пользователю, скорее всего пользователь является ботом или у него закрыты личные сообщения!')


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
            embed = nextcord.Embed(title=f"{created_since_emodji} Информация о блокировке", color=nextcord.Color.dark_purple())
            embed.add_field(name=' ', value=f'{staff_emodji} Администратор: {interaction.user.mention}\n'
                                            f'{reason_emodji} Причина: {reason}\n'
                                            f'{member_emodji} Заблокированный: {member.mention}\n')
            embed.set_footer(text=f'• {servername_to_footer} Moderation |'
                                  f' {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                             icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed)
        except nextcord.Forbidden:
            logger.error('У бота не достаточно прав для блокировки пользователя!')
            await interaction.response.send_message('У меня не достаточно прав для выполнения этой команды!',
                                                    ephemeral=True)
    else:
        logger.info(f'У {interaction.user.mention} не достаточно прав для блокировки пользователя')
        await interaction.response.send_message('У вас не достаточно прав для использования этой команды!',
                                                ephemeral=True)


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
                embed.add_field(name=' ', value=f'{warn_emodji} Количество предупреждений: {warn_count[0]}\n'
                                                f'{time_emodji} Последнее предупреждение: {warn_last[0]}')
                embed.set_footer(text=f'•{servername_to_footer} Warn | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                                 icon_url=interaction.guild.icon.url)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            except TypeError:
                embed = nextcord.Embed(title='Информация', color=nextcord.Color.dark_purple())
                embed.add_field(name='', value=f'{member_emodji} {member.name} не найден в базе данных!')
                embed.set_footer(
                    text=f'•{servername_to_footer} Warn | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                    icon_url=interaction.guild.icon.url)
                await interaction.response.send_message(embed=embed, ephemeral=True)
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
            except sqlite3.Error as e:
                logger.error(f'Something went w rong. Error: {e}')
                await interaction.response.send_message(f'Произошла ошибка: {e}')
            embed = nextcord.Embed(title=f'{created_since_emodji} Предупреждение', color=nextcord.Color.dark_purple())
            embed.add_field(name='', value=f'{staff_emodji} Администратор: {interaction.user.mention}\n'
                                           f'{reason_emodji} Причина: {reason}\n'
                                           f'{warn_emodji} Предупреждённый: {member.mention}\n'
                                           f'{created_since_emodji} Количество предупреждений: {embed_result[0]}')
            embed.set_footer(text=f'• {servername_to_footer} Warn | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                             icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed)

            if embed_result[0] >= 5:
                admin_role = nextcord.utils.get(interaction.guild.roles, name="Администратор")
                await member.remove_roles(admin_role, reason='too many warns')
                embed_warn = nextcord.Embed(title=f'{created_since_emodji} Снятие с администрации',
                                            color=nextcord.Color.red())
                embed_warn.add_field(name=f'{member_emodji} {member.name} Вы сняты с поста адниминистрации!',
                                     value=f'{reason_emodji} Причина: Слишком много предупреждений\n'
                                           f'{warn_emodji} Чтобы оспорить наказание просим обратиться в обращения')
                embed.set_footer(
                    text=f'• {servername_to_footer} Reset | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                    icon_url=interaction.guild.icon.url)
                cursor.execute("UPDATE warn_list SET warns = 0 WHERE user_id = ?", (member.id,))
                database_location.commit()
                database_location.close()
                await interaction.channel.send(embed=embed_warn)
    else:
        await interaction.response.send_message(f'У вас недостаточно прав для использования этой команды!',
                                                ephemeral=True)


@client_discord.slash_command(name='kick', description='Удаляет участника, участник сможет зайти повторно')
async def kick(interaction: Interaction, member: nextcord.Member,
               reason: str = SlashOption(description='Причина удаления', default="Причина не указана")):
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
                    INSERT INTO mod_actions (action_type, guild_id, moderator_name, moderator_id, target_user_name,
                     target_user_id, reason, action_time) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, ('Kick', interaction.guild.id, interaction.user.name, interaction.user.id, member.name, member.id,
                      reason,
                      datetime.datetime.now()))
                database_location.commit()
            except sqlite3.Error as e:
                logger.error(f'Something went wrong! Error: {e}')
            finally:
                database_location.close()
            if reason in ['Причина не указана']:
                await warn(interaction, interaction.guild.id, interaction.user.id,
                           interaction.user.name, interaction.guild)
            embed = nextcord.Embed(title=f"{created_since_emodji} Информация о удалении",
                                   color=nextcord.Color.dark_purple())
            embed.add_field(name=' ', value=f'{staff_emodji} Администратор: {interaction.user.mention}\n'
                                            f'{reason_emodji} Причина: {reason}\n'
                                            f'{member_emodji} Удалённый: {member.mention}')
            embed.set_footer(text=f'• {servername_to_footer} Kick | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                             icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed)
        except nextcord.Forbidden:
            logger.error('У бота не достаточно прав для удаления пользователя!')
            await interaction.response.send_message('У меня не достаточно прав для выполнения этой команды!',
                                                    ephemeral=True)
    else:
        logger.info(f'У {interaction.user.mention} не достаточно прав для удаления пользователя')
        await interaction.response.send_message('У вас не достаточно прав для использования этой команды!',
                                                ephemeral=True)


@client_discord.slash_command(name='server-info', description='Выводит статистику сервера')
async def serverinfo(interaction: Interaction,
                     type: str = SlashOption(description='Выберите какой тип статистики вы хотите вывести: новая или старая',
                                             choices=['new', 'old'],
                                             default='new')):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.mention} вызвал команду вывода статистики сервера')
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        if type == 'new':
            guild = interaction.guild
            bots = sum(1 for member in guild.members if member.bot)
            total_members = guild.member_count
            without_bot = total_members - bots

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
            text_channels = len(guild.text_channels)
            voice_channels = len(guild.voice_channels)
            categories = len(guild.categories)

            embed = nextcord.Embed(title=guild.name, color=0x6fa8dc)
            embed.set_thumbnail(url=guild.icon.url)
            embed.add_field(name='Основное', value=f'{guild_owner_emodji} Владелец: {server_owner}\n'
                                              f'{verification_level_emodji} Уровень проверки: {verification_level_show}\n'
                                              f'{created_since_emodji} Создан: <t:{int(created_at.timestamp())}:F>\n(<t:{int(created_at.timestamp())}:R>)\n'
                                              f'{slash_emodji} Всего {text_channels + voice_channels + categories} каналов\n'
                                              f'{text_emodji} Текстовые каналы: {text_channels}\n'
                                              f'{voice_emodji} Голосовые каналы: {voice_channels}\n'
                                              f'{categories_emodji} Категории: {categories}\n')
            embed.add_field(name='Пользователи', value=f'{members_emodji} Всего {total_members} участников\n'
                                                       f'{bot_emodji} Ботов: {bots}\n'
                                                       f'{member_emodji} Участников: {without_bot}\n')
            boost_level = guild.premium_tier
            embed.add_field(name='Бусты', value=f'{boost_emodji} Уровень: {boost_level} (бустов - {guild.premium_subscription_count})\n')
            embed.add_field(name='Ссылки', value=f'{telegram_emodji} Telegram-канал: {telegram_channels_link} \n'
                                                 f'{discord_emodji} Discord-сервер: {discord_server_link}\n')
            embed.set_footer(text=f'• Запрос от {interaction.user}\n• {servername_to_footer} Info | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
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
                embed.set_footer(text=f'• Запрос от {interaction.user}\n• {servername_to_footer} Info {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
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
        guild = interaction.guild
        members_info = [f"{member_emodji} {member.mention}-{member.name} (ID: {member.id}) (Высшая роль: {member.top_role})" for member
                        in guild.members]

        embed = nextcord.Embed(title=f'{created_since_emodji} Участники сервера', description='\n'.join(members_info), color=0xffffff)
        embed.set_footer(text=f'• {servername_to_footer} Info {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n• На сервере {guild.member_count} участников',
                         icon_url=interaction.guild.icon.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(f'{interaction.user.mention}. У вас недостаточно прав для использования этой команды!', ephemeral=True)


@client_discord.slash_command(name='mute-list', description='Выводит список заглушённых пользователей')
async def mute_list(interaction: Interaction):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.name} вызвал команду для списка заглушённых пользователей')
    if nextcord.utils.get(interaction.user.roles, name="Администратор"):

        mutes = [f'{member_emodji} {member.mention} (Высшая роль: {member.top_role})' for member in interaction.guild.members
                 if nextcord.utils.get(member.roles, name='Muted')]
        mutes_count = len(mutes)
        embed = nextcord.Embed(title=f'{created_since_emodji} Список заглушённых участников', description='\n'.join(mutes),
                               color=nextcord.Color.dark_purple())
        embed.set_footer(text=f'• {servername_to_footer} Info | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\nНа сервере {mutes_count} заглушённых.',
                         icon_url=interaction.guild.icon.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        interaction.response.send_message(f'{interaction.user.mention}. У вас недостаточно прав для использования этой команды!', ephemeral=True)


@client_discord.slash_command(name='ban-list', description='Выводит список заблокированных пользователей')
async def ban_list(interaction: Interaction):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.name} использовал команду для вывода списка заблокированных пользователей')
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        ban_list = []
        async for ban_entry in interaction.guild.bans():
            ban_list.append(f'{member_emodji} {ban_entry.user} (Причина: {ban_entry.reason})')
        ban_count = len(ban_list)
        embed = nextcord.Embed(title=f'{created_since_emodji} Список заблокированных', description='\n'.join(ban_list),
                               color=0xffffff)
        embed.set_footer(
            text=f'• {servername_to_footer} Info | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
                 f'• На сервере {ban_count} заблокированных.',
            icon_url=interaction.guild.icon.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message("У вас нет прав на просмотр списка заблокированных.", ephemeral=True)


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
        embed = nextcord.Embed(title="Доступные команды сервера", color=0x999999)
        embed.add_field(
            name=f'Основные',
            value=f'**/help**\n'
                  f'**/avatar**\n'
                  f'**/weather**\n'
                  f'**/info**\n'
                  f'**/links**\n'
                  f'**/author-links**\n'
                  f'**/invites**\n',
            inline=True
        )
        embed.set_footer(text=f'• {servername_to_footer} Help | {datetime.datetime.now().replace(microsecond=0)}',
                         icon_url=interaction.guild.icon.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    elif rank == 'mod':
        if nextcord.utils.get(interaction.user.roles, name='Администратор') is not None:
            logger.info(
                f'Пользователь {interaction.user.mention} вызвал команду для вывода списка команд. Ранг: Модерация')
            embed = nextcord.Embed(title=f"{created_since_emodji} Доступные команды сервера. Ранг модерация {created_since_emodji}",
                                   description=f'Бот использует слэш-команды (/), Ниже представлены доступные команды:',
                                   color=0x999999)
            embed.add_field(
                name=f'Основные',
                value=f'**/help**\n'
                      f'**/avatar**\n'
                      f'**/weather**\n'
                      f'**/info**\n'
                      f'**/links**\n'
                      f'**/author-links**\n'
                      f'**/invites**\n',
                inline=True
            )
            embed.add_field(
                name=f'Администрация\n',
                value=f'**/kick**\n'
                      f'**/ban**\n'
                      f'**/unban**\n'
                      f'**/mute**\n'
                      f'**/unmute**\n'
                      f'**/warn**\n'
                      f'**/mute-list**\n'
                      f'**/ban-list**',
                inline=True
            )
            embed.add_field(
                name=f'Другое',
                value=f'**/clear**\n'
                      f'**/members**\n'
                      f'**/server-info**\n'
                      f'**/say**\n'
                      f'**/log**\n'
                      f'**/database**\n'
                      f'**/channel-info**\n'
                      f'**/bot-info**\n'
                      f'**/verify-menu**\n'
                      f'**/ticket-menu**\n'
                      f'**/getrole-menu**\n',
                inline=True
            )
            embed.set_footer(text=f'• {servername_to_footer} Help | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
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
            embed = nextcord.Embed(title=f"{created_since_emodji} Информация о заглушении", color=nextcord.Color.dark_purple())
            embed.add_field(name=' ', value=f'{staff_emodji} Администратор: {interaction.user.mention}\n'
                                            f'{reason_emodji} Причина: {reason}\n'
                                            f'{member_emodji} Заглушённый: {member.mention}')
            embed.set_footer(text=f'• {servername_to_footer} Moderation | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
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
                mute_role = await interaction.guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False, speak=False))
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
            embed = nextcord.Embed(title=f'{created_since_emodji} Информации о разглушении', color=nextcord.Color.dark_purple())
            embed.add_field(name=' ', value=f'{staff_emodji} Администратор: {interaction.user.mention}\n'
                                            f'{reason_emodji} Причина: {reason}\n'
                                            f'{member_emodji} Разглушённый: {member.mention}')
            embed.set_footer(text=f'• {servername_to_footer} Moderation | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
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
            embed = nextcord.Embed(title=f'{created_since_emodji} Информация о разблокировке', color=nextcord.Color.dark_purple())
            embed.add_field(name=' ', value=f'{staff_emodji}Администратор: {interaction.user.mention}\n'
                                            f'{reason_emodji} Причина: {reason}\n'
                                            f'{member_emodji} Разблокированный: {user.mention}\n')
            embed.set_footer(
                text=f'• {servername_to_footer} Moderation | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                icon_url=interaction.guild.icon.url)

            if reason == 'Причина не указана':
                await warn(interaction, interaction.guild.id, interaction.user.id,
                           interaction.user.name, interaction.guild)

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
    excepted_roles = ["@everyone", "Member"]
    role_count = len([role.name for role in member.roles if role.name not in excepted_roles])
    roles = member.roles
    role_names = [f'<@&{role.id}>' for role in roles if role.name not in excepted_roles]
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
    embed.add_field(name="Роль:", value=f'<@&{member.top_role.id}>', inline=True)
    embed.add_field(name="Роли:", value=role_list)
    embed.add_field(name='Количество ролей:', value=role_count)
    embed.set_footer(text=f'• {servername_to_footer} Info | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                     icon_url=interaction.guild.icon.url)
    if hidden == 'hidden':
        await interaction.response.send_message(embed=embed, ephemeral=True)
    elif hidden == 'shown':
        await interaction.response.send_message(embed=embed, ephemeral=False)


@client_discord.slash_command(name='say', description='Отправляет сообщение от имени бота')
async def say(interaction: Interaction, message: str = SlashOption(description='Отправляет текст введённый здесь')):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.mention} вызвал команду для отправки сообщения от имени бота')
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        await interaction.channel.send(message)
        await interaction.response.send_message('Сообщение успешно отправленно', ephemeral=True)
        logger.info(f'Пользователь {interaction.user.name} отправил ({message}) от имени бота')
    else:
        await interaction.response.send_message(f'У вас недостаточно прав для использования этой команды', ephemeral=True)


@client_discord.slash_command(name='avatar', description='Отпраляет аватарку пользователя')
async def avatar(interaction: Interaction, member: nextcord.Member):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.mention} использовал команду для вывода аватара пользователя')
    embed = nextcord.Embed(title=f'Аватар {member.name}', color=0xffffff)
    embed.set_image(url=member.avatar.url)
    embed.set_footer(text=f'• {servername_to_footer} Info | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
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
                        win_notification('User clear archive logs', f'{interaction.user.name} cleared archive log files\nTime: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
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
                    win_notification('User clear current log', f'{interaction.user.name} cleared main logging file\nTime: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
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
                                     f'{interaction.user.name} downloaded archive log files\nTime: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
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
                                 f'{interaction.user.name} rewrited current log file\nTime: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
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
                    text=f'• {servername_to_footer} Log | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
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
            embed.set_footer(text=f'• {servername_to_footer} Weather | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                             icon_url=interaction.guild.icon.url)
            logger.info(f"Прогноз погоды для города {city} успешно выведен.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except requests.exceptions.HTTPError as e:
            logger.error(f"Ошибка HTTP: {e}")
            embed = nextcord.Embed(title=f"Ошибка", color=0xff0000)
            embed.add_field(name=f"Ошибка получения данных", value='Сервер недоступен')
            embed.set_footer(
                text=f'• {servername_to_footer} Weather | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка запроса: {e}")
            embed = nextcord.Embed(title=f"Ошибка", color=0xff0000)
            embed.add_field(name=f"Ошибка получения данных", value='Ошибка с запросом попробуйте снова')
            embed.set_footer(
                text=f'• {servername_to_footer} Weather | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        logger.error(f"Ошибка: Не удалось получить данные погоды. Код ответа: {response.status_code}")
        embed = nextcord.Embed(title=f"Ошибка", color=0xff0000)
        embed.add_field(name=f"Ошибка получения данных", value='')
        embed.set_footer(text=f'• {servername_to_footer} Weather | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
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
                users_data = [(member.id, member.name, member.mention, member.joined_at) for member in
                              interaction.guild.members]
                cursor.executemany(
                    "INSERT OR IGNORE INTO users_list (user_id, user_name, user_mention, user_joined_date) VALUES (?, ?, ?, ?)",
                    users_data)
                cursor.execute("""
                            CREATE TABLE IF NOT EXISTS tickets_reputation (
                                guild_id INTEGER NOT NULL,
                                user_id INTEGER NOT NULL,
                                user_name TEXT NOT NULL
                            )
                        """)
                admin_list = [(interaction.guild.id, member.id, member.name) for member in interaction.guild.members
                              if 'Администратор' in member.roles]
                cursor.executemany("INSERT OR IGNORE INTO tickets_reputation (guild_id, user_id, user_name) VALUES (?, ?, ?)", admin_list)

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
                    text=f'• {servername_to_footer} Database | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                    icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message('У вас нет прав для выполнения этой команды.')


@client_discord.slash_command(name='ticket-menu', description='Вывод сообщения для системы обращений')
async def menu(interaction: Interaction):
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        view = TicketView()
        embed = nextcord.Embed(title="Тикет поддержки", color=0xffffff)
        embed.add_field(name=f'{created_since_emodji} • Чтобы открыть билет поддержки, выберите категорию ниже:',
                        value=f'{reason_emodji} • Описывайте свою просьбу или проблему как можно подробнее,'
                              f' чтобы вам смогли помочь как можно быстрее.')
        embed.set_footer(
            text=f'• {servername_to_footer} Tickets | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
            icon_url=interaction.guild.icon.url)
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message(f'Сообщение успешно отправлено', ephemeral=True)
    else:
        await interaction.response.send_message(f'У вас недостаточно прав для вызова этой команды!', ephemeral=True)


@client_discord.slash_command(name='verify-menu', description='Вывод сообщения для системы верификации')
async def menu(interaction: Interaction):
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        view = VerifyView()
        embed = nextcord.Embed(title='Получение роли', color=0xffffff)
        embed.add_field(name=f'{created_since_emodji} • Нажмите кнопку ниже',
                        value=f'{reason_emodji} • Чтобы получить роль <@&1246041998054522880>\n'
                              f'{warn_emodji} • Вам нужно нажать на кнопку ниже и выбрать "Verify"')
        embed.set_footer(
            text=f'• {servername_to_footer} Verify | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
            icon_url=interaction.guild.icon.url)
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message(f'Сообщение успешно отправлено', ephemeral=True)
    else:
        await interaction.response.send_message(f'У вас недостаточно прав для использования этой команды!', ephemeral=True)


@client_discord.slash_command(name='getrole-menu', description='Вывод сообщения для системы выбора группы')
async def menu(interaction: Interaction):
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        view = GetroleView()
        embed = nextcord.Embed(title='Получение группы', color=0xffffff)
        embed.add_field(name=f'{created_since_emodji} • Нажмите кнопку ниже',
                        value=f'{reason_emodji} • Чтобы получить вашу группу\n'
                              f'{warn_emodji} • Вам нужно нажать на кнопку ниже и выбрать вашу группу')
        embed.set_footer(
            text=f'• {servername_to_footer} Verify | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
            icon_url=interaction.guild.icon.url)
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message(f'Сообщение успешно отправлено', ephemeral=True)
    else:
        await interaction.response.send_message(f'У вас недостаточно прав для использования этой команды!', ephemeral=True)


@client_discord.slash_command(name='links', description='Вывод списка ссылок учреждений')
async def links(interaction: Interaction):
    logger = logging.getLogger(__name__)
    logger.info(f'{created_since_emodji} Пользователь {interaction.user.name} использовал команду для вывода ссылок')
    embed = nextcord.Embed(title=f'{created_since_emodji} Ссылки', color=0x8b00ff)
    embed.add_field(name=f'{created_since_emodji} Здесь представленны оффициальные ссылки на ресурсы учреждения:',
                    value=f'{link_emodji} Основной сайт: {link["main"]}\n'
                          f'{link_emodji} Страница расписания: {link["shedules"]}\n'
                          f'{link_emodji} Страница входа:  {link["login"]}')
    embed.set_footer(
        text=f'• {servername_to_footer} Links | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
        icon_url=interaction.guild.icon.url)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='author-links', description='Вывод списка ссылок автора бота')
async def author_links(interaction: Interaction):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.name} использовал команду для вывода списка ссылок автора бота')
    embed = nextcord.Embed(title=f'{created_since_emodji} Ссылки', color=0xffffff)
    embed.add_field(name=f'{created_since_emodji} Здесь представленны ссылки на автора(создателя) бота',
                    value=f'{link_emodji} Страница создателя: {author_link["main"]}\n'
                          f'{link_emodji} Репозиторий бота: {author_link["bot-repositori"]}\n'
                          f'{link_emodji} Остальные репозитории: {author_link["other-repositories"]}')
    embed.set_footer(
        text=f'• {servername_to_footer} Links | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
        icon_url=interaction.guild.icon.url)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='invites', description='Вывод списка ссылок для приглашений')
async def invite(interaction: Interaction):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.name} использовал команду для вывода списка ссылок для приглашений')
    invites = await interaction.guild.invites()
    embed = nextcord.Embed(title=f'{created_since_emodji} Здесь представленны ссылки для приглашения на сервер:', color=0xffffff)
    if not invites:
        embed.add_field(name=f'{created_since_emodji} Здесь представленны ссылки для приглашения на сервер:',
                        value=f'{link_emodji} В данный момент на сервере нет активных ссылок!')
    else:
        for invite in invites:
            embed.add_field(name=f'{created_since_emodji} Приглашение от {invite.inviter}',
                            value=f'{link_emodji} Ссылка: {invite.url}\n'
                                  f'{members_emodji} Использованно {invite.uses} раз\n'
                                  f'{warn_emodji} Создано: {invite.created_at.strftime("%Y-%m-%d %H:%M")}\n'
                                  f'{warn_emodji} Удалится: {invite.expires_at.strftime("%Y-%m-%d %H:%M")}')
    embed.set_footer(
        text=f'• {servername_to_footer} Invites | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
        icon_url=interaction.guild.icon.url)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='bot-info', description='Вывод информации о боте')
async def info(interaction: Interaction):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.name} использовал команду для вывода ')
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        member = interaction.guild.me
        excepted_roles = ["@everyone", "Member"]
        role_count = len([f'<@&{role.id}>' for role in member.roles if role.name not in excepted_roles])
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
        embed.add_field(name="Роль:", value=f'<@&{member.top_role.id}>', inline=True)
        embed.add_field(name="Роли:", value=role_list)
        embed.add_field(name='Количество ролей:', value=role_count)
        embed.set_footer(text=f'• {servername_to_footer} Info | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                         icon_url=interaction.guild.icon.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='channel-info', description='Вывод информацию о указанном канале')
async def channel_info(interaction: Interaction,
                       channel: nextcord.abc.GuildChannel = SlashOption(
                           description='Выводит информацию о выбранном канале',
                           channel_types=[ChannelType.text, ChannelType.voice, ChannelType.category, ChannelType.forum, ChannelType.stage_voice]
                       )):
    logger = logging.getLogger(__name__)
    logger.info(f'Пользователь {interaction.user.name} использовал команду для информации о {channel} канале')
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        embed = nextcord.Embed(title=f'{created_since_emodji} Канал {channel.name}', color=0xffffff)
        embed.add_field(name='Channel ID:', value=channel.id, inline=True)
        embed.add_field(name='Channel Name:', value=channel.name, inline=True)
        embed.add_field(name='Channel Type:', value=channel.type, inline=True)
        if isinstance(channel, nextcord.TextChannel):
            embed.add_field(name='Topic:', value=channel.topic or 'No topic found', inline=True)
            embed.add_field(name='NSFW:', value=channel.is_nsfw(), inline=True)
        if isinstance(channel, nextcord.VoiceChannel):
            embed.add_field(name='Bitrate:', value=channel.bitrate, inline=True)
            embed.add_field(name='User Limit:', value=channel.user_limit, inline=True)
            embed.add_field(name='Quality:', value=channel.video_quality_mode, inline=True)
        if isinstance(channel, nextcord.ForumChannel):
            embed.add_field(name='Tags:', value='\n'.join([f'{tags.name} ({tags.id})' for tags in channel.available_tags]), inline=True)
            embed.add_field(name='NSFW:', value=channel.is_nsfw(), inline=True)
        if isinstance(channel, nextcord.CategoryChannel):
            embed.add_field(name='Channels:', value='\n'.join([f'{channels.name} ({channels.type})' for channels in channel.channels]), inline=True)
            embed.add_field(name='Position:', value=channel.position, inline=True)
        if isinstance(channel, nextcord.StageChannel):
            embed.add_field(name='User Limit:', value=channel.user_limit, inline=True)
            embed.add_field(name='Bitrate:', value=channel.bitrate, inline=True)
        embed.add_field(name='Created At', value=channel.created_at.strftime("%m-%d %H:%M"), inline=True)
        embed.set_footer(text=f'• {servername_to_footer} Info | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                         icon_url=interaction.guild.icon.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(f'У вас недостаточно прав для использования этой команды!', ephemeral=True)


@client_discord.slash_command(name='giveaway')
async def giveaway(interaction: Interaction,
                   action: str = SlashOption(
                       description='Выберите что хотите сделать',
                       choices=['create', 'delete', 'list']
                   ),
                   name: str = SlashOption(
                       description='Введите название розыгрыша',
                       default=None
                   ),
                   text: str = SlashOption(
                       description='Введите текст для правил участния',
                       default=None
                   ),
                   prize: str = SlashOption(
                       description='Введите название приза',
                       default=None
                   ),
                   expires_at: int = SlashOption(
                       description='Введите через сколько дней розыгрыш будет окончен',
                       default=None
                   )):
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        if action == 'create':
            if not any(param is None for param in [name, text, prize, expires_at]):
                time_delta = datetime.timedelta(days=expires_at)
                new_giveaway = {
                    'name': name,
                    'text': text,
                    'prize': prize,
                    'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'expires_at': (datetime.datetime.now() + time_delta).strftime('%Y-%m-%d %H:%M:%S')
                }
                json_file = 'jsons/giveaway.json'
                data = read_json(json_file)
                if not isinstance(data, list):
                    data = []
                data.append(new_giveaway)
                giveaway_add(json_file, data)

                embed = nextcord.Embed(title='Розыгрыш', color=0xffffff)
                embed.add_field(name='Название:', value=name)
                embed.add_field(name='Условия:', value=text + '\nВсем удачи!')
                embed.add_field(name='Приз:', value=prize)
                embed.add_field(name='Окончание:',
                                value=f'<t:{int((datetime.datetime.now() + time_delta).timestamp())}:F>')

                message = await interaction.channel.send(embed=embed)

                await message.add_reaction('🎉')

                giveaway_data = {
                    'message_id': message.id,
                    'channel_id': interaction.channel.id,
                    'name': name
                }
                giveaways = read_json('jsons/giveaways.json')
                giveaways.append(giveaway_data)
                giveaway_add('jsons/giveaways.json', giveaways)
            else:
                await interaction.response.send_message(f'Заполните все данные для создания розыгрыша!', ephemeral=True)

        elif action == 'delete':
            json_file = 'jsons\\giveaway.json'
            data = read_json(json_file)
            data = [item for item in data if item.get('name') != name]
            giveaway_add(json_file, data)
            await interaction.response.send_message(f'Розыгрыш {name} удалён', ephemeral=True)
        elif action == 'list':
            json_file = 'jsons\\giveaway.json'
            json_data = read_json(json_file)
            embed = nextcord.Embed(title='Список доступных розыгрышей:', color=0xffffff)
            count = 0
            for data in json_data:
                count += 1
                embed.add_field(name=f'Номер:',
                                value=count)
                embed.add_field(name='Название:',
                                value=data.get('name', 'Not found'))
                embed.add_field(name='Условия (текст)',
                                value=data.get('text', 'Not found'))
                embed.add_field(name='Награда:',
                                value=data.get('prize', 'Not found'))
                embed.add_field(name='Создано:',
                                value=data.get('created_at', 'Not found'))
                embed.add_field(name='Окончится:',
                                value=data.get('expires_at', 'Not found'))
            await interaction.response.send_message(embed=embed, ephemeral=True)

    else:
        await interaction.response.send_message(f'У вас не достаточно прав для использования этой команды', ephemeral=True)


@client_discord.slash_command(name='crypto-difference', description='Выводит информацию о криптовалюте')
async def crypto_difference(interaction: Interaction,
                 crypto_currency: str = SlashOption(
                     name='crypto',
                     description='Введите название криптовалюты в формате: USDT, BTC, или ETH',
                     choices=['BTC', 'ETH', 'DOGE', 'USDT', 'BUSD', 'SHIB', 'ELON', 'AKITA']
                 ),
                 convert_currency: str = SlashOption(
                     name='convert',
                     description='Введите валюту в которую нужно конвертировать криптовалюту. Формат: UST, BTC, RUB',
                     choices=['BTC', 'ETH', 'DOGE', 'USDT', 'RUB', 'USD', 'BUSD', 'SHIB', 'ELON', 'AKITA']
                 )):
    if crypto_currency == 'USDT':
        crypto_currency_emoji = USDT_emodji
    elif crypto_currency == 'BTC':
        crypto_currency_emoji = BTC_emodji
    elif crypto_currency == 'DOGE':
        crypto_currency_emoji = DOGE_emodji
    elif crypto_currency == 'ETH':
        crypto_currency_emoji = ETH_emodji
    elif crypto_currency == 'BUSD':
        crypto_currency_emoji = BUSD_emodji
    elif crypto_currency == 'SHIB':
        crypto_currency_emoji = SHIB_emodji
    elif crypto_currency == 'ELON':
        crypto_currency_emoji = ELON_emodji
    elif crypto_currency == 'AKITA':
        crypto_currency_emoji = AKITA_emodji
    if convert_currency == 'USD':
        convert_currency_emoji = USD_emodji
    elif convert_currency == 'USDT':
        convert_currency_emoji = USDT_emodji
    elif convert_currency == 'BTC':
        convert_currency_emoji = BTC_emodji
    elif convert_currency == 'ETH':
        convert_currency_emoji = ETH_emodji
    elif convert_currency == 'DOGE':
        convert_currency_emoji = DOGE_emodji
    elif convert_currency == 'RUB':
        convert_currency_emoji = RUB_emodji
    elif convert_currency == 'BUSD':
        convert_currency_emoji = BUSD_emodji
    elif convert_currency == 'SHIB':
        convert_currency_emoji = SHIB_emodji
    elif convert_currency == 'ELON':
        convert_currency_emoji = ELON_emodji
    elif convert_currency == 'AKITA':
        convert_currency_emoji = AKITA_emodji
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    parameters = {
        'symbol': crypto_currency,
        'convert': convert_currency
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_Crypto,
    }
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()
    price_difference = data['data'][crypto_currency]['quote'][convert_currency]['price']
    change_24h = data['data'][crypto_currency]['quote'][convert_currency]['percent_change_24h']
    embed = nextcord.Embed(title=f'{created_since_emodji}Информация о криптовалюте', color=0xffffff)
    embed.add_field(name=f'{slash_emodji} Соотношение {crypto_currency} к {convert_currency}',
                    value=f'{crypto_currency_emoji} Выбранная валюта: {crypto_currency}\n'
                          f"🔃 Разница: {price_difference:,.1f}\n"
                          f'{convert_currency_emoji} Конвертировать в: {convert_currency}\n'
                          f'🔄 Изменения за 24 часа: {change_24h}%')
    embed.set_footer(
        text=f'• {servername_to_footer} Crypto | https://coinmarketcap.com/ | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
        icon_url='https://logos-world.net/wp-content/uploads/2023/02/CoinMarketCap-Logo.png')
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='crypto-trending', description='Выводит список последних добавленных токенов на coinmarketcap')
async def crypto_trending(interaction: Interaction,
                          limit: int = SlashOption(
                            description='Выберите количество токенов в списке максимальное количество - 10',
                            choices=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
                            default=5
                          )):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_Crypto,
    }

    parameters = {
        'sort': 'volume_24h',
        'limit': limit
    }

    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()
    if 'data' not in data:
        await interaction.response.send_message(f"Произошла ошибка при получении данных: {data}", ephemeral=True)
        return

    embed = nextcord.Embed(title=f'Топ {limit} по востребованности на (https://coinmarketcap.com/)', color=0xffffff)
    for crypto in data['data']:
        tags = crypto.get("tags", [])
        tags_str = ', '.join(tags)
        embed.add_field(name=f'{created_since_emodji} Название: {crypto["name"]}',
                        value=f'{created_since_emodji} ID: {crypto["id"]}\n'
                              f'{created_since_emodji} Символ: {crypto["symbol"]}\n'
                              f'{created_since_emodji} Теги: {tags_str if tags else "Нет тегов"}\n'
                              f'{created_since_emodji} Дата добавления: {crypto.get("date_added", "N/A").split("T")[0]}')
        embed.set_footer(
            text=f'• {servername_to_footer} Crypto | https://coinmarketcap.com/ | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
            icon_url='https://logos-world.net/wp-content/uploads/2023/02/CoinMarketCap-Logo.png')
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='crypto-info', description='Вывод информацию о выбранной криптовалюте')
async def crypto_info(interaction: Interaction,
                      crypto: str = SlashOption(
                          description='Выберите криптовалюту о которой хотите получить информацию',
                          choices=['BTC', 'ETH', 'DOGE', 'USDT', 'BUSD', 'SHIB', 'ELON', 'AKITA', 'SOL', 'BNB', 'USDC', 'XRP', 'TON', 'LTC']
                      )):
    if crypto is None:
        await interaction.response.send_message(f'Выберите криптовалю!', ephemeral=True)
        return

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    if crypto == 'USDT':
        crypto_emoji = USDT_emodji
    elif crypto == 'BTC':
        crypto_emoji = BTC_emodji
    elif crypto == 'DOGE':
        crypto_emoji = DOGE_emodji
    elif crypto == 'ETH':
        crypto_emoji = ETH_emodji
    elif crypto == 'BUSD':
        crypto_emoji = BUSD_emodji
    elif crypto == 'SHIB':
        crypto_emoji = SHIB_emodji
    elif crypto == 'ELON':
        crypto_emoji = ELON_emodji
    elif crypto == 'AKITA':
        crypto_emoji = AKITA_emodji
    elif crypto == 'SOL':
        crypto_emoji = SOL_emodji
    elif crypto == 'BNB':
        crypto_emoji = BNB_emodji
    elif crypto == 'USDC':
        crypto_emoji = USDC_emodji
    elif crypto == 'XRP':
        crypto_emoji = XRP_emodji
    elif crypto == 'TON':
        crypto_emoji = TON_emodji
    elif crypto == 'LTC':
        crypto_emoji = LTC_emodji
    parameters = {
        'symbol': crypto,
        'convert': 'USD'
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_Crypto
    }
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()
    crypto_data = data['data'][crypto]
    embed = nextcord.Embed(title=f'{created_since_emodji} Информация о криптовалюте', color=0xffffff)
    embed.add_field(name=f'{crypto_emoji} {crypto_data["name"]}',
                    value=f'{crypto_emoji} Symbol: {crypto_data["symbol"]}\n'
                          f'{crypto_emoji} ID: {crypto_data["id"]}\n'
                          f'{Right_emodji} Price: ${crypto_data["quote"]["USD"]["price"]:.2f}\n'
                          f'{Right_emodji} Market cap: ${crypto_data["quote"]["USD"]["market_cap"]:.2f}\n'
                          f'{Right_emodji} Volume 24h: ${crypto_data["quote"]["USD"]["volume_24h"]:.2f}\n'
                          f'{Right_emodji} % Change 24h: {crypto_data["quote"]["USD"]["percent_change_24h"]:.2f}%\n'
                          f'{Right_emodji} Circulating Supply: {crypto_data["circulating_supply"]}\n'
                          f'{Right_emodji} Page: https://coinmarketcap.com/currencies/{crypto_data["name"]}/')
    embed.set_footer(
        text=f'• {servername_to_footer} Crypto | https://coinmarketcap.com/ | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
        icon_url='https://logos-world.net/wp-content/uploads/2023/02/CoinMarketCap-Logo.png')
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='crypto-list', description='Выводит список всех доступных криптовалют')
async def crypto_list(interaction: Interaction,
                      all: bool = SlashOption(
                          description='Все ли должны выводится криптовалюты?',
                          choices=['True', 'False'],
                          default=False
                      )):
    if all is False:
        embed = nextcord.Embed(title=f'{created_since_emodji} Список доступных криптовалют', description=f'{created_since_emodji} **Жирным** текстом выделены основные криптовалюты', color=0xffffff)
        embed.add_field(name=f'{text_emodji} Список',
                        value=f'{BTC_emodji} **BTC** - **Bitcoin**\n'
                              f'{LTC_emodji} **LTC** - **Litecoin**\n'
                              f'{ETH_emodji} **ETH** - **Ethereum**\n'
                              f'{USDT_emodji} **USDT** - **Tether** **USD**\n'
                              f'{USDC_emodji} USDC - USDC\n'
                              f'{BNB_emodji} BNB - BNB\n'
                              f'{TON_emodji} **TON** - **Toncoin**\n'
                              f'{DOGE_emodji} DOGE - Dogecoin\n'
                              f'{BUSD_emodji} **BUSD** - **Binance USD**\n'
                              f'{ELON_emodji} ELON - ELON\n'
                              f'{AKITA_emodji} AKITA - Akita Inu\n'
                              f'{SHIB_emodji} SHIB - Shiba Inu\n'
                              f'{XRP_emodji} **XRP** - **XRP**'
                        )
        embed.set_footer(
            text=f'• {servername_to_footer} Crypto | https://coinmarketcap.com/ | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
            icon_url='https://logos-world.net/wp-content/uploads/2023/02/CoinMarketCap-Logo.png')
        await interaction.response.send_message(embed=embed, ephemeral=True)
    if all is True:
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': API_Crypto
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        if response.status_code == 200:
            cryptocurrencies = [f"{created_since_emodji} **{crypto['name']} - {crypto['symbol']} ({crypto.get('date_added', 'N/A').split('T')[0]}) [{crypto['quote']['USD']['percent_change_24h']:.2f}%]**"
                                for crypto in data['data']]
        else:
            interaction.response.send_message(f'Ошибка запроса. Код: {response.status_code}')
        embed = nextcord.Embed(title=f'{created_since_emodji} Список доступных криптовалют',
                               description=f'\n'.join(cryptocurrencies[:50]),
                               color=0xffffff)
        embed.set_footer(
            text=f'• {servername_to_footer} Crypto | https://coinmarketcap.com/ | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
            icon_url='https://logos-world.net/wp-content/uploads/2023/02/CoinMarketCap-Logo.png')
        await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='crypto', description='Выводит список команд для криптовалюты')
async def crypto(interaction: Interaction):
    embed = nextcord.Embed(title='Помощь по использованию команд с заголовком crypto', color=0xffffff)
    embed.add_field(name=f'Использование: Crypto-info',
                    value=f'{created_since_emodji} /crypto-info crypto:x\n'
                          f'{created_since_emodji} x - Название криптовалюты о которой вы хотите получить информацию\n'
                          f'{created_since_emodji} Выбираете криптовалюту из списка и получаете информацию\n',
                    inline=False)
    embed.add_field(name=f'Использование: Crypto-exchange',
                    value=f'{created_since_emodji} /crypto-exchange name:x\n'
                          f'{created_since_emodji} x - Название криптобиржи о которой вы хотите получить информацию\n'
                          f'{created_since_emodji} Вводить биржу самостоятельно lowercase типом. Пример: binance',
                    inline=False)
    embed.add_field(name=f'Использование: Crypto-list',
                    value=f'{created_since_emodji} /crypto-list all:True, False\n'
                          f'{created_since_emodji} True - Выведет список из 50 криптовалют\n'
                          f'{created_since_emodji} False - Выведет список из доступных в /crypto-info',
                    inline=False)
    embed.add_field(name=f'Использование: Crypto-difference',
                    value=f'{created_since_emodji} /crypto-difference crypto:x convert:y\n'
                          f'{created_since_emodji} x - название криптовалюты из которой вы хотите преобразовать валюту\n'
                          f'{created_since_emodji} y - название валюты в которую вы хотите преобразовать первую',
                    inline=False)
    embed.add_field(name=f'{created_since_emodji} Использование: Crypto-image',
                    value=f'{created_since_emodji} /crypto image:id\n'
                          f'{created_since_emodji} id - введите айди криптовалюты для картинки\n'
                          f'{created_since_emodji} получить его можно в /crypto-info')
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        embed.add_field(name=f'{created_since_emodji} Использование: Crypto-admin',
                        value=f'{created_since_emodji} /crypto-admin\n'
                              f'{created_since_emodji} Выведет текущее состояние api ключа',
                        inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='crypto-admin', description='Выводит информацию о действующем API ключе')
async def crypto_admin(interaction: Interaction):
    url = 'https://pro-api.coinmarketcap.com/v1/key/info'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_Crypto
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    crypto_status = data['status']
    crypto_data = data['data']
    embed = nextcord.Embed(title=f'Api key: {API_Crypto}', color=0xffffff)
    embed.add_field(name=f'{created_since_emodji} Информация:',
                    value=f'{created_since_emodji} Время запроса: <t:{int(datetime.datetime.fromisoformat(crypto_status["timestamp"].replace("Z", "")).timestamp())}:R>(Время UTC+4)\n'
                          f'{created_since_emodji} Длительность ответа: {crypto_status["elapsed"]} сек.\n'
                          f'{created_since_emodji} Лимит токенов (месяц): {crypto_data["plan"]["credit_limit_monthly"]}\n'
                          f'{created_since_emodji} Сброс токенов (через сколько): {crypto_data["plan"]["credit_limit_monthly_reset"]}\n'
                          f'{created_since_emodji} Сброс токенов (когда): <t:{int(datetime.datetime.fromisoformat(crypto_data["plan"]["credit_limit_monthly_reset_timestamp"].replace("Z", "")).timestamp())}:R>\n'
                          f'{created_since_emodji} Лимит запросов (минута): {crypto_data["plan"]["rate_limit_minute"]}\n'
                          f'{created_since_emodji} Осталось токенов (месяц): {crypto_data["usage"]["current_month"]["credits_left"]}\n'
                          f'{created_since_emodji} Использованно токенов (сегодня): {crypto_data["usage"]["current_day"]["credits_used"]}\n'
                          f'{created_since_emodji} Использованно токенов (месяц): {crypto_data["usage"]["current_month"]["credits_used"]}')
    embed.set_footer(
        text=f'• {servername_to_footer} Crypto | https://coinmarketcap.com/ | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
        icon_url='https://logos-world.net/wp-content/uploads/2023/02/CoinMarketCap-Logo.png')
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='crypto-exchange',
                              description='Выводит информацию о выбранной криптобирже')
async def crypto_exchange(interaction: Interaction,
                          name: str = SlashOption(
                              description='Введите название криптобиржи. Пример: binance. Нельзя использовать заглавные буквы. '
                          )):
    url = 'https://pro-api.coinmarketcap.com/v1/exchange/info'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_Crypto
    }
    params = {
        'slug': name
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    try:
        exchange_data = data['data'][name]
    except KeyError:
        await interaction.response.send_message(f'Вы ввели неверное название биржи. Введено: {name}, попробуйте ещё раз', ephemeral=True)
        return
    embed = nextcord.Embed(title=f'{created_since_emodji} Криптобиржа: {exchange_data["name"]}', color=0xffffff)
    embed.set_thumbnail(url=exchange_data['logo'])
    embed.add_field(name=f'{created_since_emodji} Основные данные',
                    value=f'{created_since_emodji} Название: {exchange_data["name"]}\n'
                          f'{created_since_emodji} ID: {exchange_data["id"]}\n'
                          f'{created_since_emodji} Lowercase: {exchange_data["slug"]}\n'
                          f'{created_since_emodji} Валюты: {", ".join(exchange_data["fiats"])}\n'
                          f'{created_since_emodji} Дата запуска: <t:{int(datetime.datetime.fromisoformat(exchange_data["date_launched"].replace("Z", "")).timestamp())}:R>\n'
                          f'{created_since_emodji} Посещений в неделю: {exchange_data["weekly_visits"]:,.0f}\n'
                          f'{created_since_emodji} Объём торгов ежедневно (USD): {exchange_data["spot_volume_usd"]:,.1f}\n'
                          f'{created_since_emodji} Последнее обновление торгов: <t:{int(datetime.datetime.fromisoformat(exchange_data["spot_volume_last_updated"].replace("Z", "")).timestamp())}:R>')
    embed.add_field(name='Ссылки',
                    value=f'{link_emodji} Чат: [Тык]({"".join(exchange_data["urls"]["chat"])})\n'
                          f'{link_emodji} Сайт: [Тык]({"".join(exchange_data["urls"]["website"])})\n'
                          f'{link_emodji} Твиттер (X): [Тык]({"".join(exchange_data["urls"]["twitter"])})\n'
                          f'{link_emodji} Политика комиссии: [Тык]({"".join(exchange_data["urls"]["fee"])})')
    embed.set_footer(
        text=f'• {servername_to_footer} Crypto | https://coinmarketcap.com/ | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
        icon_url='https://logos-world.net/wp-content/uploads/2023/02/CoinMarketCap-Logo.png')
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='crypto-image', description='Выводит картинку криптовалюты')
async def crypto_image(interaction: Interaction,
                       id: str = SlashOption(
                           description='Введите id криптовалюты. Получить его можно в /crypto-info'
                       )):
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_Crypto
    }
    params = {
        'id': id
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        image = data['data'][id]['logo']
        await interaction.response.send_message(image)
    else:
        await interaction.response.send_message(f'Ошибка. Code: {response.status_code}', ephemeral=True)
try:
    client_discord.run(TOKEN)
except Exception as e:
    print(f'Error {e}')
    client_discord.run(TOKEN)
