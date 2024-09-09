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
import webbrowser
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

API_Weather = 'Enter OpenWeatherMap api key'
API_Crypto = 'Enter coinmarketcap api key'
Forbidden_words = ['даун', 'пидор', 'шлюха', 'гей', 'еблан', 'пидорас', 'хуйня', 'хуйни', 'шлюхи', 'пидрила', 'пидорасина', 'блять', 'блядь', 'блядина', 'ебланище', 'сука', 'негр', 'уёбище', 'шмара', 'хуесос', 'пиздализ', 'пизда', 'жопа', 'член', 'ссанина']
guild_owner_emodji = f"<:customemoji:enter emoji id>"
verification_level_emodji = f"<:customemoji:enter emoji id>"
created_since_emodji = f"<:customemoji:enter emoji id>"
all_categories_emodji = f"<:customemoji:enter emoji id>"
categories_emodji = f"<:customemoji:enter emoji id>"
members_emodji = f"<:customemoji:enter emoji id>"
member_emodji = f"<:customemoji:enter emoji id>"
boost_emodji = f"<:customemoji:enter emoji id>"
voice_emodji = f"<:customemoji:enter emoji id>"
reason_emodji = f"<:customemoji:enter emoji id>"
telegram_channels_link = 'https://t.me/UnicUm_Colabarations'
discord_server_link = 'https://discord.gg/hW39qmju'
staff_emodji = f"<:customemoji:enter emoji id>"
warn_emodji = f"<:customemoji:enter emoji id>"
time_emodji = f"<:customemoji:enter emoji id>"
text_emodji = f"<:customemoji:enter emoji id>"
slash_emodji = f"<:customemoji:enter emoji id>"
bot_emodji = f"<:customemoji:enter emoji id>"
telegram_emodji = f"<:customemoji:enter emoji id>"
discord_emodji = f"<:customemoji:enter emoji id>"
link_emodji = f"<:customemoji:enter emoji id>"
BTC_emodji = f"<:customemoji:enter emoji id>"
ETH_emodji = f"<:customemoji:enter emoji id>"
DOGE_emodji = f"<:customemoji:enter emoji id>"
RUB_emodji = f"<:customemoji:enter emoji id>"
USD_emodji = f"<:customemoji:enter emoji id>"
USDT_emodji = f"<:customemoji:enter emoji id>"
BUSD_emodji = f"<:customemoji:enter emoji id>"
SHIB_emodji = f"<:customemoji:enter emoji id>"
ELON_emodji = f"<:customemoji:enter emoji id>"
AKITA_emodji = f"<:customemoji:enter emoji id>"
Coinmarket_emodji = f"<:customemoji:enter emoji id>"
Right_emodji = f"<:customemoji:enter emoji id>"
LTC_emodji = f"<:customemoji:enter emoji id>"
SOL_emodji = f"<:customemoji:enter emoji id>"
BNB_emodji = f"<:customemoji:enter emoji id>"
USDC_emodji = f"<:customemoji:enter emoji id>"
XRP_emodji = f"<:customemoji:enter emoji id>"
HMSTR_emodji = f"<:customemoji:enter emoji id>"
TON_emodji = f"<:customemoji:enter emoji id>"
admin_tickets = 'enter admin tickets channel id'
link = {
    "main": "",
    "shedules": '',
    "login": ''
}
author_link = {
    "main": "(main)[https://github.com/Ivanskem]",
    "bot-repositori": "(bot)[https://github.com/Ivanskem/Python-discord-bot]",
    "other-repositories": "(other)[https://github.com/Ivanskem?tab=repositories]"
}


class Getrole(Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label=language["Roles"]["Getrole"]["Options"]["R_71"]["Label"],
                                  description=language["Roles"]["Getrole"]["Options"]["R_71"]["Description"],
                                  emoji=language["Roles"]["Getrole"]["Options"]["R_71"]["Emoji"]),
            nextcord.SelectOption(label=language["Roles"]["Getrole"]["Options"]["R_72"]["Label"],
                                  description=language["Roles"]["Getrole"]["Options"]["R_72"]["Description"],
                                  emoji=language["Roles"]["Getrole"]["Options"]["R_72"]["Emoji"]),
            nextcord.SelectOption(label=language["Roles"]["Getrole"]["Options"]["IE_71"]["Label"],
                                  description=language["Roles"]["Getrole"]["Options"]["IE_71"]["Description"],
                                  emoji=language["Roles"]["Getrole"]["Options"]["IE_71"]["Emoji"]),
            nextcord.SelectOption(label=language["Roles"]["Getrole"]["Options"]["IE_72"]["Label"],
                                  description=language["Roles"]["Getrole"]["Options"]["IE_72"]["Description"],
                                  emoji=language["Roles"]["Getrole"]["Options"]["IE_72"]["Emoji"]),
            nextcord.SelectOption(label=language["Roles"]["Getrole"]["Options"]["II_71"]["Label"],
                                  description=language["Roles"]["Getrole"]["Options"]["II_71"]["Description"],
                                  emoji=language["Roles"]["Getrole"]["Options"]["II_71"]["Emoji"]),
            nextcord.SelectOption(label=language["Roles"]["Getrole"]["Options"]["II_72"]["Label"],
                                  description=language["Roles"]["Getrole"]["Options"]["II_72"]["Description"],
                                  emoji=language["Roles"]["Getrole"]["Options"]["II_72"]["Emoji"])
        ]
        super().__init__(placeholder=language["Roles"]["Getrole"]["Placeholder"], min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        R_71 = nextcord.utils.get(interaction.guild.roles, name='Ученик Р-71')
        R_72 = nextcord.utils.get(interaction.guild.roles, name='Ученик Р-72')
        IE_71 = nextcord.utils.get(interaction.guild.roles, name='Ученик ИЭ-71')
        IE_72 = nextcord.utils.get(interaction.guild.roles, name='Ученик ИЭ-72')
        II_71 = nextcord.utils.get(interaction.guild.roles, name='Ученик ИИ-71')
        II_72 = nextcord.utils.get(interaction.guild.roles, name='Ученик ИИ-72')

        picked_group = self.values[0]

        if picked_group == language["Roles"]["Getrole"]["Options"]["R_71"]["Label"]:
            await interaction.user.add_roles(R_71, reason=language["Roles"]["Getrole"]["Reason"])
            await interaction.response.send_message(language["Roles"]["Getrole"]["Messages"]["Success"].format(group='Р-71'), ephemeral=True)
        elif picked_group == language["Roles"]["Getrole"]["Options"]["R_72"]["Label"]:
            await interaction.user.add_roles(R_72, reason=language["Roles"]["Getrole"]["Reason"])
            await interaction.response.send_message(language["Roles"]["Getrole"]["Messages"]["Success"].format(group='Р-72'), ephemeral=True)
        elif picked_group == language["Roles"]["Getrole"]["Options"]["IE_71"]["Label"]:
            await interaction.user.add_roles(IE_71, reason=language["Roles"]["Getrole"]["Reason"])
            await interaction.response.send_message(language["Roles"]["Getrole"]["Messages"]["Success"].format(group='ИЭ-71'), ephemeral=True)
        elif picked_group == language["Roles"]["Getrole"]["Options"]["IE_72"]["Label"]:
            await interaction.user.add_roles(IE_72, reason=language["Roles"]["Getrole"]["Reason"])
            await interaction.response.send_message(language["Roles"]["Getrole"]["Messages"]["Success"].format(group='ИЭ-72'), ephemeral=True)
        elif picked_group == language["Roles"]["Getrole"]["Options"]["II_71"]["Label"]:
            await interaction.user.add_roles(II_71, reason=language["Roles"]["Getrole"]["Reason"])
            await interaction.response.send_message(language["Roles"]["Getrole"]["Messages"]["Success"].format(group='ИИ-71'), ephemeral=True)
        elif picked_group == language["Roles"]["Getrole"]["Options"]["II_72"]["Label"]:
            await interaction.user.add_roles(II_72, reason=language["Roles"]["Getrole"]["Reason"])
            await interaction.response.send_message(language["Roles"]["Getrole"]["Messages"]["Success"].format(group='ИИ-72'), ephemeral=True)


class GetroleView(View):
    def __init__(self):
        super().__init__()
        self.add_item(Getrole())


class Settings(Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label='Русский', description='Выберите чтобы установить язык (Русский)',
                                  emoji="<:customemoji:1272602729948123136>"),
            nextcord.SelectOption(label='Ukraine', description='Виберіть щоб встановити мову (Українська)',
                                  emoji='<:customemoji:1272602710415249441>'),
            nextcord.SelectOption(label='English (UK)', description='Select to set the language (English(UK))',
                                  emoji='<:customemoji:1272602644900347914>'),
            nextcord.SelectOption(label='English (US)', description='Select to set the language (English(US))',
                                  emoji='<:customemoji:1272602527208181771>'),
            nextcord.SelectOption(label='Finland', description='Valitse Kieli (Suomi)',
                                  emoji='<:customemoji:1272602680509988946>'),
            nextcord.SelectOption(label='Italy', description='Selezionare per impostare la lingua (Italiano)',
                                  emoji='<:customemoji:1272602670418366615>'),
            nextcord.SelectOption(label='France', description='Sélectionnez pour définir la langue (Français)',
                                  emoji='<:customemoji:1272602629478027315>'),
            nextcord.SelectOption(label='Spain', description='Seleccione para establecer el idioma (Español)',
                                  emoji='<:customemoji:1272602660423598203>')
        ]
        super().__init__(placeholder='Pick language', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        language = self.values[0]
        await self.set_language(interaction, language)

    async def set_language(self, interaction: Interaction, language: str):
        logger = guild_logger(interaction.guild)
        logger.info('Set new language')

        database_location = connect_database(interaction.guild)
        cursor = database_location.cursor()

        cursor.execute("SELECT language FROM settings WHERE guild_id = ?", (interaction.guild.id,))
        result = cursor.fetchone()
        language_database = result[0] if result else None

        if language_database == language:
            await interaction.response.send_message("You already have this language!", ephemeral=True)
        else:
            try:
                cursor.execute("UPDATE settings SET language = ? WHERE guild_id = ?", (language, interaction.guild.id,))
                database_location.commit()
            except sqlite3.Error:
                await interaction.response.send_message('Something went wrong, try again later', ephemeral=True)
            finally:
                cursor.close()
                database_location.close()

            await interaction.response.send_message(f'Successfully set new language: {language}', ephemeral=True)


class SettingsView(View):
    def __init__(self):
        super().__init__()
        self.add_item(Settings())


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
            nextcord.SelectOption(label=language["Tickets"]["View"]["Options"]["Support"]["Title"], description=language["Tickets"]["View"]["Options"]["Support"]["Description"],
                                  emoji="🛠"),
            nextcord.SelectOption(label=language["Tickets"]["View"]["Options"]["Bot"]["Title"], description=language["Tickets"]["View"]["Options"]["Bot"]["Description"],
                                  emoji="🤖")
        ]
        super().__init__(placeholder=language["Tickets"]["View"]["Action"]["Placeholder"], min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        category = self.values[0]
        await interaction.response.send_message(language["Tickets"]["View"]["Callback"]["Picked"].format(category=category), ephemeral=True)
        await self.create_ticket(interaction, category)

    async def create_ticket(self, interaction: Interaction, category: str):
        channel_name = f'ticket-{interaction.user.name}'.replace(" ", "-").lower()
        admin_role = nextcord.utils.get(interaction.guild.roles, name='Администратор')
        bot = interaction.guild.me
        default_role = interaction.guild.default_role
        overwrites = {
            default_role: nextcord.PermissionOverwrite(view_channel=False),
            interaction.user: nextcord.PermissionOverwrite(view_channel=True, send_messages=True),
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
        embed = nextcord.Embed(title=language["Tickets"]["Create"]["Channel"]["Title"], color=0xffffff)
        embed.add_field(name=f'{created_since_emodji} {language["Tickets"]["Create"]["Channel"]["Description"]["Title"].format(mention=interaction.user.name)}',
                        value=f'{slash_emodji} • {language["Tickets"]["Create"]["Channel"]["Description"]["Header"].format(category=category)}.\n'
                              f'{member_emodji} • {language["Tickets"]["Create"]["Channel"]["Description"]["Lower"].format(mention=interaction.user.mention)}')
        embed.set_footer(
            text=f'• {interaction.guild.name} Tickets | {datetime.datetime.now().replace(microsecond=0)}',
            icon_url=interaction.guild.icon.url)
        embed_admin = nextcord.Embed(title=language["Tickets"]["Create"]["Admin"]["Title"], color=0xffffff)
        embed_admin.add_field(name=f'{created_since_emodji} {language["Tickets"]["Create"]["Admin"]["Description"]["Title"].format(member=interaction.user.name)}',
                              value=f'{created_since_emodji} • {language["Tickets"]["Create"]["Admin"]["Description"]["Header"].format(channel_id=ticket_channel.id)}\n'
                                    f'{member_emodji} • {language["Tickets"]["Create"]["Admin"]["Description"]["Lower"].format(member=interaction.user.mention)}')
        embed_admin.set_footer(
            text=f'• {interaction.guild.name} Tickets | {datetime.datetime.now().replace(microsecond=0)}',
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
            nextcord.SelectOption(label=language["Tickets"]["View"]["Action"]["Close"]["Title"], description=language["Tickets"]["View"]["Action"]["Close"]["Description"],
                                  emoji="❌"),
            nextcord.SelectOption(label=language["Tickets"]["View"]["Action"]["Feedback"]["Title"], description=language["Tickets"]["View"]["Action"]["Feedback"]["Description"],
                                  emoji="✍")
        ]
        super().__init__(placeholder=language["Tickets"]["View"]["Action"]["Placeholder"], min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        action = self.values[0]
        try:
            if action == language["Tickets"]["View"]["Action"]["Close"]["Title"]:
                await interaction.response.send_modal(CloseTicketModal())
            elif action == language["Tickets"]["View"]["Action"]["Feedback"]["Title"]:
                await interaction.response.send_modal(FeedbackModal())
        except Exception:
            await interaction.response.send_message(language["Errors"]["Bot"]["Network"], ephemeral=True)


class TicketActionView(View):
    def __init__(self):
        super().__init__()
        self.add_item(TicketAction())


class CloseTicketModal(Modal):
    def __init__(self):
        super().__init__(title=language["Tickets"]["Close"]["Title"])
        self.reason = TextInput(label=language["Tickets"]["Close"]["Label"], style=nextcord.TextInputStyle.paragraph)
        self.add_item(self.reason)

    async def callback(self, interaction: Interaction):
        logger = guild_logger(interaction.guild)
        reason = self.reason.value
        logger.info(f'Пользователь {interaction.user.name} закрыл тикет с причиной {reason}')
        database_location = connect_database(interaction.guild)
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
        embed_channel = nextcord.Embed(title=language["Tickets"]["Close"]["Callback"]["Channel"]["Title"], color=0xffffff)
        embed_channel.add_field(name=f'{created_since_emodji} {language["Tickets"]["Close"]["Callback"]["Channel"]["Description"]["Title"].format(mention=interaction.user.name)}',
                                value=f'{slash_emodji} • {language["Tickets"]["Close"]["Callback"]["Channel"]["Description"]["Header"].format(reason=reason)}\n'
                                      f'{warn_emodji} • {language["Tickets"]["Close"]["Callback"]["Channel"]["Description"]["Lower"]}')
        embed_channel.set_footer(
            text=f'• {interaction.guild.name} Tickets | {datetime.datetime.now().replace(microsecond=0)}',
            icon_url=interaction.guild.icon.url)
        embed_admin = nextcord.Embed(title=language["Tickets"]["Close"]["Callback"]["Admin"]["Title"], color=0xffffff)
        embed_admin.add_field(name=f'{created_since_emodji} {language["Tickets"]["Close"]["Callback"]["Admin"]["Description"]["Title"].format(mention=interaction.user.name)}',
                              value=f'{slash_emodji} • {language["Tickets"]["Close"]["Callback"]["Admin"]["Description"]["Header"].format(channel_id=channel_id)}\n'
                                    f'{created_since_emodji} • {language["Tickets"]["Close"]["Callback"]["Admin"]["Description"]["Lower"].format(reason=reason)}')
        embed_admin.set_footer(
            text=f'• {interaction.guild.name} Tickets | {datetime.datetime.now().replace(microsecond=0)}',
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
        database_location = connect_database(interaction.guild)
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
        embed_channel = nextcord.Embed(title=language["Tickets"]["Review"]["Callback"]["Channel"]["Title"], color=0xffffff)
        embed_channel.add_field(name=f'{created_since_emodji} {language["Tickets"]["Review"]["Callback"]["Channel"]["Description"]["Title"].format(mention=interaction.user.name)}',
                                value=f'{slash_emodji} • {language["Tickets"]["Review"]["Callback"]["Channel"]["Description"]["Header"].format(feedback=feedback)}\n'
                                      f'{warn_emodji} • {language["Tickets"]["Review"]["Callback"]["Channel"]["Description"]["Lower"]}')
        embed_channel.set_footer(
            text=f'• {interaction.guild.name} Tickets | {datetime.datetime.now().replace(microsecond=0)}',
            icon_url=interaction.guild.icon.url)
        embed_admin = nextcord.Embed(title=language["Tickets"]["Review"]["Callback"]["Admin"]["Title"], color=0xffffff)
        embed_admin.add_field(name=f'{created_since_emodji} {language["Tickets"]["Review"]["Callback"]["Admin"]["Description"]["Title"].format(mention=interaction.user.name)}',
                              value=f'{slash_emodji} • {language["Tickets"]["Review"]["Callback"]["Admin"]["Description"]["Header"].format(feedback=feedback)}\n'
                                    f'{created_since_emodji} • {language["Tickets"]["Review"]["Callback"]["Admin"]["Description"]["Lower"].format(channel_id=channel_id)}')
        embed_admin.set_footer(
            text=f'• {interaction.guild.name} Tickets | {datetime.datetime.now().replace(microsecond=0)}',
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


def guild_logger(guild):
    log_dir = os.path.join("Database", f"{guild.id}")
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, f"{guild.id}.log")

    logger = logging.getLogger(f"{guild.id}_logger")

    logger.propagate = False

    if not logger.hasHandlers():
        handler = logging.FileHandler(log_path, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger


def connect_database(guild):
    directory_path = os.path.join('Database',
                                  f'{guild.id}')
    os.makedirs(directory_path, exist_ok=True)
    database_location = sqlite3.connect(os.path.join(directory_path, f'{guild.id}.db'))
    return database_location


def giveaway_add(json_file, data):
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def setup_language(language_data):
    global language_file
    if language_data == 'Ukraine':
        language_file = 'uk_UA'
    elif language_data == 'Русский':
        language_file = 'ru_RU'
    elif language_data == 'Italy':
        language_file = 'it_IT'
    elif language_data == 'France':
        language_file = 'fr_FR'
    elif language_data == 'Spain':
        language_file = 'es_ES'
    elif language_data == 'Finland':
        language_file = 'fi_FI'
    elif language_data == 'English (US)':
        language_file = 'en_US'
    elif language_data == 'English (UK)':
        language_file = 'en_UK'

    with open(f'language/{language_file}.json', 'r', encoding='utf-8') as file:
        language = json.load(file)
    return language


def language_data(guild):
    database_location = connect_database(guild)
    cursor = database_location.cursor()
    cursor.execute("SELECT language FROM settings WHERE guild_id=? AND guild_name=?",
                   (guild.id, guild.name))
    language_result = cursor.fetchone()
    language_data = language_result[0]
    database_location.close()
    return language_data


def win_notification(title, message):
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=0, threaded=True)


async def send_server_info():
    for guild in client_discord.guilds:
        language_code = language_data(guild)
        language = setup_language(language_code)
        logger = guild_logger(guild)
        logger.info(f'{language["Logging"]["Serverinfo"]} | {datetime.datetime.now().replace(microsecond=0)}')
        channel = nextcord.utils.get(guild.channels, name='статистика') or nextcord.utils.get(guild.channels, name='statistics')
        if channel:
            async for msg in channel.history(limit=1):
                await msg.delete()
            bots = sum(1 for member in guild.members if member.bot)
            total_members = guild.member_count
            without_bot = total_members - bots

            verification_level = guild.verification_level
            if verification_level == guild.verification_level.low:
                if language == "Русский":
                    verification_level = 'Низкий'
                elif language == 'English (US)' or language == 'English (UK)':
                    verification_level = 'Low'
                elif language == 'Ukraine':
                    verification_level = 'Низький'
                elif language == 'Finland':
                    verification_level = 'Matala'
                elif language == 'Italy':
                    verification_level = 'Basso'
                elif language == 'Spain':
                    verification_level = 'Bajo'
                elif language == 'France':
                    verification_level = 'Faible'
            elif verification_level == guild.verification_level.medium:
                if language == "Русский":
                    verification_level = 'Средний'
                elif language == 'English (US)' or language == 'English (UK)':
                    verification_level = 'Medium'
                elif language == 'Ukraine':
                    verification_level = 'Середній'
                elif language == 'Finland':
                    verification_level = 'Keskitaso'
                elif language == 'Italy':
                    verification_level = 'Medio'
                elif language == 'Spain':
                    verification_level = 'Medio'
                elif language == 'France':
                    verification_level = 'Moyen'
            elif verification_level == guild.verification_level.high:
                if language == "Русский":
                    verification_level = 'Высокий'
                elif language == 'English (US)' or language == 'English (UK)':
                    verification_level = 'High'
                elif language == 'Ukraine':
                    verification_level = 'Високий'
                elif language == 'Finland':
                    verification_level = 'Korkea'
                elif language == 'Italy':
                    verification_level = 'Alto'
                elif language == 'Spain':
                    verification_level = 'Alto'
                elif language == 'France':
                    verification_level = 'Élevé'
            else:
                if language == "Русский":
                    verification_level = 'Нет'
                elif language == 'English (US)' or language == 'English (UK)':
                    verification_level = 'None'
                elif language == 'Ukraine':
                    verification_level = 'Немає'
                elif language == 'Finland':
                    verification_level = 'Ei mitään'
                elif language == 'Italy':
                    verification_level = 'Nessuno'
                elif language == 'Spain':
                    verification_level = 'Ninguno'
                elif language == 'France':
                    verification_level = 'Aucun'

            created_at = guild.created_at
            text_channels = len(guild.text_channels)
            voice_channels = len(guild.voice_channels)
            categories = len(guild.categories)
            total_channels = text_channels + voice_channels + categories

            embed = nextcord.Embed(title=guild.name, color=0x6fa8dc)
            if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)
            else:
                pass
            embed.add_field(name=f'{language["ServerInfo"]["New_type"]["Main"]["Title"]}',
                            value=f'{guild_owner_emodji} {language["ServerInfo"]["New_type"]["Main"]["Owner"].format(owner=guild.owner.mention)}\n'
                                  f'{verification_level_emodji} {language["ServerInfo"]["New_type"]["Main"]["Verification_lvl"].format(verification_level_show=verification_level)}\n'
                                  f'{created_since_emodji} {language["ServerInfo"]["New_type"]["Main"]["Created_at"]} <t:{int(created_at.timestamp())}:F>\n(<t:{int(created_at.timestamp())}:R>)\n'
                                  f'{slash_emodji} {language["ServerInfo"]["New_type"]["Main"]["About"].format(text_channels=text_channels, voice_channels=voice_channels, categories=categories, total_channels=total_channels)}\n'  # Используем результат
                                  f'{text_emodji} {language["ServerInfo"]["New_type"]["Main"]["Text"].format(text_channels=text_channels)}\n'
                                  f'{voice_emodji} {language["ServerInfo"]["New_type"]["Main"]["Voice"].format(voice_channels=voice_channels)}\n'
                                  f'{categories_emodji} {language["ServerInfo"]["New_type"]["Main"]["Categories"].format(categories=categories)}\n')
            embed.add_field(name=f'{language["ServerInfo"]["New_type"]["Users"]["Title"]}',
                            value=f'{members_emodji} {language["ServerInfo"]["New_type"]["Users"]["About"].format(total_members=total_members)}\n'
                                  f'{bot_emodji} {language["ServerInfo"]["New_type"]["Users"]["Bots"].format(bots=bots)}\n'
                                  f'{member_emodji} {language["ServerInfo"]["New_type"]["Users"]["Members"].format(members=without_bot)}\n')
            boost_level = guild.premium_tier
            embed.add_field(name=f'{language["ServerInfo"]["New_type"]["Boosts"]["Title"]}',
                            value=f'{boost_emodji} {language["ServerInfo"]["New_type"]["Boosts"]["Level"].format(boost_level=boost_level)}\n ({language["ServerInfo"]["New_type"]["Boosts"]["Boosts"].format(boost_count=guild.premium_subscription_count)})\n')
            embed.add_field(name=f'{language["ServerInfo"]["New_type"]["Links"]["Title"]}',
                            value=f'{telegram_emodji} {language["ServerInfo"]["New_type"]["Links"]["Telegram"].format(telegram_link=telegram_channels_link)} \n'
                                  f'{discord_emodji} {language["ServerInfo"]["New_type"]["Links"]["Discord"].format(discord_link=discord_server_link)}\n')
            if guild.icon:
                embed.set_footer(
                    text=f'• {guild.name} Info | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                    icon_url=guild.icon.url)
            else:
                embed.set_footer(
                    text=f'• {guild.name} Info | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
            await channel.send(embed=embed)
        else:
            owner = guild.owner
            await owner.send(f'{language["Errors"]["Serverinfo"]["Send"]}')


async def send_server_info_7_days():
    while True:
        await send_server_info()
        await asyncio.sleep(7 * 24 * 60 * 60)


async def warn(interaction, guild_id, user_id, user_name):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    admin_role = nextcord.utils.get(interaction.guild.roles, name="Администратор")
    database_location = connect_database(interaction.guild)
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
    reason = 'Incorrect reason'
    embed = nextcord.Embed(title=f'{created_since_emodji} {language["Warn"]["Title"]}', color=nextcord.Color.dark_purple())
    embed.add_field(name=f'{member_emodji} {language["Warn"]["Description"]["Title"].format(user=user_name)}\n'
                         f'{reason_emodji} {language["Warn"]["Description"]["Reason"].format(reason=reason)}\n'
                         f'{warn_emodji} {language["Warn"]["Description"]["Count"].format(count=warn_count)}', value='')
    try:
        embed.set_footer(text=f'• {interaction.guild.name} Warn | {datetime.datetime.now().replace(microsecond=0)}',
                         icon_url=interaction.guild.icon.url)
    except AttributeError:
        embed.set_footer(text=f'• {interaction.guild.name} Warn | {datetime.datetime.now().replace(microsecond=0)}')
    await interaction.channel.send(embed=embed)
    if warn_count >= 5:
        await interaction.user.remove_roles(admin_role, reason='too many warns')
        embed_warn = nextcord.Embed(title=f'{created_since_emodji} {language["Moderation"]["Admin_removal"]["Title"]}', color=nextcord.Color.red())
        embed_warn.add_field(name=f'{member_emodji} {language["Moderation"]["Admin_removal"]["Admin"].format(mention=user_name)}',
                             value=f'{reason_emodji} {language["Moderation"]["Admin_removal"]["Reason"]}\n'
                                   f'{warn_emodji} {language["Moderation"]["Admin_removal"]["Lower"]}')
        try:
            embed.set_footer(text=f'• {interaction.guild.name} Reset | {datetime.datetime.now().replace(microsecond=0)}',
                             icon_url=interaction.guild.icon.url)
        except AttributeError:
            embed.set_footer(text=f'• {interaction.guild.name} Reset | {datetime.datetime.now().replace(microsecond=0)}')
        cursor.execute("UPDATE warn_list SET warns = 0 WHERE user_id = ?", (member.id,))
        database_location.commit()
        database_location.close()
        await interaction.channel.send(embed=embed_warn)


@client_discord.event
async def on_guild_join(guild):
    logger = guild_logger(guild)
    logger.warning(f'Joined new server {guild.id}({guild.name})')
    archive_database = os.path.join(f'Database/{guild.id}',
                                    f'archive_database')
    os.makedirs(archive_database, exist_ok=True)
    archive_log = os.path.join(f'Database/{guild.id}',
                               f'archive_logs')
    os.makedirs(archive_log, exist_ok=True)
    database_location = connect_database(guild)
    cursor = database_location.cursor()
    try:
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    guild_name TEXT NOT NULL,
                    guild_id INTEGER NOT NULL,
                    language TEXT NOT NULL
                    )
                    """)
        cursor.execute("INSERT INTO settings (guild_name, guild_id, language) VALUES (?, ?, ?)", (guild.name, guild.id, 'en_US'))
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS users_list (
                    user_id INTEGER PRIMARY KEY,
                    user_name TEXT NOT NULL,
                    user_mention TEXT NOT NULL,
                    user_joined_date DATETIME NOT NULL
                    )
                    ''')
        users_data = [(member.id, member.name, member.mention, member.joined_at) for member in guild.members]
        cursor.executemany(
            "INSERT OR IGNORE INTO users_list (user_id, user_name, user_mention, user_joined_date) VALUES (?, ?, ?, ?)",
            users_data
        )
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
    except sqlite3.Error as e:
        logger.error(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_location:
            database_location.close()


# @client_discord.event
# async def on_reaction_add(reaction: nextcord.Reaction, user: nextcord.User):
#     if user.bot:
#         return
#
#     json_file = 'jsons/giveaway.json'
#     giveaways = read_json(json_file)
#
#     for giveaway in giveaways:
#         if giveaway['message_id'] == reaction.message.id and reaction.emoji == '🎉':
#             users = await reaction.users().flatten()
#             users = [user for user in users if not user.bot]
#
#             if users:
#                 winner = random.choice(users)
#                 await reaction.message.channel.send(
#                     f'Поздравляем {winner.mention}, вы выиграли розыгрыш {giveaway["name"]}!')
#             else:
#                 await reaction.message.channel.send('Участвующих пользователей нет!')
#             giveaways.remove(giveaway)
#             giveaway_add(json_file, giveaways)
#             break


@client_discord.event
async def on_ready():
    print(f'{client_discord.user} запущен')
    print(' ')
    message = f"Блокировка: /ban Нарушитель причина \nРазблокировка: /unban Нарушитель причина \nУдаление: /kick Нарушитель причина \nОтчистка: /clear количество(можно любым количеством либо 0 для удаления всего) \nСписок всех учатников: /members \nВывод информации о сервере: /serverinfo \nЗаглушение участника: /mute Нарушитель причина"f" \nРазглушение участника: /unmute Нарушитель причина \nИнформация о участнике: /info Участник \nАватар участника: /avatar Участник \nИнформация о погоде: /weather Город(любой) \nВывод этого сообщения: /commands (в канал #bot-commands, не писать) \nОтправить сообщение: /say (сообщение)"
    print(message)
    # asyncio.create_task(send_server_info_7_days())

    win_notification("Bot Started", f"Дискорд бот запущен\nTime: {datetime.datetime.now().replace(microsecond=0)}")


@client_discord.event
async def on_disconnect():
    print(f'Бот {client_discord.user} остановлен!, перезапуск')
    await asyncio.sleep(10)
    await client_discord.connect(reconnect=True)


@client_discord.event
async def on_member_join(member):
    global database_location
    user_id = member.id
    user_name = member.name
    user_mention = member.mention
    user_joined_date = member.joined_at

    language_code = language_data(member.guild)
    language = setup_language(language_code)
    logger = guild_logger(member.guild)
    logger.info(language["Logging"]["Member_join"].format(name=user_name))

    try:
        database_location = connect_database(member.guild)
        cursor = database_location.cursor()
        cursor.execute("INSERT INTO users_list (user_id, user_name, user_mention, user_joined_date) VALUES (?, ?, ?, ?)",
                       (user_id, user_name, user_mention, user_joined_date))
        database_location.commit()
    except sqlite3.Error as e:
        logger.error(language["Errors"]["Standart"]["Unknown_error"].format(e=e))
    finally:
        database_location.close()

    embed_server = nextcord.Embed(
        title=f'{language["Join"]["Server"]["Title"]} "{member.guild.name}"',
        color=nextcord.Color.purple()
    )
    if member.avatar:
        embed_server.set_thumbnail(url=member.avatar.url)
    else:
        embed_server.set_thumbnail(url='https://cdn.discordapp.com/embed/avatars/0.png')

    embed_server.add_field(name=language["Join"]["Server"]["Description"]["Title"],
                           value=language["Join"]["Server"]["Description"]["Value"])
    try:
        embed_server.set_footer(text=f'• {member.guild.name} Welcome | {datetime.datetime.now().replace(microsecond=0)}',
                                icon_url=member.guild.icon.url)
    except AttributeError:
        embed_server.set_footer(
            text=f'• {member.guild.name} Welcome | {datetime.datetime.now().replace(microsecond=0)}')

    embed_user = nextcord.Embed(
        title=f'{language["Join"]["User"]["Title"]} "{member.guild.name}"',
        color=nextcord.Color.purple()
    )
    if member.avatar:
        embed_user.set_thumbnail(url=member.avatar.url)
    else:
        embed_user.set_thumbnail(url='https://cdn.discordapp.com/embed/avatars/0.png')
    embed_user.add_field(name=language["Join"]["User"]["Description"]["Title"], value=language["Join"]["User"]["Description"]["Value"])
    try:
        embed_user.set_footer(text=f'• {member.guild.name} Welcome | {datetime.datetime.now().replace(microsecond=0)}',
                              icon_url=member.guild.icon.url)
    except AttributeError:
        embed_user.set_footer(
            text=f'• {member.guild.name} Welcome | {datetime.datetime.now().replace(microsecond=0)}')

    channel = nextcord.utils.get(member.guild.channels, name='добро-пожаловать')
    if channel:
        await channel.send(embed=embed_server)
    else:
        logger.error(language["Errors"]["Join"]["Channel_Not_Found"])
    try:
        await member.send(embed=embed_user)
    except nextcord.errors.HTTPException:
        logger.warning(language["Errors"]["Join"]["Invalid_user"])


@client_discord.event
async def on_member_leave(member):
    language_code = language_data(member.guild)
    language = setup_language(language_code)
    embed_server = nextcord.Embed(title=f'{language["Leave"]["Server"]["Title"]} {member.guild.name}',
                                  color=nextcord.Color.dark_blue())
    embed_server.set_thumbnail(url=member.avatar.url)
    embed_server.add_field(name='', value=f'{language["Leave"]["Server"]["Value"]}')
    embed_server.set_footer(text=f'{member.guild.name} Goodbye | {datetime.datetime.now().replace(microsecond=0)}')

    embed_user = nextcord.Embed(title=f'{language["Leave"]["User"]["Title"]} {member.guild.name}',
                                color=nextcord.Color.purple())
    embed_user.set_thumbnail(url=member.avatar.url)
    embed_user.add_field(name=' ', value=language["Leave"]["User"]["Value"])
    embed_user.set_footer(text=f'{member.guild.name} Goodbye | {datetime.datetime.now().replace(microsecond=0)}')
    channel = nextcord.utils.get(member.guild.channels, name='admin')
    if channel:
        await channel.send(embed=embed_server)
    else:
        logger.error(language["Errors"]["Join"]["Channel_Not_Found"])
    await member.send(embed=embed_user)


@client_discord.event
async def on_message(message):
    if message.author == client_discord.user:
        return

    language_code = language_data(message.guild)
    language = setup_language(language_code)

    for word in Forbidden_words:
        if word in message.content:
            if any(role.name == "Администратор" for role in message.author.roles):
                return
            else:
                await message.delete()
                await message.channel.send(f'{message.author.mention}. {language["Other"]["Forbidden_find"]}')
                return


@client_discord.slash_command(name='ban', description='Blocks a participant')
async def ban(interaction: Interaction, member: nextcord.Member,
              reason: str = SlashOption(
                  description="The reason for the ban",
                  default="Without reason"
              )):
    global database_location
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    logger.info(language["Logging"]["Ban"]["Interaction"].format(name=interaction.user.name))
    if nextcord.utils.get(interaction.user.roles, name='Администратор') is not None:
        try:
            await member.ban(reason=reason)
            logger.info(language["Logging"]["Ban"]["Banned"].format(member=member.name, user=interaction.user.name,
                                                                    reason=reason))
            try:
                database_location = connect_database(interaction.guild)
                cursor = database_location.cursor()
                cursor.execute("""
                    INSERT INTO mod_actions (action_type, guild_id, moderator_name, moderator_id, target_user_name, target_user_id, reason, action_time) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, ('Ban', interaction.guild.id, interaction.user.name, interaction.user.id, member.name, member.id, reason,
                      datetime.datetime.now()))
                cursor.close()
                database_location.commit()
            except sqlite3.Error as e:
                logger.error(language["Errors"]["Standart"]["Error_message_with_code"].format(e=e))
                await interaction.response.send_message(language["Errors"]["Standart"]["Unknown_error"].format(e=e),
                                                        ephemeral=True)
            finally:
                database_location.close()
            if reason in ['Without reason']:
                await warn(interaction, interaction.guild.id, interaction.user.id,
                           interaction.user.name)
            embed = nextcord.Embed(title=f'{created_since_emodji} {language["Moderation"]["Ban"]["Title"]}',
                                   color=nextcord.Color.dark_purple())
            embed.add_field(name=' ',
                            value=f'{staff_emodji} {language["Moderation"]["Ban"]["Admin"].format(mention=interaction.user.mention)}\n'
                                  f'{reason_emodji} {language["Moderation"]["Ban"]["Reason"].format(reason=reason)}\n'
                                  f'{member_emodji} {language["Moderation"]["Ban"]["Banned"].format(user=member.mention)}\n')
            if interaction.guild.icon:
                embed.set_footer(
                    text=f'• {interaction.guild.name} Ban | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                    icon_url=interaction.guild.icon.url)
            else:
                embed.set_footer(
                    text=f'• {interaction.guild.name} Ban | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
            await interaction.response.send_message(embed=embed)
        except nextcord.Forbidden:
            logger.error(language["Errors"]["Bot"]["Forbidden"])
            await interaction.response.send_message(language["Errors"]["Bot"]["Forbidden"],
                                                    ephemeral=True)
    else:
        logger.info(language["Errors"]["User"]["Not_enough_rights"].format(user=interaction.user.name))
        await interaction.response.send_message(language["Errors"]["Standart"]["Not_enough_rights"],
                                                ephemeral=True)


@client_discord.slash_command(name='warn', description='Issues a warning to the participant')
async def warn_command(interaction: Interaction, member: nextcord.Member,
                       action: str = SlashOption(description='Select an action',
                                                 choices=['show', 'give'],
                                                 default='show'),
                       reason: str = SlashOption(description='The reason for the warning',
                                                 default='Without reason'
                       )):
    global warn_count, warn_last, embed_result, cursor, database_location
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    logger.info(language["Logging"]["Warn"]["Interaction"].format(name=interaction.user.name))
    if nextcord.utils.get(interaction.user.roles, name='Администратор') is not None:
        if action == 'show':
            try:
                database_location = connect_database(interaction.guild)
                cursor = database_location.cursor()
                cursor.execute("SELECT warns FROM warn_list WHERE guild_id=? AND user_id=?",
                               (interaction.guild.id, member.id))
                warn_count = cursor.fetchone()
                cursor.execute("SELECT last_warn_time FROM warn_list WHERE guild_id=? AND user_id=?",
                               (interaction.guild.id, member.id))
                warn_last = cursor.fetchone()
            except sqlite3.Error as e:
                logger.error(language["Errors"]["Standart"]["Error_message_with_code"].format(e=e))
                await interaction.response.send_message(language["Errors"]["Standart"]["Unknown_error"].format(e=e), ephemeral=True)
            try:
                embed = nextcord.Embed(title=f'{language["Moderation"]["Show"]["Title"].format(mention=member.name)}', color=nextcord.Color.dark_purple())
                embed.add_field(name=' ', value=f'{warn_emodji} {language["Moderation"]["Show"]["Count"].format(count=warn_count[0])}\n'
                                                f'{time_emodji} {language["Moderation"]["Show"]["Last"].format(last=warn_last[0])}')
                if interaction.guild.icon:
                    embed.set_footer(
                        text=f'• {interaction.guild.name} Warn | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                        icon_url=interaction.guild.icon.url)
                else:
                    embed.set_footer(
                        text=f'• {interaction.guild.name} Warn | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
                await interaction.response.send_message(embed=embed, ephemeral=True)
            except TypeError:
                embed = nextcord.Embed(title=language["Errors"]["Warn"]["Title"], color=nextcord.Color.dark_purple())
                embed.add_field(name='', value=f'{member_emodji} {language["Errors"]["Warn"]["Value"].format(member=member.name)}')
                if interaction.guild.icon:
                    embed.set_footer(
                        text=f'• {interaction.guild.name} Warn | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                        icon_url=interaction.guild.icon.url)
                else:
                    embed.set_footer(
                        text=f'• {interaction.guild.name} Warn | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
                await interaction.response.send_message(embed=embed, ephemeral=True)
        if action == 'give':
            try:
                database_location = connect_database(interaction.guild)
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
                logger.error(language["Errors"]["Standart"]["Error_message_with_code"].format(e=e))
                await interaction.response.send_message(language["Errors"]["Standart"]["Unknown_error"].format(e=e))
            logger.info(language["Logging"]["Warn"]["Warned"].format(member=member.name, user=interaction.user.name,
                                                                     reason=reason))
            embed = nextcord.Embed(title=f'{created_since_emodji} {language["Moderation"]["Warn"]["Title"]}', color=nextcord.Color.dark_purple())
            embed.add_field(name='', value=f'{staff_emodji} {language["Moderation"]["Warn"]["Admin"].format(mention=interaction.user.mention)}\n'
                                           f'{reason_emodji} {language["Moderation"]["Warn"]["Reason"].format(reason=reason)}\n'
                                           f'{warn_emodji} {language["Moderation"]["Warn"]["Warned"].format(user=member.mention)}\n'
                                           f'{created_since_emodji} {language["Moderation"]["Warn"]["Count"].format(count=embed_result[0])}')
            if interaction.guild.icon:
                embed.set_footer(
                    text=f'• {interaction.guild.name} Warn | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                    icon_url=interaction.guild.icon.url)
            else:
                embed.set_footer(
                    text=f'• {interaction.guild.name} Warn | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
            await interaction.response.send_message(embed=embed)

            if embed_result[0] >= 5:
                admin_role = nextcord.utils.get(interaction.guild.roles, name="Администратор")
                await member.remove_roles(admin_role, reason='too many warns')
                embed_warn = nextcord.Embed(title=f'{created_since_emodji} {language["Moderation"]["Admin_removal"]["Title"]}',
                                            color=nextcord.Color.red())
                embed_warn.add_field(name=f'{member_emodji} {language["Moderation"]["Admin_removal"]["Admin"].format(mention=member.name)}',
                                     value=f'{reason_emodji} {language["Moderation"]["Admin_removal"]["Reason"]}\n'
                                           f'{warn_emodji} {language["Moderation"]["Admin_removal"]["Lower"]}')
                if interaction.guild.icon:
                    embed_warn.set_footer(
                        text=f'• {interaction.guild.name} Reset | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                        icon_url=interaction.guild.icon.url)
                else:
                    embed_warn.set_footer(
                        text=f'• {interaction.guild.name} Reset | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
                cursor.execute("UPDATE warn_list SET warns = 0 WHERE user_id = ?", (member.id,))
                database_location.commit()
                database_location.close()
                await interaction.channel.send(embed=embed_warn)
    else:
        logger.info(language["Errors"]["User"]["Not_enough_rights"].format(user=interaction.user.name))
        await interaction.response.send_message(language["Errors"]["Standart"]["Not_enough_rights"],
                                                ephemeral=True)


@client_discord.slash_command(name='kick', description='Deletes a participant, the participant will be able to log in again')
async def kick(interaction: Interaction, member: nextcord.Member,
               reason: str = SlashOption(description='Reason for kick', default="Without reason")):
    global database_location
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    logger.info(language["Logging"]["Kick"]["Interaction"].format(name=interaction.user.name))
    if nextcord.utils.get(interaction.user.roles, name='Администратор') is not None:
        try:
            await member.kick(reason=reason)
            logger.info(language["Logging"]["Kick"]["Kicked"].format(member=member.name, user=interaction.user.name,
                                                                    reason=reason))
            try:
                database_location = connect_database(interaction.guild)
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
                logger.error(language["Errors"]["Standart"]["Error_message_with_code"].format(e=e))
                await interaction.response.send_message(language["Errors"]["Standart"]["Unknown_error"].format(e=e), ephemeral=True)
            finally:
                database_location.close()
            if reason in ['Without reason']:
                await warn(interaction, interaction.guild.id, interaction.user.id,
                           interaction.user.name)
            embed = nextcord.Embed(title=f'{created_since_emodji} {language["Moderation"]["Kick"]["Title"]}',
                                   color=nextcord.Color.dark_purple())
            embed.add_field(name=' ', value=f'{staff_emodji} {language["Moderation"]["Kick"]["Admin"].format(mention=interaction.user.mention)}\n'
                                            f'{reason_emodji} {language["Moderation"]["Kick"]["Reason"].format(reason=reason)}\n'
                                            f'{member_emodji} {language["Moderation"]["Kick"]["Kicked"].format(user=member.mention)}')
            if interaction.guild.icon:
                embed.set_footer(text=f'• {interaction.guild.name} Kick | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                                 icon_url=interaction.guild.icon.url)
            else:
                embed.set_footer(
                    text=f'• {interaction.guild.name} Kick | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
            await interaction.response.send_message(embed=embed)
        except nextcord.Forbidden:
            logger.error(language["Errors"]["Bot"]["Forbidden"])
            await interaction.response.send_message(language["Errors"]["Bot"]["Forbidden"],
                                                    ephemeral=True)
    else:
        logger.info(language["Errors"]["User"]["Not_enough_rights"].format(user=interaction.user.name))
        await interaction.response.send_message(language["Errors"]["Standart"]["Not_enough_rights"],
                                                ephemeral=True)


@client_discord.slash_command(name='server-info', description='Displays server statistics')
async def serverinfo(interaction: Interaction):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    logger.info(language["Logging"]["Serverinfo"]["Interaction"].format(name=interaction.user.name))
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        guild = interaction.guild
        bots = sum(1 for member in guild.members if member.bot)
        total_members = guild.member_count
        without_bot = total_members - bots

        verification_level = guild.verification_level
        if verification_level == guild.verification_level.low:
            if language == "Русский":
                verification_level = 'Низкий'
            elif language == 'English (US)' or language == 'English (UK)':
                verification_level = 'Low'
            elif language == 'Ukraine':
                verification_level = 'Низький'
            elif language == 'Finland':
                verification_level = 'Matala'
            elif language == 'Italy':
                verification_level = 'Basso'
            elif language == 'Spain':
                verification_level = 'Bajo'
            elif language == 'France':
                verification_level = 'Faible'
        elif verification_level == guild.verification_level.medium:
            if language == "Русский":
                verification_level = 'Средний'
            elif language == 'English (US)' or language == 'English (UK)':
                verification_level = 'Medium'
            elif language == 'Ukraine':
                verification_level = 'Середній'
            elif language == 'Finland':
                verification_level = 'Keskitaso'
            elif language == 'Italy':
                verification_level = 'Medio'
            elif language == 'Spain':
                verification_level = 'Medio'
            elif language == 'France':
                verification_level = 'Moyen'
        elif verification_level == guild.verification_level.high:
            if language == "Русский":
                verification_level = 'Высокий'
            elif language == 'English (US)' or language == 'English (UK)':
                verification_level = 'High'
            elif language == 'Ukraine':
                verification_level = 'Високий'
            elif language == 'Finland':
                verification_level = 'Korkea'
            elif language == 'Italy':
                verification_level = 'Alto'
            elif language == 'Spain':
                verification_level = 'Alto'
            elif language == 'France':
                verification_level = 'Élevé'
        else:
            if language == "Русский":
                verification_level = 'Нет'
            elif language == 'English (US)' or language == 'English (UK)':
                verification_level = 'None'
            elif language == 'Ukraine':
                verification_level = 'Немає'
            elif language == 'Finland':
                verification_level = 'Ei mitään'
            elif language == 'Italy':
                verification_level = 'Nessuno'
            elif language == 'Spain':
                verification_level = 'Ninguno'
            elif language == 'France':
                verification_level = 'Aucun'

        created_at = guild.created_at
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        total_channels = text_channels + voice_channels + categories

        embed = nextcord.Embed(title=guild.name, color=0x6fa8dc)
        try:
            embed.set_thumbnail(url=guild.icon.url)
        except AttributeError:
            pass
        embed.add_field(name=f'{language["ServerInfo"]["New_type"]["Main"]["Title"]}',
                        value=f'{guild_owner_emodji} {language["ServerInfo"]["New_type"]["Main"]["Owner"].format(owner=guild.owner.mention)}\n'
                              f'{verification_level_emodji} {language["ServerInfo"]["New_type"]["Main"]["Verification_lvl"].format(verification_level_show=verification_level)}\n'
                              f'{created_since_emodji} {language["ServerInfo"]["New_type"]["Main"]["Created_at"]} <t:{int(created_at.timestamp())}:F>\n(<t:{int(created_at.timestamp())}:R>)\n'
                              f'{slash_emodji} {language["ServerInfo"]["New_type"]["Main"]["About"].format(text_channels=text_channels, voice_channels=voice_channels, categories=categories, total_channels=total_channels)}\n'  # Используем результат
                              f'{text_emodji} {language["ServerInfo"]["New_type"]["Main"]["Text"].format(text_channels=text_channels)}\n'
                              f'{voice_emodji} {language["ServerInfo"]["New_type"]["Main"]["Voice"].format(voice_channels=voice_channels)}\n'
                              f'{categories_emodji} {language["ServerInfo"]["New_type"]["Main"]["Categories"].format(categories=categories)}\n')
        embed.add_field(name=f'{language["ServerInfo"]["New_type"]["Users"]["Title"]}',
                        value=f'{members_emodji} {language["ServerInfo"]["New_type"]["Users"]["About"].format(total_members=total_members)}\n'
                              f'{bot_emodji} {language["ServerInfo"]["New_type"]["Users"]["Bots"].format(bots=bots)}\n'
                              f'{member_emodji} {language["ServerInfo"]["New_type"]["Users"]["Members"].format(members=without_bot)}\n')
        boost_level = guild.premium_tier
        embed.add_field(name=f'{language["ServerInfo"]["New_type"]["Boosts"]["Title"]}',
                        value=f'{boost_emodji} {language["ServerInfo"]["New_type"]["Boosts"]["Level"].format(boost_level=boost_level)}\n ({language["ServerInfo"]["New_type"]["Boosts"]["Boosts"].format(boost_count=guild.premium_subscription_count)})\n')
        embed.add_field(name=f'{language["ServerInfo"]["New_type"]["Links"]["Title"]}',
                        value=f'{telegram_emodji} {language["ServerInfo"]["New_type"]["Links"]["Telegram"].format(telegram_link=telegram_channels_link)} \n'
                              f'{discord_emodji} {language["ServerInfo"]["New_type"]["Links"]["Discord"].format(discord_link=discord_server_link)}\n')
        if interaction.guild.icon:
            embed.set_footer(text=f'• {language["ServerInfo"]["New_type"]["Footer"]["Footer"].format(member=interaction.user.name)}\n'
                     f'• {interaction.guild.name} Serverinfo | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                             icon_url=interaction.guild.icon.url)
        else:
            embed.set_footer(
                text=f'• {language["ServerInfo"]["New_type"]["Footer"]["Footer"].format(member=interaction.user.name)}\n'
                     f'• {interaction.guild.name} Serverinfo | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(
            f'{language["Errors"]["Serverinfo"]["Error"]} <#1246752343182278747>', ephemeral=True)


@client_discord.slash_command(name='clear', description='Deletes messages')
async def clear(interaction: Interaction,
                limit: int = SlashOption(description='Number of messages (0 - delete all)')):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    logger.info(language["Logging"]["Clear"]["Interaction"].format(name=interaction.user.name))
    if nextcord.utils.get(interaction.user.roles, name='Администратор') is not None:
        try:
            if limit == 0:
                await interaction.channel.purge(limit=None)
            else:
                await interaction.channel.purge(limit=limit)

            if interaction.response.is_done():
                await interaction.followup.send(f'{language["Clear"]["Successfully"]}', ephemeral=True)
            else:
                await interaction.response.send_message(f'{language["Clear"]["Successfully"]}', ephemeral=True)
        except nextcord.errors.Forbidden:
            if interaction.response.is_done():
                await interaction.followup.send(language["Errors"]["Bot"]["Forbidden"], ephemeral=True)
            else:
                await interaction.response.send_message(language["Errors"]["Bot"]["Forbidden"], ephemeral=True)
        except ValueError:
            if interaction.response.is_done():
                await interaction.followup.send(language["Errors"]["Clear"]["Incorrect_value"], ephemeral=True)
            else:
                await interaction.response.send_message(language["Errors"]["Clear"]["Incorrect_value"], ephemeral=True)
    else:
        if interaction.response.is_done():
            logger.info(language["Errors"]["User"]["Not_enough_rights"].format(user=interaction.user.name))
            await interaction.followup.send(language["Errors"]["Standart"]["Not_enough_rights"], ephemeral=True)
        else:
            await interaction.response.send_message(language["Errors"]["User"]["Not_enough_rights"].format(user=interaction.user.name), ephemeral=True)


@client_discord.slash_command(name='members', description='Displays a list of all users')
async def members(interaction: Interaction):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    logger.info(language["Logging"]["Members"]["Interaction"].format(name=interaction.user.name))
    if nextcord.utils.get(interaction.user.roles, name='Администратор') is not None:
        guild = interaction.guild
        members_info = [f'{member_emodji} {member.mention}-{member.name} (ID: {member.id}) ({language["Members"]["Role"]} {member.top_role})' for member
                        in guild.members]

        embed = nextcord.Embed(title=f'{created_since_emodji} {language["Members"]["Title"]}', description='\n'.join(members_info), color=0xffffff)
        if interaction.guild.icon:
            embed.set_footer(text=f'• {interaction.guild.name} Info {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
                                  f'• {language["Members"]["Footer"].format(count=guild.member_count)}',
                             icon_url=interaction.guild.icon.url)
        else:
            embed.set_footer(
                text=f'• {interaction.guild.name} Info {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
                     f'• {language["Members"]["Footer"].format(count=guild.member_count)}')
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        logger.info(language["Errors"]["User"]["Not_enough_rights"].format(user=interaction.user.name))
        await interaction.response.send_message(language["Errors"]["Standart"]["Not_enough_rights"], ephemeral=True)


@client_discord.slash_command(name='mute-list', description='Displays a list of muted users')
async def mute_list(interaction: Interaction):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    logger.info(language["Logging"]["Mute_list"]["Interaction"].format(name=interaction.user.name))
    if nextcord.utils.get(interaction.user.roles, name="Администратор"):

        mutes = [f'{member_emodji} {member.mention} ({language["Mute_list"]["Role"]} {member.top_role})' for member in interaction.guild.members
                 if nextcord.utils.get(member.roles, name='Muted')]
        mutes_count = len(mutes)
        embed = nextcord.Embed(title=f'{created_since_emodji} {language["Mute_list"]["Title"]}', description='\n'.join(mutes),
                               color=nextcord.Color.dark_purple())
        if interaction.guild.icon:
            embed.set_footer(text=f'• {interaction.guild.name} Info | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
                                  f'• {language["Mute_list"]["Footer"].format(mute_count=mutes_count)}',
                             icon_url=interaction.guild.icon.url)
        else:
            embed.set_footer(
                text=f'• {interaction.guild.name} Info | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
                     f'• {language["Mute_list"]["Footer"].format(mute_count=mutes_count)}')
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        logger.info(language["Errors"]["User"]["Not_enough_rights"].format(user=interaction.user.name))
        await interaction.response.send_message(language["Errors"]["Standart"]["Not_enough_rights"], ephemeral=True)


@client_discord.slash_command(name='ban-list', description='Displays a list of blocked users')
async def ban_list(interaction: Interaction):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    logger.info(language["Logging"]["Ban_list"]["Interaction"].format(name=interaction.user.name))
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        ban_list = []
        async for ban_entry in interaction.guild.bans():
            ban_list.append(f'{member_emodji} {ban_entry.user} ({language["Ban_list"]["Reason"]}: {ban_entry.reason})')
        ban_count = len(ban_list)
        embed = nextcord.Embed(title=f'{created_since_emodji} {language["Ban_list"]["Title"]}', description='\n'.join(ban_list),
                               color=0xffffff)
        if interaction.guild.icon:
            embed.set_footer(
                text=f'• {interaction.guild.name} Info | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
                     f'• {language["Ban_list"]["Footer"].format(ban_count=ban_count)}',
                icon_url=interaction.guild.icon.url)
        else:
            embed.set_footer(
                text=f'• {interaction.guild.name} Info | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
                     f'• {language["Ban_list"]["Footer"].format(ban_count=ban_count)}')
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        logger.info(language["Errors"]["User"]["Not_enough_rights"].format(user=interaction.user.name))
        await interaction.response.send_message(language["Errors"]["Standart"]["Not_enough_rights"], ephemeral=True)


@client_discord.slash_command(name='help', description='Displays a list of bot commands')
async def help(interaction: Interaction,
             rank: str = SlashOption(
                  name="rank",
                  description='Select a rank: mod или default',
                  choices=['default', 'mod'],
                  default='default'
             )
             ):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    if rank == 'default':
        logger.info(language["Logging"]["Help"]["Default"]["Interaction"].format(name=interaction.user.name))
        embed = nextcord.Embed(title=f'{language["Info"]["Default"]["Title"]}', color=0x999999)
        embed.add_field(
            name=f'{language["Info"]["Default"]["Tab1"]}',
            value=f'**/help**\n'
                  f'**/avatar**\n'
                  f'**/weather**\n'
                  f'**/info**\n'
                  f'**/links**\n'
                  f'**/author-links**\n'
                  f'**/invites**\n',
            inline=True
        )
        if interaction.guild.icon:
            embed.set_footer(
                text=f'• {interaction.guild.name} Help | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                icon_url=interaction.guild.icon.url)
        else:
            embed.set_footer(
                text=f'• {interaction.guild.name} Help | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
        await interaction.response.send_message(embed=embed, ephemeral=True)
    elif rank == 'mod':
        if nextcord.utils.get(interaction.user.roles, name='Администратор') is not None:
            logger.info(language["Logging"]["Help"]["Moderation"]["Interaction"].format(name=interaction.user.name))
            embed = nextcord.Embed(title=f'{created_since_emodji} {language["Help"]["Moderation"]["Title"]} {created_since_emodji}',
                                   description=f'{language["Help"]["Moderation"]["Header"]}',
                                   color=0x999999)
            embed.add_field(
                name=f'{language["Help"]["Moderation"]["Tab1"]}',
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
                name=f'{language["Help"]["Moderation"]["Tab2"]}\n',
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
                name=f'{language["Help"]["Moderation"]["Tab3"]}',
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
            if interaction.guild.icon:
                embed.set_footer(
                    text=f'• {interaction.guild.name} Help | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                    icon_url=interaction.guild.icon.url)
            else:
                embed.set_footer(
                    text=f'• {interaction.guild.name} Help | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            logger.info(language["Errors"]["User"]["Not_enough_rights"].format(user=interaction.user.name))
            await interaction.response.send_message(language["Errors"]["Standart"]["Not_enough_rights"], ephemeral=True)


@client_discord.slash_command(name='mute', description='Mutes out the participant')
async def mute(interaction: Interaction, member: nextcord.Member,
               reason: str = SlashOption(description='The reason for the mute',
                                         default="Without reason")):
    global database_location
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    logger.info(language["Logging"]["Mute"]["Interaction"].format(name=interaction.user.name))
    if nextcord.utils.get(interaction.user.roles, name='Администратор') is not None:
        try:
            mute_role = nextcord.utils.get(interaction.guild.roles, name="Muted")
            if not mute_role:
                mute_role = await interaction.guild.create_role(name="Muted",permissions=discord.Permissions(send_messages=False,speak=False))
                await mute_role.edit(position=1)
            await member.add_roles(mute_role, reason=reason)
            logger.info(language["Logging"]["Mute"]["Muted"].format(member=member.name, user=interaction.user.name,
                                                                    reason=reason))
            try:
                database_location = connect_database(interaction.guild)
                cursor = database_location.cursor()
                cursor.execute("""
                    INSERT INTO mod_actions (action_type, guild_id, moderator_name, moderator_id, target_user_name, target_user_id, reason, action_time) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, ('Mute', interaction.guild.id, interaction.user.name, interaction.user.id, member.name, member.id, reason,
                      datetime.datetime.now()))
                database_location.commit()
            except sqlite3.Error as e:
                logger.error(language["Errors"]["Standart"]["Error_message_with_code"].format(e=e))
                await interaction.response.send_message(language["Errors"]["Standart"]["Unknown_error"].format(e=e), ephemeral=True)
            finally:
                database_location.close()
            if reason in ['Without reason']:
                await warn(interaction, interaction.guild.id, interaction.user.id,
                           interaction.user.name)
            embed = nextcord.Embed(title=f'{created_since_emodji} {language["Moderation"]["Mute"]["Title"]}', color=nextcord.Color.dark_purple())
            embed.add_field(name=' ', value=f'{staff_emodji} {language["Moderation"]["Mute"]["Admin"].format(mention=interaction.user.mention)}\n'
                                            f'{reason_emodji} {language["Moderation"]["Mute"]["Reason"].format(reason=reason)}\n'
                                            f'{member_emodji} {language["Moderation"]["Mute"]["Muted"].format(user=member.mention)}')
            if interaction.guild.icon:
                embed.set_footer(
                    text=f'• {interaction.guild.name} Mute | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                    icon_url=interaction.guild.icon.url)
            else:
                embed.set_footer(
                    text=f'• {interaction.guild.name} Mute | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
            await interaction.response.send_message(embed=embed)
        except nextcord.Forbidden:
            logger.error(language["Errors"]["Bot"]["Forbidden"])
            await interaction.response.send_message(language["Errors"]["Bot"]["Forbidden"],
                                                    ephemeral=True)
    else:
        logger.info(language["Errors"]["User"]["Not_enough_rights"].format(user=interaction.user.name))
        await interaction.response.send_message(language["Errors"]["Standart"]["Not_enough_rights"],
                                                ephemeral=True)


@client_discord.slash_command(name='unmute', description='Removes the participant mute')
async def unmute(interaction: Interaction, member: nextcord.Member,
                 reason: str = SlashOption(description='The reason for the mute', default="Without reason")):
    global database_location
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    logger.info(language["Logging"]["Unmute"]["Interaction"].format(name=interaction.user.name))
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        try:
            mute_role = nextcord.utils.get(interaction.guild.roles, name="Muted")
            if not mute_role:
                mute_role = await interaction.guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False, speak=False))
                await mute_role.edit(position=1)
            await member.remove_roles(mute_role, reason=reason)
            logger.info(language["Logging"]["Unmute"]["Unmuted"].format(member=member.name, user=interaction.user.name,
                                                                    reason=reason))
            try:
                database_location = connect_database(interaction.guild)
                cursor = database_location.cursor()
                cursor.execute("""
                    INSERT INTO mod_actions (action_type, guild_id, moderator_name, moderator_id, target_user_name, target_user_id, reason, action_time) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, ('Unmute', interaction.guild.id, interaction.user.name, interaction.user.id, member.name, member.id, reason,
                      datetime.datetime.now()))
                database_location.commit()
            except sqlite3.Error as e:
                logger.error(language["Errors"]["Standart"]["Error_message_with_code"].format(e=e))
                await interaction.response.send_message(language["Errors"]["Standart"]["Unknown_error"].format(e=e))
            finally:
                database_location.close()
            if reason in ['Without reason']:
                await warn(interaction, interaction.guild.id, interaction.user.id,
                           interaction.user.name)
            embed = nextcord.Embed(title=f'{created_since_emodji} {language["Moderation"]["Unmute"]["Title"]}', color=nextcord.Color.dark_purple())
            embed.add_field(name=' ', value=f'{staff_emodji} {language["Moderation"]["Unmute"]["Admin"].format(mention=interaction.user.mention)}\n'
                                            f'{reason_emodji} {language["Moderation"]["Unmute"]["Reason"].format(reason=reason)}\n'
                                            f'{member_emodji} {language["Moderation"]["Unmute"]["Unmuted"].format(user=member.mention)}')
            if interaction.guild.icon:
                embed.set_footer(
                    text=f'• {interaction.guild.name} Unmute | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                    icon_url=interaction.guild.icon.url)
            else:
                embed.set_footer(
                    text=f'• {interaction.guild.name} Unmute | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
            await interaction.response.send_message(embed=embed)
        except nextcord.Forbidden:
            logger.error(language["Errors"]["Bot"]["Forbidden"])
            await interaction.response.send_message(language["Errors"]["Bot"]["Forbidden"], ephemeral=True)
    else:
        logger.info(language["Errors"]["User"]["Not_enough_rights"].format(user=interaction.user.name))
        await interaction.response.send_message(language["Errors"]["Standart"]["Not_enough_rights"], ephemeral=True)


@client_discord.slash_command(name='unban', description='Removes the lock from the user')
async def unban(interaction: Interaction, user_id: str,
                reason: str = SlashOption(description='Reason for blocking',
                                          default='Without reason')):
    global database_location
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    logger.info(language["Logging"]["Unban"]["Interaction"].format(name=interaction.user.name))

    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        try:
            user = await client_discord.fetch_user(int(user_id))
            await interaction.guild.unban(user, reason=reason)
            embed = nextcord.Embed(title=f'{created_since_emodji} {language["Moderation"]["Unban"]["Title"]}', color=nextcord.Color.dark_purple())
            embed.add_field(name=' ', value=f'{staff_emodji} {language["Moderation"]["Unban"]["Admin"].format(mention=interaction.user.mention)}\n'
                                            f'{reason_emodji} {language["Moderation"]["Unban"]["Reason"].format(reason=reason)}\n'
                                            f'{member_emodji} {language["Moderation"]["Unban"]["Unbanned"].format(user=user.mention)}\n')
            if interaction.guild.icon:
                embed.set_footer(
                    text=f'• {interaction.guild.name} Unban | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                    icon_url=interaction.guild.icon.url)
            else:
                embed.set_footer(
                    text=f'• {interaction.guild.name} Unban | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')

            if reason == 'Without reason':
                await warn(interaction, interaction.guild.id, interaction.user.id,
                           interaction.user.name)

            try:
                database_location = connect_database(interaction.guild)
                cursor = database_location.cursor()
                cursor.execute("""
                    INSERT INTO mod_actions (action_type, guild_id, moderator_name, moderator_id, target_user_name, target_user_id, reason, action_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, ('Unban', interaction.guild.id, interaction.user.name, interaction.user.id,
                      user.name, user.id, reason, datetime.datetime.now()))
                database_location.commit()
            except sqlite3.Error as e:
                logger.error(language["Errors"]["Standart"]["Error_message_with_code"].format(e=e))
                await interaction.response.send_message(language["Errors"]["Standart"]["Unknown_error"].format(e=e))

            finally:
                database_location.close()

            await interaction.response.send_message(embed=embed)
        except nextcord.errors.Forbidden:
            logger.error(language["Errors"]["Bot"]["Forbidden"])
            await interaction.response.send_message(language["Errors"]["Bot"]["Forbidden"], ephemeral=True)
        except nextcord.errors.NotFound:
            logger.error(language["Errors"]["Unban"]["Not_Found"]["Error"])
            await interaction.response.send_message(language["Errors"]["Unban"]["Not_Found"]["Error"], ephemeral=True)
    else:
        await interaction.response.send_message(language["Errors"]["Standart"]["Not_enough_rights"], ephemeral=True)


@client_discord.slash_command(name='info', description='Sends information about the participant')
async def info(interaction: Interaction, member: nextcord.Member,
               hidden: str = SlashOption(
                   name="hidden",
                   description='Choose how the message will be sent',
                   choices=['hidden', 'shown'],
                   default='hidden'
               )):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    logger.info(language["Logging"]["Info"]["Interaction"].format(name=interaction.user.name))
    excepted_roles = ["@everyone", "Member"]
    role_count = len([role.name for role in member.roles if role.name not in excepted_roles])
    roles = member.roles
    role_names = [f'<@&{role.id}>' for role in roles if role.name not in excepted_roles]
    role_list = ' '.join(role_names)
    discriminator = member.discriminator
    if discriminator == 0:
        discriminator = None
    embed = nextcord.Embed(title=f'{language["Info"]["Title"].format(member=member.name)}', color=0xffffff)
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name=f'{language["Info"]["Nickname"]}', value=member.name, inline=True)
    embed.add_field(name=f'{language["Info"]["Mention"]}', value=member.mention, inline=True)
    embed.add_field(name=f'{language["Info"]["Full_name"]}', value=f'{member.name}#{discriminator}', inline=True)
    embed.add_field(name=f'{language["Info"]["Id"]}', value=member.id, inline=True)
    embed.add_field(name=f'{language["Info"]["Joined_date"]}', value=f'<t:{int(member.joined_at.timestamp())}:R>', inline=True)
    embed.add_field(name=f'{language["Info"]["Created_date"]}', value=f'<t:{int(member.created_at.timestamp())}:R>')
    embed.add_field(name=f'{language["Info"]["Main_role"]}', value=f'<@&{member.top_role.id}>', inline=True)
    embed.add_field(name=f'{language["Info"]["Roles"]}', value=role_list)
    embed.add_field(name=f'{language["Info"]["Count_roles"]}', value=role_count)
    if interaction.guild.icon:
        embed.set_footer(
            text=f'• {interaction.guild.name} Info | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
            icon_url=interaction.guild.icon.url)
    else:
        embed.set_footer(
            text=f'• {interaction.guild.name} Info | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
    if hidden == 'hidden':
        await interaction.response.send_message(embed=embed, ephemeral=True)
    elif hidden == 'shown':
        if nextcord.utils.get(interaction.user.roles, name='Администратор'):
            await interaction.response.send_message(embed=embed, ephemeral=False)
        else:
            logger.info(language["Errors"]["User"]["Not_enough_rights"].format(user=interaction.user.name))
            await interaction.response.send_message(language["Errors"]["Standart"]["Not_enough_rights"], ephemeral=True)


@client_discord.slash_command(name='say', description='Sends a message on behalf of the bot')
async def say(interaction: Interaction, message: str = SlashOption(description='Отправляет текст введённый здесь')):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    logger.info(language["Logging"]["Say"]["Interaction"].format(name=interaction.user.name))
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        await interaction.channel.send(message)
        await interaction.response.send_message(f'{language["Say"]["Successfully"]}', ephemeral=True)
        logger.info(language["Logging"]["Say"]["Sended"].format(name=interaction.user.name))
    else:
        await interaction.response.send_message(language["Errors"]["Standart"]["Not_enough_rights"], ephemeral=True)


@client_discord.slash_command(name='avatar', description='Sends the user avatar')
async def avatar_interaction(interaction: Interaction, member: nextcord.Member):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    logger.info(language["Logging"]["Avatar"]["Interaction"].format(name=interaction.user.name))
    embed = nextcord.Embed(title=f'Аватар {member.name}', color=0xffffff)
    embed.set_image(url=member.avatar.url)
    if interaction.guild.icon:
        embed.set_footer(
            text=f'• {interaction.guild.name} Avatar | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
            icon_url=interaction.guild.icon.url)
    else:
        embed.set_footer(
            text=f'• {interaction.guild.name} Avatar | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='log', description='Sends actions with logs')
async def log(interaction: Interaction,
              content: str = SlashOption(
                  name="action",
                  description='Select the action you want to perform with the logs',
                  choices=['download',  'save', 'archive', 'delete']
              ),
              target: str = SlashOption(
                  name="target",
                  description='Choose where the download will be from: current, archive or any other file name',
                  default='current'
              )
              ):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    logger.info(language["Logging"]["Log"]["Interaction"].format(name=interaction.user.name))
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        if content.lower() in ['delete']:
            if target in ['archive']:
                folder_path = f'Database/{interaction.guild.id}/archive_logs'
                if os.path.exists(folder_path):
                    for filename in os.listdir(folder_path):
                        file_path = os.path.join(folder_path, filename)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    await interaction.response.send_message(language["Log"]["Delete"]["Archive"]["Successfully"],
                                                            ephemeral=True)
                    win_notification('User clear archive logs',
                                     f'{interaction.user.name} cleared archive log files\n'
                                     f'Time: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
                else:
                    logger.error(language["Errors"]["Standart"]["Folder_Not_Found"])
                    await interaction.response.send_message(language["Errors"]["Standart"]["Folder_Not_Found"],
                                                            ephemeral=True)
            else:
                await interaction.response.send_message(language["Errors"]["Standart"]["Not_enough_rights"], ephemeral=True)
            if target in ['current']:
                logging.shutdown()
                open(f'Database/{interaction.guild.id}/{interaction.guild.id}.log', 'w').close()
                logging.basicConfig(filename=f'Database/{interaction.guild.id}/{interaction.guild.id}.log', level=logging.INFO, encoding='utf-8')
                await interaction.response.send_message(language["Log"]["Delete"]["Successfully"], ephemeral=True)
                win_notification('User clear current log', f'{interaction.user.name} cleared main logging file\nServer {interaction.guild.name}\nTime: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
        if content.lower() in ['download', 'Download', 'dowload', 'Dowload']:
            if content == 'download':
                if target == 'current':
                    logger.info(language["Logging"]["Log"]["Request_current"].format(name=interaction.user.name))
                    await interaction.response.send_message(file=nextcord.File(f'Database/{interaction.guild.id}/log.log'),
                                                            ephemeral=True)
                    win_notification('User downloaded log',
                                     f'Current log file downloaded by {interaction.user.name}\n'
                                     f'Server: {interaction.guild.name}')
                elif target in ['Archive', 'archive']:
                    logger.info(language["Logging"]["Log"]["Request_archive"].format(name=interaction.user.name))
                    archive_logs_dir = os.path.join(os.getcwd(), f'Database/{interaction.guild.id}/archive_logs')
                    files = os.listdir(archive_logs_dir)
                    await interaction.response.defer(ephemeral=True)
                    for file in files:
                        file_path = os.path.join(archive_logs_dir, file)
                        await interaction.followup.send(file=nextcord.File(file_path), ephemeral=True)
                    win_notification('User downloaded log',
                                     f'{interaction.user.name} downloaded archive log files\nTime: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
                else:
                    logger.info(language["Logging"]["Log"]["Request_else"].format(name=interaction.user.name))
                    try:
                        await interaction.response.send_message(file=nextcord.File(f'Database/{interaction.guild.id}/archive_logs/{target}'),
                                                                ephemeral=True)
                    except FileNotFoundError:
                        await interaction.response.send_message(language["Errors"]["Standart"]["File_Not_Found"], ephemeral=True)
                    win_notification('User downloaded log', f'{target} downloaded by {interaction.user.name}')

            else:
                await interaction.response.send_message(language["Errors"]["Log"]["Download"]["Incorrect_action"], ephemeral=True)
        elif content.lower() in ['save', 'Save']:
            log_channel = nextcord.utils.get(interaction.guild.channels, name='logs')
            if log_channel:
                file = f'Database/{interaction.guild.id}/{interaction.guild.id}.log'
                with open(file, 'r', encoding='utf-8') as file1:
                    first_line_temp = file1.readline()
                    first_line = first_line_temp.strip()
                log_datetime_str = first_line.split(' ', 1)[0]
                log_datetime = datetime.datetime.strptime(log_datetime_str, "%Y-%m-%d")

                last_change_time = os.path.getmtime(f'Database/{interaction.guild.id}/{interaction.guild.id}.log')
                last_change_timestamp = int(last_change_time)

                try:
                    await log_channel.send(file=nextcord.File(f'Database/{interaction.guild.id}/{interaction.guild.id}.log'))
                    await log_channel.send(
                        f'{language["Log"]["Save"]["Title"]}\n'
                        f'{language["Log"]["Save"]["Header"].format(member=interaction.user.mention)}\n'
                        f'{language["Log"]["Save"]["Center"]} <t:{int(log_datetime.timestamp())}:R>\n'
                        f'{language["Log"]["Save"]["Lower"]} <t:{last_change_timestamp}:R>'
                    )
                except nextcord.errors.Forbidden:
                    await interaction.response.send_message(language["Errors"]["Log"]["Permissions_Log"], ephemeral=True)

                logging.shutdown()
                if not os.path.exists('archive_logs'):
                    os.makedirs('archive_logs')

                new_log_name = f"log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
                new_log_path = os.path.join(f'Database/{interaction.guild.id}/archive_logs', new_log_name)

                shutil.move(f'Database/{interaction.guild.id}/{interaction.guild.id}.log', new_log_path)

                open(f'Database/{interaction.guild.id}/{interaction.guild.id}.log', 'w').close()

                logging.basicConfig(filename=f'Database/{interaction.guild.id}/{interaction.guild.id}.log', level=logging.INFO, encoding='utf-8')
                await interaction.response.send_message(language["Log"]["Send"]["Successfully"], ephemeral=True)
                win_notification('User rewrited (save) log',
                                 f'{interaction.user.name} rewrited current log file\nServer: {interaction.guild.name}\nTime: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
            else:
                await interaction.response.send_message(language["Errors"]["Log"]["Channel_Not_Found"], ephemeral=True)
        elif content.lower() in ['archive', 'Archive']:
            archive_logs_dir = os.path.join(os.getcwd(), f'Database/{interaction.guild.id}/archive_logs')

            if not os.path.exists(archive_logs_dir) or not os.path.isdir(archive_logs_dir):
                await interaction.response.send_message(language["Errors"]["Log"]["Folder_Not_Found"], ephemeral=True)
                return

            files = os.listdir(archive_logs_dir)

            embed = nextcord.Embed(title=f"List of files in the log archive", color=0xffffff)

            for file in files:
                file_path = os.path.join(archive_logs_dir, file)
                file_size = os.path.getsize(file_path)
                embed.add_field(name=file, value=f"Size: {(file_size/1024.0):.2f}kb", inline=False)
                if interaction.guild.icon:
                    embed.set_footer(
                        text=f'• {interaction.guild.name} Log | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                        icon_url=interaction.guild.icon.url)
                else:
                    embed.set_footer(
                        text=f'• {interaction.guild.name} Log | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        logger.info(language["Errors"]["User"]["Not_enough_rights"].format(user=interaction.user.name))
        await interaction.response.send_message(language["Errors"]["Standart"]["Not_enough_rights"], ephemeral=True)


@client_discord.slash_command(name='weather', description='Sends the weather in the specified city')
async def weather(interaction: Interaction, city: str = SlashOption(description='Specify the city')):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    logger.info(language["Logging"]["Weather"]["Interaction"].format(name=interaction.user.name))

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_Weather}&units=metric'
    response = requests.get(url)
    logger.info(language["Logging"]["Weather"]["Request"])

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
            logger.info(language["Logging"]["Weather"]["Successfully"].format(city=city))
        except KeyError:
            logger.error(language["Errors"]["Weather"]["Description"]["Error"])
            embed = nextcord.Embed(title=language["Errors"]["Weather"]["Title"], color=0xff0000)
            embed.add_field(name=language["Errors"]["Weather"]["Description"]["Error"], value=language["Errors"]["Weather"]["Description"]["Request_error"])
            if interaction.guild.icon:
                embed.set_footer(
                    text=f'• {interaction.guild.name} Weather | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                    icon_url=interaction.guild.icon.url)
            else:
                embed.set_footer(
                    text=f'• {interaction.guild.name} Weather | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            url_png = f"https://tile.openweathermap.org/map/temp_new/0/0/0.png?appid={API_Weather}"
            embed = nextcord.Embed(title=f'{language["Weather"]["Title"].format(city=city)}', color=0x376abd)
            embed.set_thumbnail(url=url_png)
            embed.add_field(
                name=f'{language["Weather"]["Description"]["Title"].format(city=city, country=filtered_data["Country"])}',
                value=f'{language["Weather"]["Description"]["Average_temp"].format(temp=filtered_data["Temp"])}\n'
                      f'{language["Weather"]["Description"]["Minimum_temp"].format(temp=filtered_data["Temp_min"])}\n'
                      f'{language["Weather"]["Description"]["Maximum_temp"].format(temp=filtered_data["Temp_max"])}\n'
                      f'{language["Weather"]["Description"]["Feels_temp"].format(temp=filtered_data["Feels_like"])}\n'
                      f'{language["Weather"]["Description"]["Wind_speed"].format(speed=filtered_data["Wind_speed"])}\n'
                      f'{language["Weather"]["Description"]["Humidity"].format(humidity=filtered_data["Humidity"])}\n'
                      f'{language["Weather"]["Description"]["Received"].format(time=datetime.datetime.now().strftime("%m-%d %H:%M"))}\n'
                      f'{language["Weather"]["Description"]["Request_author"].format(mention=interaction.user.mention)}\n'
                      f'{language["Weather"]["Description"]["Source"].format(source=filtered_data["City_id"])}'
            )
            if interaction.guild.icon:
                embed.set_footer(
                    text=f'• {interaction.guild.name} Weather | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                    icon_url=interaction.guild.icon.url)
            else:
                embed.set_footer(
                    text=f'• {interaction.guild.name} Weather | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except requests.exceptions.HTTPError as e:
            logger.error(language["Errors"]["Weather"]["Description"]["HTTP_error"].format(e=e))
            embed = nextcord.Embed(title=language["Weather"]["Title"], color=0xff0000)
            embed.add_field(name=language["Weather"]["Description"]["Title"], value=language["Weather"]["Description"]["Server_invalid"])
            if interaction.guild.icon:
                embed.set_footer(
                    text=f'• {interaction.guild.name} Weather | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                    icon_url=interaction.guild.icon.url)
            else:
                embed.set_footer(
                    text=f'• {interaction.guild.name} Weather | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except requests.exceptions.RequestException:
            logger.error(language["Weather"]["Description"]["Value"])
            embed = nextcord.Embed(title=language["Weather"]["Title"], color=0xff0000)
            embed.add_field(name=language["Weather"]["Description"]["Title"], value=language["Weather"]["Description"]["Value"])
            if interaction.guild.icon:
                embed.set_footer(
                    text=f'• {interaction.guild.name} Weather | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                    icon_url=interaction.guild.icon.url)
            else:
                embed.set_footer(
                    text=f'• {interaction.guild.name} Weather | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        logger.error(language["Weather"]["Description"]["Title"])
        embed = nextcord.Embed(title=language["Weather"]["Title"], color=0xff0000)
        embed.add_field(name=language["Weather"]["Description"]["Title"], value='')
        if interaction.guild.icon:
            embed.set_footer(text=f'• {interaction.guild.name} Weather | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                             icon_url=interaction.guild.icon.url)
        else:
            embed.set_footer(
                text=f'• {interaction.guild.name} Weather | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
        await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='database', description='Server Database Management')
async def database(interaction: Interaction,
                   content: str = SlashOption(
                       name="action",
                       description='Database action',
                       choices=['update', 'download', 'save', 'archive']
                   ),
                   target: str = SlashOption(
                       name='target',
                       description='Select which file you want to download',
                       default='current'
                   )):
    global database_location
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    guild = interaction.guild
    logger = guild_logger(guild)
    logger.info(language["Logging"]["Database"]["Interaction"].format(name=interaction.user.name))
    directory_path = os.path.join('Database', f'{guild.id}')

    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        if content == 'update':
            try:
                database_location = connect_database(guild)
                cursor = database_location.cursor()

                users_data = [(member.id, member.name, member.mention, member.joined_at) for member in guild.members]
                cursor.executemany(
                    "INSERT OR IGNORE INTO users_list (user_id, user_name, user_mention, user_joined_date) VALUES (?, ?, ?, ?)",
                    users_data
                )

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tickets_reputation (
                        guild_id INTEGER NOT NULL,
                        user_id INTEGER NOT NULL,
                        user_name TEXT NOT NULL
                    )
                """)

                admin_list = [(guild.id, member.id, member.name) for member in guild.members if any(role.name == 'Администратор' for role in member.roles)]
                cursor.executemany(
                    "INSERT OR IGNORE INTO tickets_reputation (guild_id, user_id, user_name) VALUES (?, ?, ?)",
                    admin_list
                )

                database_location.commit()
                await interaction.response.send_message(f'{language["Database"]["Start"]["Response"].format(name=guild.name)}', ephemeral=True)

            except sqlite3.Error as e:
                logger.error(language["Errors"]["Database"]["Error_when_working"].format(e=e))
                await interaction.response.send_message(language["Errors"]["Database"]["Error_when_working"].format(e=e), ephemeral=True)

            except Exception as e:
                logger.error(language["Errors"]["Standart"]["Error_message_with_code"].format(e=e))
                await interaction.response.send_message(language["Errors"]["Standart"]["Error_message_with_code"].format(e=e), ephemeral=True)

            finally:
                if database_location:
                    database_location.close()

        elif content == 'download':
            try:
                if target == 'current':
                    file_path = os.path.join(directory_path, f'{guild.id}.db')
                    await interaction.response.send_message(file=nextcord.File(file_path), ephemeral=True)
                else:
                    file_path = os.path.join(directory_path, 'archive_database', target)
                    await interaction.response.send_message(file=nextcord.File(file_path), ephemeral=True)
            except FileNotFoundError:
                await interaction.response.send_message(language["Errors"]["Standart"]["File_Not_Found"], ephemeral=True)

        elif content == 'save':
            try:
                database_location = connect_database(guild)
                database_location.commit()
                shutil.copy2(
                    f'{directory_path}/{guild.id}.db',
                    f'{directory_path}/archive_database/{guild.id}-{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.db'
                )
                await interaction.response.send_message(f'{language["Database"]["Save"]["Response"].format(name=f"{guild.id}")}', ephemeral=True)

                database_channel = nextcord.utils.get(guild.channels, name='database')
                if database_channel:
                    last_change_time = os.path.getmtime(f'{directory_path}/{guild.id}.db')
                    last_change_timestamp = int(last_change_time)
                    await database_channel.send(file=nextcord.File(f'{directory_path}/{guild.id}.db'))
                    await database_channel.send(
                        f'{language["Database"]["Save"]["Header"]}\n'
                        f'{language["Database"]["Save"]["Center"].format(called=interaction.user.mention)}\n'
                        f'{language["Database"]["Save"]["Lower"].format(last_change_timestamp=last_change_timestamp)}'
                    )
            except FileNotFoundError:
                await interaction.response.send_message(language["Errors"]["Standart"]["File_Not_Found"], ephemeral=True)

            except OSError as e:
                logger.error(language["Errors"]["Os"]["Copy_error"].format(e=e))

            finally:
                if database_location:
                    database_location.close()

        elif content.lower() == 'archive':
            archive_database_dir = os.path.join(directory_path, 'archive_database')

            if not os.path.exists(archive_database_dir) or not os.path.isdir(archive_database_dir):
                await interaction.response.send_message(language["Errors"]["Database"]["Folder_Not_Found"], ephemeral=True)
                return

            files = os.listdir(archive_database_dir)
            embed = nextcord.Embed(title=language["Database"]["Archive"]["Title"], color=0xffffff)

            for file in files:
                file_path = os.path.join(archive_database_dir, file)
                file_size = os.path.getsize(file_path)
                embed.add_field(
                    name=file,
                    value=f'{language["Database"]["Archive"]["Header"].format(file_size=file_size / 1024.0)}\n',
                    inline=False
                )

            embed.set_footer(
                text=f'• {guild.name} Database | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                icon_url=guild.icon.url if guild.icon else None
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

    else:
        await interaction.response.send_message(f'{language["Errors"]["Standart"]["Not_enough_rights"]}', ephemeral=True)


@client_discord.slash_command(name='ticket-menu', description='Message output for the referral system')
async def menu(interaction: Interaction):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        view = TicketView()
        embed = nextcord.Embed(title=f'{language["Menu"]["Ticket"]["Title"]}', color=0xffffff)
        embed.add_field(name=f'{created_since_emodji} • {language["Menu"]["Ticket"]["Header"]}',
                        value=f'{reason_emodji} • {language["Menu"]["Ticket"]["Lower"]}')
        if interaction.guild.icon:
            embed.set_footer(
                text=f'• {interaction.guild.name} Tickets | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                icon_url=interaction.guild.icon.url)
        else:
            embed.set_footer(
                text=f'• {interaction.guild.name} Tickets | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message(f'{language["Success"]["Send_message"]}', ephemeral=True)
    else:
        await interaction.response.send_message(f'{language["Errors"]["Standart"]["Not_enough_rights"]}', ephemeral=True)


@client_discord.slash_command(name='verify-menu', description='Message output for the verification system')
async def menu(interaction: Interaction):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        view = VerifyView()
        embed = nextcord.Embed(title=f'{language["Menu"]["Verify"]["Title"]}', color=0xffffff)
        embed.add_field(name=f'{created_since_emodji} • {language["Menu"]["Verify"]["Header"]}',
                        value=f'{reason_emodji} • {language["Menu"]["Verify"]["Center"]}\n'
                              f'{warn_emodji} • {language["Menu"]["Verify"]["Lower"]}')
        if interaction.guild.icon:
            embed.set_footer(
                text=f'• {interaction.guild.name} Verify | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                icon_url=interaction.guild.icon.url)
        else:
            embed.set_footer(
                text=f'• {interaction.guild.name} Verify | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message(f'{language["Success"]["Send_message"]}', ephemeral=True)
    else:
        await interaction.response.send_message(f'{language["Errors"]["Standart"]["Not_enough_rights"]}', ephemeral=True)


@client_discord.slash_command(name='getrole-menu', description='Message output for the group selection system')
async def menu(interaction: Interaction):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        view = GetroleView()
        embed = nextcord.Embed(title=f'{language["Menu"]["Getrole"]["Title"]}', color=0xffffff)
        embed.add_field(name=f'{created_since_emodji} • {language["Menu"]["Getrole"]["Header"]}',
                        value=f'{reason_emodji} • {language["Menu"]["Getrole"]["Center"]}\n'
                              f'{warn_emodji} • {language["Menu"]["Getrole"]["Lower"]}')
        if interaction.guild.icon:
            embed.set_footer(
                text=f'• {interaction.guild.name} Getrole | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                icon_url=interaction.guild.icon.url)
        else:
            embed.set_footer(
                text=f'• {interaction.guild.name} Getrole | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message(f'{language["Success"]["Send_message"]}', ephemeral=True)
    else:
        await interaction.response.send_message(f'{language["Errors"]["Standart"]["Not_enough_rights"]}', ephemeral=True)


@client_discord.slash_command(name='language', description='Select the language for the discord bot on your server')
async def menu(interaction: Interaction):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        view = SettingsView()
        embed = nextcord.Embed(
            title=f"{created_since_emodji} Выбор языка / Language Selection",
            description=f"{created_since_emodji} Please, choose one of language in list below:",
            color=0xffffff
        )

        embed.add_field(name=f"<:customemoji:1272602729948123136> Русский:",
                        value=f"{created_since_emodji} Используйте выпадающий список ниже, чтобы установить предпочитаемый язык (Русский).",
                        inline=False)

        embed.add_field(name=f"<:customemoji:1272602527208181771> English (US):",
                        value=f"{created_since_emodji} Use the dropdown menu below to set your preferred language (English US).",
                        inline=False)

        embed.add_field(name=f"<:customemoji:1272602644900347914> English (UK):",
                        value=f"{created_since_emodji} Use the dropdown menu below to set your preferred language (English UK).",
                        inline=False)

        embed.add_field(name=f"<:customemoji:1272602710415249441> Українська:",
                        value=f"{created_since_emodji} Використовуйте випадаюче меню нижче, щоб встановити бажану мову (Українська).",
                        inline=False)

        embed.add_field(name=f"<:customemoji:1272602680509988946> Suomi:",
                        value=f"{created_since_emodji} Valitse kieli alla olevasta pudotusvalikosta (Suomi).",
                        inline=False)

        embed.add_field(name=f"<:customemoji:1272602670418366615> Italiano:",
                        value=f"{created_since_emodji} Seleziona la lingua dal menu a tendina qui sotto (Italiano).",
                        inline=False)

        embed.add_field(name=f"<:customemoji:1272602629478027315> Français:",
                        value=f"{created_since_emodji} Sélectionnez la langue dans le menu déroulant ci-dessous (Français).",
                        inline=False)

        embed.add_field(name=f"<:customemoji:1272602660423598203> Español:",
                        value=f"{created_since_emodji} Seleccione el idioma en el menú desplegable a continuación (Español).",
                        inline=False)

        embed.set_footer(
            text=f"Нажмите на меню ниже, чтобы выбрать язык / Click the menu below to select your language.")

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    else:
        await interaction.response.send_message(language["Errors"]["Standart"]["Not_enough_rights"], ephemeral=True)


@client_discord.slash_command(name='links', description='Displaying a list of links to institutions')
async def links(interaction: Interaction):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    logger.info(language["Logging"]["Links"]["Interaction"].format(name=interaction.user.name))
    embed = nextcord.Embed(title=f'{created_since_emodji} {language["Links"]["Title"]}', color=0x8b00ff)
    embed.add_field(name=f'{created_since_emodji} {language["Links"]["Links"]["Title"]}',
                    value=f'{link_emodji} {language["Links"]["Links"]["Site"]} {link["main"]}\n'
                          f'{link_emodji} {language["Links"]["Links"]["Schedule_Page"]} {link["shedules"]}\n'
                          f'{link_emodji} {language["Links"]["Links"]["Auth_page"]} {link["login"]}')
    if interaction.guild.icon:
        embed.set_footer(
            text=f'• {interaction.guild.name} Links | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
            icon_url=interaction.guild.icon.url)
    else:
        embed.set_footer(
            text=f'• {interaction.guild.name} Links | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='author-links', description='Displaying the list of links of the bot author')
async def author_links(interaction: Interaction):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    logger.info(language["Logging"]["links"]["Interaction"].format(name=interaction.user.name))
    embed = nextcord.Embed(title=f'{created_since_emodji} {language["Links"]["Title"]}', color=0xffffff)
    embed.add_field(name=f'{created_since_emodji} {language["Links"]["Author"]["Title"]}',
                    value=f'{link_emodji} {language["Links"]["Author"]["Creator_Page"]} {author_link["main"]}\n'
                          f'{link_emodji} {language["Links"]["Author"]["Bot_Repository"]} {author_link["bot-repositori"]}\n'
                          f'{link_emodji} {language["Links"]["Author"]["Other_repositories"]} {author_link["other-repositories"]}')
    if interaction.guild.icon:
        embed.set_footer(
            text=f'• {interaction.guild.name} Links | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
            icon_url=interaction.guild.icon.url)
    else:
        embed.set_footer(
            text=f'• {interaction.guild.name} Links | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='invites', description='Displaying a list of links for invitations')
async def invite(interaction: Interaction):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    logger.info(language["Logging"]["Invites"]["Interaction"].format(name=interaction.user.name))
    invites = await interaction.guild.invites()
    embed = nextcord.Embed(title=f'{created_since_emodji} {language["Invites"]["Title"]}', color=0xffffff)
    if not invites:
        embed.add_field(name=f'',
                        value=f'{link_emodji} {language["Invites"]["No_invites"]}')
    else:
        for invite in invites:
            embed.add_field(name=f'{created_since_emodji} {language["Invites"]["Inviter"]} {invite.inviter}',
                            value=f'{link_emodji} {language["Invites"]["Link"]} {invite.url}\n'
                                  f'{members_emodji} {language["Invites"]["Use_count"].format(uses=invite.uses)}\n'
                                  f'{warn_emodji} {language["Invites"]["Created_at"]} {invite.created_at.strftime("%m-%d %H:%M")}\n'
                                  f'{warn_emodji} {language["Invites"]["Expires_at"]} {invite.expires_at.strftime("%m-%d %H:%M")}')
    if interaction.guild.icon:
        embed.set_footer(
            text=f'• {interaction.guild.name} Invites | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
            icon_url=interaction.guild.icon.url)
    else:
        embed.set_footer(
            text=f'• {interaction.guild.name} Invites | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='bot-info', description='Displaying information about the bot')
async def info(interaction: Interaction):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    logger.info(language["Logging"]["Bot-info"]["Interaction"].format(name=interaction.user.name))
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
        if interaction.guild.icon:
            embed.set_footer(text=f'• {interaction.guild.name} Info | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                             icon_url=interaction.guild.icon.url)
        else:
            embed.set_footer(
                text=f'• {interaction.guild.name} Info | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        logger.info(language["Errors"]["User"]["Not_enough_rights"].format(user=interaction.user.name))
        await interaction.response.send_message(language["Errors"]["Standart"]["Not_enough_rights"], ephemeral=True)


@client_discord.slash_command(name='channel-info', description='Output information about the specified channel')
async def channel_info(interaction: Interaction,
                       channel: nextcord.abc.GuildChannel = SlashOption(
                           description='Displays information about the selected channel',
                           channel_types=[ChannelType.text, ChannelType.voice, ChannelType.category, ChannelType.forum, ChannelType.stage_voice]
                       )):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    logger = guild_logger(interaction.guild)
    logger.info(language["Logging"]["Channel-info"]["Interaction"].format(name=interaction.user.name, channel=channel))
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        embed = nextcord.Embed(title=f'{created_since_emodji} {language["Channel"]["Channel"]} {channel.name}', color=0xffffff)
        embed.add_field(name=f'{language["Channel"]["Channel_id"]}', value=channel.id, inline=True)
        embed.add_field(name=f'{language["Channel"]["Channel_name"]}', value=channel.name, inline=True)
        embed.add_field(name=f'{language["Channel"]["Channel_type"]}', value=channel.type, inline=True)
        if isinstance(channel, nextcord.TextChannel):
            embed.add_field(name=f'{language["Channel"]["Text_channel"]["Topic"]}', value=channel.topic or 'No topic found', inline=True)
            embed.add_field(name=f'{language["Channel"]["Text_channel"]["NSFW"]}', value=channel.is_nsfw(), inline=True)
        if isinstance(channel, nextcord.VoiceChannel):
            embed.add_field(name=f'{language["Channel"]["Voice_channel"]["Bitrate"]}', value=channel.bitrate, inline=True)
            embed.add_field(name=f'{language["Channel"]["Voice_channel"]["User_limit"]}', value=channel.user_limit, inline=True)
            embed.add_field(name=f'{language["Channel"]["Voice_channel"]["Quality"]}', value=channel.video_quality_mode, inline=True)
        if isinstance(channel, nextcord.ForumChannel):
            embed.add_field(name=f'{language["Channel"]["Forum_channel"]["Tags"]}', value='\n'.join([f'{tags.name} ({tags.id})' for tags in channel.available_tags]), inline=True)
            embed.add_field(name=f'{language["Channel"]["Forum_channel"]["NSFW"]}', value=channel.is_nsfw(), inline=True)
        if isinstance(channel, nextcord.CategoryChannel):
            embed.add_field(name=f'{language["Channel"]["Category_channel"]["Channels"]}', value='\n'.join([f'{channels.name} ({channels.type})' for channels in channel.channels]), inline=True)
            embed.add_field(name=f'{language["Channel"]["Category_channel"]["Position"]}', value=channel.position, inline=True)
        if isinstance(channel, nextcord.StageChannel):
            embed.add_field(name=f'{language["Channel"]["Stage_channel"]["User_limit"]}', value=channel.user_limit, inline=True)
            embed.add_field(name=f'{language["Channel"]["Stage_channel"]["Bitrate"]}', value=channel.bitrate, inline=True)
        embed.add_field(name=f'{language["Channel"]["Created_at"]}', value=channel.created_at.strftime("%m-%d %H:%M"), inline=True)
        if interaction.guild.icon:
            embed.set_footer(text=f'• {interaction.guild.name} Info | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                             icon_url=interaction.guild.icon.url)
        else:
            embed.set_footer(
                text=f'• {interaction.guild.name} Info | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        logger.info(language["Errors"]["User"]["Not_enough_rights"].format(user=interaction.user.name))
        await interaction.response.send_message(language["Errors"]["Standart"]["Not_enough_rights"], ephemeral=True)


# @client_discord.slash_command(name='giveaway')
# async def giveaway(interaction: Interaction,
#                    action: str = SlashOption(
#                        description='Выберите что хотите сделать',
#                        choices=['create', 'delete', 'list']
#                    ),
#                    name: str = SlashOption(
#                        description='Введите название розыгрыша',
#                        default=None
#                    ),
#                    text: str = SlashOption(
#                        description='Введите текст для правил участния',
#                        default=None
#                    ),
#                    prize: str = SlashOption(
#                        description='Введите название приза',
#                        default=None
#                    ),
#                    expires_at: int = SlashOption(
#                        description='Введите через сколько дней розыгрыш будет окончен',
#                        default=None
#                    )):
#     if nextcord.utils.get(interaction.user.roles, name='Администратор'):
#         if action == 'create':
#             if not any(param is None for param in [name, text, prize, expires_at]):
#                 time_delta = datetime.timedelta(days=expires_at)
#                 new_giveaway = {
#                     'name': name,
#                     'text': text,
#                     'prize': prize,
#                     'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#                     'expires_at': (datetime.datetime.now() + time_delta).strftime('%Y-%m-%d %H:%M:%S')
#                 }
#                 json_file = 'jsons/giveaway.json'
#                 data = read_json(json_file)
#                 if not isinstance(data, list):
#                     data = []
#                 data.append(new_giveaway)
#                 giveaway_add(json_file, data)
#
#                 embed = nextcord.Embed(title='Розыгрыш', color=0xffffff)
#                 embed.add_field(name='Название:', value=name)
#                 embed.add_field(name='Условия:', value=text + '\nВсем удачи!')
#                 embed.add_field(name='Приз:', value=prize)
#                 embed.add_field(name='Окончание:',
#                                 value=f'<t:{int((datetime.datetime.now() + time_delta).timestamp())}:F>')
#
#                 message = await interaction.channel.send(embed=embed)
#
#                 await message.add_reaction('🎉')
#
#                 giveaway_data = {
#                     'message_id': message.id,
#                     'channel_id': interaction.channel.id,
#                     'name': name
#                 }
#                 giveaways = read_json('jsons/giveaways.json')
#                 giveaways.append(giveaway_data)
#                 giveaway_add('jsons/giveaways.json', giveaways)
#             else:
#                 await interaction.response.send_message(f'Заполните все данные для создания розыгрыша!', ephemeral=True)
#
#         elif action == 'delete':
#             json_file = 'jsons\\giveaway.json'
#             data = read_json(json_file)
#             data = [item for item in data if item.get('name') != name]
#             giveaway_add(json_file, data)
#             await interaction.response.send_message(f'Розыгрыш {name} удалён', ephemeral=True)
#         elif action == 'list':
#             json_file = 'jsons\\giveaway.json'
#             json_data = read_json(json_file)
#             embed = nextcord.Embed(title='Список доступных розыгрышей:', color=0xffffff)
#             count = 0
#             for data in json_data:
#                 count += 1
#                 embed.add_field(name=f'Номер:',
#                                 value=count)
#                 embed.add_field(name='Название:',
#                                 value=data.get('name', 'Not found'))
#                 embed.add_field(name='Условия (текст)',
#                                 value=data.get('text', 'Not found'))
#                 embed.add_field(name='Награда:',
#                                 value=data.get('prize', 'Not found'))
#                 embed.add_field(name='Создано:',
#                                 value=data.get('created_at', 'Not found'))
#                 embed.add_field(name='Окончится:',
#                                 value=data.get('expires_at', 'Not found'))
#             await interaction.response.send_message(embed=embed, ephemeral=True)
#
#     else:
#         await interaction.response.send_message(f'У вас не достаточно прав для использования этой команды', ephemeral=True)


@client_discord.slash_command(name='crypto-difference', description='Displays information about the cryptocurrency')
async def crypto_difference(interaction: Interaction,
                 crypto_currency: str = SlashOption(
                     name='crypto',
                     description='Choose the name of the cryptocurrency in the format: USDT, BTC, или ETH',
                     choices=['BTC', 'ETH', 'DOGE', 'USDT', 'BUSD', 'SHIB', 'ELON', 'AKITA']
                 ),
                 convert_currency: str = SlashOption(
                     name='convert',
                     description='Enter the currency you want to convert the cryptocurrency into. Format: UST, BTC, RUB',
                     choices=['BTC', 'ETH', 'DOGE', 'USDT', 'RUB', 'USD', 'BUSD', 'SHIB', 'ELON', 'AKITA']
                 )):
    global crypto_currency_emoji, convert_currency_emoji
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
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
    embed = nextcord.Embed(title=f'{created_since_emodji} {language["Crypto"]["Difference"]["Title"]}', color=0xffffff)
    embed.add_field(name=f'{slash_emodji} {language["Crypto"]["Difference"]["Description"]["Title"].format(crypto_currency=crypto_currency, convert_currency=convert_currency)}',
                    value=f'{crypto_currency_emoji} {language["Crypto"]["Difference"]["Description"]["Header"].format(crypto_currency=crypto_currency)}\n'
                          f'🔃 {language["Crypto"]["Difference"]["Description"]["Difference"].format(price_difference=price_difference)}\n'
                          f'{convert_currency_emoji} {language["Crypto"]["Difference"]["Description"]["Convert"].format(convert_currency=convert_currency)}\n'
                          f'🔄 {language["Crypto"]["Difference"]["Description"]["Lower"].format(change_24h=change_24h)}')
    embed.set_footer(
        text=f'• {interaction.guild.name} Crypto | https://coinmarketcap.com/ | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
        icon_url='https://logos-world.net/wp-content/uploads/2023/02/CoinMarketCap-Logo.png')
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='crypto-trending',
                              description='Displays a list of the most recently added tokens on coinmarketcap')
async def crypto_trending(interaction: Interaction,
                          limit: int = SlashOption(
                            description='Select the number of tokens in the list, the maximum number is 10',
                            choices=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
                            default=5
                          )):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
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
        await interaction.response.send_message(f'{language["Errors"]["Crypto"]["Response_data_error"]}: {data}', ephemeral=True)
        return

    embed = nextcord.Embed(title=f'{language["Crypto"]["Trending"]["Title"].format(limit=limit)}', color=0xffffff)
    for crypto in data['data']:
        tags = crypto.get("tags", [])
        tags_str = ', '.join(tags)
        embed.add_field(name=f'{created_since_emodji} {language["Crypto"]["Trending"]["Description"]["Name"]} {crypto["name"]}',
                        value=f'{created_since_emodji} {language["Crypto"]["Trending"]["Description"]["Id"]} {crypto["id"]}\n'
                              f'{created_since_emodji} {language["Crypto"]["Trending"]["Description"]["Symbol"]} {crypto["symbol"]}\n'
                              f'{created_since_emodji} {language["Crypto"]["Trending"]["Description"]["Tags"]} {tags_str if tags else "Нет тегов"}\n'
                              f'{created_since_emodji} {language["Crypto"]["Trending"]["Description"]["Date_added"]} {crypto.get("date_added", "N/A").split("T")[0]}')
        embed.set_footer(
            text=f'• {interaction.guild.name} Crypto | https://coinmarketcap.com/ | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
            icon_url='https://logos-world.net/wp-content/uploads/2023/02/CoinMarketCap-Logo.png')
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='crypto-info', description='Output information about the selected cryptocurrency')
async def crypto_info(interaction: Interaction,
                      crypto: str = SlashOption(
                          description='Select the cryptocurrency you want to get information about',
                          choices=['BTC', 'ETH', 'DOGE', 'USDT', 'BUSD', 'SHIB', 'ELON', 'AKITA', 'SOL', 'BNB', 'USDC', 'XRP', 'TON', 'LTC']
                      )):
    global crypto_emoji
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    if crypto is None:
        await interaction.response.send_message(f'{language["Crypto"]["Errors"]["Crypto"]["Not_picked"]}', ephemeral=True)
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
    embed = nextcord.Embed(title=f'{created_since_emodji} {language["Crypto"]["Info"]["Title"]}', color=0xffffff)
    embed.add_field(name=f'{crypto_emoji} {crypto_data["name"]}',
                    value=f'{crypto_emoji} {language["Crypto"]["Info"]["Symbol"]} {crypto_data["symbol"]}\n'
                          f'{crypto_emoji} {language["Crypto"]["Info"]["Id"]} {crypto_data["id"]}\n'
                          f'{Right_emodji} {language["Crypto"]["Info"]["Price"]} ${crypto_data["quote"]["USD"]["price"]:.2f}\n'
                          f'{Right_emodji} {language["Crypto"]["Info"]["Market_cap"]} ${crypto_data["quote"]["USD"]["market_cap"]:.2f}\n'
                          f'{Right_emodji} {language["Crypto"]["Info"]["Volume_24h"]} ${crypto_data["quote"]["USD"]["volume_24h"]:.2f}\n'
                          f'{Right_emodji} {language["Crypto"]["Info"]["Change_24h"]} {crypto_data["quote"]["USD"]["percent_change_24h"]:.2f}%\n'
                          f'{Right_emodji} {language["Crypto"]["Info"]["Circulating_Supply"]} {crypto_data["circulating_supply"]}\n'
                          f'{Right_emodji} {language["Crypto"]["Info"]["Cryptocurrency_page"]} https://coinmarketcap.com/currencies/{crypto_data["name"]}/')
    embed.set_footer(
        text=f'• {interaction.guild.name} Crypto | https://coinmarketcap.com/ | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
        icon_url='https://logos-world.net/wp-content/uploads/2023/02/CoinMarketCap-Logo.png')
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='crypto-list', description='Displays a list of all available cryptocurrencies')
async def crypto_list(interaction: Interaction,
                      all: bool = SlashOption(
                          description='Should all cryptocurrencies be withdrawn?',
                          choices=['True', 'False'],
                          default=False
                      )):
    global cryptocurrencies
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    if all is False:
        embed = nextcord.Embed(title=f'{created_since_emodji} {language["Crypto"]["Other"]["Title"]}',
                               description=f'{created_since_emodji} {language["Crypto"]["Other"]["Header"]}', color=0xffffff)
        embed.add_field(name=f'{text_emodji} {language["Crypto"]["Other"]["List_title"]}',
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
            text=f'• {interaction.guild.name} Crypto | https://coinmarketcap.com/ | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
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
            interaction.response.send_message(f'{language["Errors"]["Standart"]["Request_error"]} {response.status_code}')
        embed = nextcord.Embed(title=f'{created_since_emodji} {language["Crypto"]["Other"]["Title"]}',
                               description=f'\n'.join(cryptocurrencies[:50]),
                               color=0xffffff)
        embed.set_footer(
            text=f'• {interaction.guild.name} Crypto | https://coinmarketcap.com/ | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
            icon_url='https://logos-world.net/wp-content/uploads/2023/02/CoinMarketCap-Logo.png')
        await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='crypto', description='Displays a list of commands for cryptocurrency')
async def crypto(interaction: Interaction):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    embed = nextcord.Embed(title=f'{language["Crypto"]["Help"]["Title"]}', color=0xffffff)
    embed.add_field(name=f'{language["Crypto"]["Help"]["Crypto_info"]["Title"]}',
                    value=f'{created_since_emodji} {language["Crypto"]["Help"]["Crypto_info"]["Description"]["Usage"]}\n'
                          f'{created_since_emodji} {language["Crypto"]["Help"]["Crypto_info"]["Description"]["Header"]}\n'
                          f'{created_since_emodji} {language["Crypto"]["Help"]["Crypto_info"]["Description"]["Lower"]}\n',
                    inline=False)
    embed.add_field(name=f'{language["Crypto"]["Help"]["Crypto_exchange"]["Title"]}',
                    value=f'{created_since_emodji} {language["Crypto"]["Help"]["Crypto_exchange"]["Description"]["Usage"]}\n'
                          f'{created_since_emodji} {language["Crypto"]["Help"]["Crypto_exchange"]["Description"]["Header"]}\n'
                          f'{created_since_emodji} {language["Crypto"]["Help"]["Crypto_exchange"]["Description"]["Lower"]}\n',
                    inline=False)
    embed.add_field(name=f'{language["Crypto"]["Help"]["Crypto_list"]["Title"]}',
                    value=f'{created_since_emodji} {language["Crypto"]["Help"]["Crypto_list"]["Description"]["Usage"]}\n'
                          f'{created_since_emodji} {language["Crypto"]["Help"]["Crypto_list"]["Description"]["Header"]}\n'
                          f'{created_since_emodji} {language["Crypto"]["Help"]["Crypto_list"]["Description"]["Lower"]}\n',
                    inline=False)
    embed.add_field(name=f'{language["Crypto"]["Help"]["Crypto_difference"]["Title"]}',
                    value=f'{created_since_emodji} {language["Crypto"]["Help"]["Crypto_difference"]["Description"]["Usage"]}\n'
                          f'{created_since_emodji} {language["Crypto"]["Help"]["Crypto_difference"]["Description"]["Header"]}\n'
                          f'{created_since_emodji} {language["Crypto"]["Help"]["Crypto_difference"]["Description"]["Lower"]}\n',
                    inline=False)
    embed.add_field(name=f'{language["Crypto"]["Help"]["Crypto_image"]["Title"]}',
                    value=f'{created_since_emodji} {language["Crypto"]["Help"]["Crypto_image"]["Description"]["Usage"]}\n'
                          f'{created_since_emodji} {language["Crypto"]["Help"]["Crypto_image"]["Description"]["Header"]}\n'
                          f'{created_since_emodji} {language["Crypto"]["Help"]["Crypto_image"]["Description"]["Lower"]}\n')
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        embed.add_field(name=f'{language["Crypto"]["Help"]["Crypto_admin"]["Title"]}',
                        value=f'{created_since_emodji} {language["Crypto"]["Help"]["Crypto_admin"]["Description"]["Usage"]}\n'
                              f'{created_since_emodji} {language["Crypto"]["Help"]["Crypto_admin"]["Description"]["Header"]}\n',
                        inline=False)
    embed.set_footer(
        text=f'• {interaction.guild.name} Crypto | https://coinmarketcap.com/ | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
        icon_url='https://logos-world.net/wp-content/uploads/2023/02/CoinMarketCap-Logo.png')
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='crypto-admin', description='Displays information about the current API key')
async def crypto_admin(interaction: Interaction):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
    if nextcord.utils.get(interaction.user.roles, name='Администратор'):
        url = 'https://pro-api.coinmarketcap.com/v1/key/info'
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': API_Crypto
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        crypto_status = data['status']
        crypto_data = data['data']
        embed = nextcord.Embed(title=f'{language["Crypto"]["Admin"]["Title"]}: {API_Crypto}', color=0xffffff)
        embed.add_field(name=f'{created_since_emodji} {language["Crypto"]["Admin"]["Information"]["Title"]}:',
                        value=f'{created_since_emodji} {language["Crypto"]["Admin"]["Information"]["Request_Time"]} <t:{int(datetime.datetime.fromisoformat(crypto_status["timestamp"].replace("Z", "")).timestamp())}:R> (UTC+4)\n'
                              f'{created_since_emodji} {language["Crypto"]["Admin"]["Information"]["Response_Duration"]} {crypto_status["elapsed"]} сек.\n'
                              f'{created_since_emodji} {language["Crypto"]["Admin"]["Information"]["Token_Limit_Monthly"]} {crypto_data["plan"]["credit_limit_monthly"]}\n'
                              f'{created_since_emodji} {language["Crypto"]["Admin"]["Information"]["Token_Reset_In"]} {crypto_data["plan"]["credit_limit_monthly_reset"]}\n'
                              f'{created_since_emodji} {language["Crypto"]["Admin"]["Information"]["Token_Reset_At"]} <t:{int(datetime.datetime.fromisoformat(crypto_data["plan"]["credit_limit_monthly_reset_timestamp"].replace("Z", "")).timestamp())}:R>\n'
                              f'{created_since_emodji} {language["Crypto"]["Admin"]["Information"]["Request_Limit_Minute"]} {crypto_data["plan"]["rate_limit_minute"]}\n'
                              f'{created_since_emodji} {language["Crypto"]["Admin"]["Information"]["Tokens_Left_Month"]} {crypto_data["usage"]["current_month"]["credits_left"]}\n'
                              f'{created_since_emodji} {language["Crypto"]["Admin"]["Information"]["Tokens_Used_Today"]} {crypto_data["usage"]["current_day"]["credits_used"]}\n'
                              f'{created_since_emodji} {language["Crypto"]["Admin"]["Information"]["Tokens_Used_Month"]} {crypto_data["usage"]["current_month"]["credits_used"]}')
        embed.set_footer(
            text=f'• {interaction.guild.name} Crypto | https://coinmarketcap.com/ | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
            icon_url='https://logos-world.net/wp-content/uploads/2023/02/CoinMarketCap-Logo.png')
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(f'{language["Errors"]["Standart"]["Not_enough_rights"]}', ephemeral=True)


@client_discord.slash_command(name='crypto-exchange',
                              description='Displays information about the selected crypto exchange')
async def crypto_exchange(interaction: Interaction,
                          name: str = SlashOption(
                              description='Enter exchange name. Example: binance. You cannot use capital letters.'
                          )):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
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
        await interaction.response.send_message(f'{language["Errors"]["Crypto"]["Invalid_Exchange_name"]} {name}', ephemeral=True)
        return
    embed = nextcord.Embed(title=f'{created_since_emodji} {language["Crypto"]["Exchange"]["Title"]}: {exchange_data["name"]}', color=0xffffff)
    embed.set_thumbnail(url=exchange_data['logo'])
    embed.add_field(name=f'{created_since_emodji} {language["Crypto"]["Exchange"]["Value_title"]}',
                    value=f'{created_since_emodji} {language["Crypto"]["Exchange"]["Name"]} {exchange_data["name"]}\n'
                          f'{created_since_emodji} {language["Crypto"]["Exchange"]["Id"]} {exchange_data["id"]}\n'
                          f'{created_since_emodji} {language["Crypto"]["Exchange"]["Lowercase"]} {exchange_data["slug"]}\n'
                          f'{created_since_emodji} {language["Crypto"]["Exchange"]["Currencies"]} {", ".join(exchange_data["fiats"])}\n'
                          f'{created_since_emodji} {language["Crypto"]["Exchange"]["Launch_date"]} <t:{int(datetime.datetime.fromisoformat(exchange_data["date_launched"].replace("Z", "")).timestamp())}:R>\n'
                          f'{created_since_emodji} {language["Crypto"]["Exchange"]["Weekly_visits"]} {exchange_data["weekly_visits"]:,.0f}\n'
                          f'{created_since_emodji} {language["Crypto"]["Exchange"]["Daily_volume"]} {exchange_data["spot_volume_usd"]:,.1f}\n'
                          f'{created_since_emodji} {language["Crypto"]["Exchange"]["Last_update"]} <t:{int(datetime.datetime.fromisoformat(exchange_data["spot_volume_last_updated"].replace("Z", "")).timestamp())}:R>')
    embed.add_field(name='Ссылки',
                    value=f'{link_emodji} {language["Crypto"]["Links"]["Title"]} [Тык]({"".join(exchange_data["urls"]["chat"])})\n'
                          f'{link_emodji} {language["Crypto"]["Links"]["Chat"]} [Тык]({"".join(exchange_data["urls"]["website"])})\n'
                          f'{link_emodji} {language["Crypto"]["Links"]["Website"]} (X): [Тык]({"".join(exchange_data["urls"]["twitter"])})\n'
                          f'{link_emodji} {language["Crypto"]["Links"]["Twitter"]} [Тык]({"".join(exchange_data["urls"]["fee"])})\n'
                          f'{link_emodji} {language["Crypto"]["Links"]["Fee_policy"]} [Тык]({"".join(exchange_data["urls"]["fee"])})')
    embed.set_footer(
        text=f'• {interaction.guild.name} Crypto | https://coinmarketcap.com/ | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
        icon_url='https://logos-world.net/wp-content/uploads/2023/02/CoinMarketCap-Logo.png')
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client_discord.slash_command(name='crypto-image', description='Displays a picture of the cryptocurrency')
async def crypto_image(interaction: Interaction,
                       id: str = SlashOption(
                           description='Enter cryptocurrency if. You can get it on /crypto-info'
                       )):
    language_code = language_data(interaction.guild)
    language = setup_language(language_code)
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
        await interaction.response.send_message(image, ephemeral=True)
    else:
        await interaction.response.send_message(f'{language["Errors"]["Standart"]["Error_message"]}. Code: {response.status_code}', ephemeral=True)
try:
    client_discord.run(TOKEN)
except Exception as e:
    print(f'Error {e}')
    client_discord.run(TOKEN)
