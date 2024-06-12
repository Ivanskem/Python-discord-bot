import discord
import requests
import datetime
import os
# from discord.ext import commands
# import asyncio
# import flet as ft

# Создайте объект Intents и установите необходимые флаги
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.bans = True
intents.moderation = True

# Создайте объект Client, передав объект Intents
client = discord.Client(intents=intents)

try:
    with open('token.txt', 'r') as f:
        TOKEN = f.read().strip()
except FileNotFoundError:
    TOKEN = input("Введите ваш токен Discord: ")
    with open('token.txt', 'w') as f:
        f.write(TOKEN)

# Читаем WEATHER_API из файла


try:
    with open('weather_api.txt', 'r') as f:
        API_Weather = f.read().split()
except FileNotFoundError:
    API_Weather = input("Введите ваш api для погоды: ")
    with open('weather_api.txt', 'w') as f:
        f.write(API_Weather)
@client.event
async def on_ready():
    print(f'{client.user} запущен')
    print(' ')
    print(f'Блокировка: .ban @Нарушитель причина \nРазблокировка: .unban @Нарушитель причина \nУдаление: .kick @Нарушитель причина \nОтчистка: .clear количество(можно цифрой либо all для удаления всего \nСписок всех учатников: .members \nВывод информации о сервере: .serverinfo(писать только в канал статистика) \nЗаглушение участника: .mute @Нарушитель причина"f" \nРазглушение участника: .unmute @Нарушитель причина \nИнформация о участнике: .member @Участник \nАватар участника: .avatar @Участник \nИнформация о погоде: .weather Город(любой)')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Обработка команд
    if message.content.startswith('.ban') and any(role.name == "Администратор" for role in message.author.roles):
        await handle_ban(message)

    if message.content.startswith('.serverinfo') and any(role.name == "Администратор" for role in message.author.roles):
        await handle_serverinfo(message)

    if message.content.startswith('.clear') and any(role.name == "Администратор" for role in message.author.roles):
        await handle_clear(message)

    if message.content.startswith('.kick') and any(role.name == "Администратор"for role in message.author.roles):
        await handle_kick(message)

    if message.content.startswith('.members') and any(role.name == "Администратор" for role in message.author.roles):
        await handle_members(message)

    if message.content.startswith('.info'):
        await handle_memberinfo(message)

    if message.content.startswith('.commands') and any(role.name == "Администратор" for role in message.author.roles):
        await handle_commands(message)

    # if message.content.split('.bot'):
    #     await handle_bot(message)

    if message.content.startswith('.mute') and any(role.name == 'Администратор' for role in message.author.roles):
        await handle_mute(message)

    if message.content.startswith('.unmute') and any(role.name == 'Администратор' for role in message.author.roles):
        await handle_unmute(message)

    if message.content.startswith('.unban') and any(role.name == 'Администратор' for role in message.author.roles):
        await handle_unban(message)

    if message.content.startswith('.avatar'):
        await handle_avatar(message)

    if message.content.startswith('.weather'):
        await handle_weather(message)

# Функция для обработки команды .ban
async def handle_ban(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    parts = message.content.split(' ')
    if len(parts) > 2 and len(message.mentions) == 1:
        target_user = message.mentions[0]
        reason = ' '.join(parts[2:])
        try:
            await target_user.ban(reason=reason)
            embed = discord.Embed(title="Информация о блокировке", color=discord.Color.dark_purple())
            embed.add_field(name=" ", value=f"Администратор: {message.author}\nПричина: {reason}\nЗаблокированный: {target_user}", inline=False)
            await message.channel.send(embed=embed)
        except discord.errors.Forbidden:
            await message.channel.send(f'У меня нет прав для блокировки {target_user.mention}.')
    else:
        embed = discord.Embed(title=f"Ошибка", color=0xff0000)
        embed.add_field(name=" ", value='Неверный формат команды. Используйте: .ban @игрок причина')
        await message.channel.send(embed=embed)
#функция для обработки команды .kick

async def handle_kick(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    parts = message.content.split(' ')
    if len(parts) > 2 and len(message.mentions) == 1:
        target_user = message.mentions[0]
        reason = ' '.join(parts[2:])
        try:
            await message.guild.kick(target_user, reason=reason)
            embed = discord.Embed(title="Информация о кике", color=discord.Color.dark_purple())
            embed.add_field(name=" ", value=f"Администратор: {message.author}\nПричина: {reason}\nУдалённый: {target_user}", inline=False)
            await message.channel.send(embed=embed)
        except discord.errors.Forbidden:
             await message.channel.send(f'У меня нет прав для кика {target_user.mention}.')
    else:
        embed = discord.Embed(title=f"Ошибка", color=0xff0000)
        embed.add_field(name=" ", value='Неверный формат команды. Используйте: .kick @игрок причина')
        await message.channel.send(embed=embed)
# Функция для обработки команды .serverinfo

async def handle_serverinfo(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    embed = discord.Embed(title="Информация о сервере", color=discord.Color.blue())
    embed.add_field(name="Участники", value=f"Всего участников: {len(message.guild.members)}", inline=False)
    embed.add_field(name="Каналы", value=f"Текстовых каналов: {len(message.guild.text_channels)}\nГолосовых каналов: {len(message.guild.voice_channels)}\nКатегорий: {len(message.guild.categories)}", inline=False)
    channel_stat = discord.utils.get(message.guild.channels, name="статистика")
    if channel_stat:
        async for msg in channel_stat.history(limit=1):
            await msg.delete()
        await channel_stat.send(embed=embed)
    else:
        embed = discord.Embed(title=f"Ошибка", color=0xff0000)
        embed.add_field(name=" ", value="Канал 'статистика' не найден")
        await message.channel.send(embed=embed)

# Функция для обработки команды .clear
async def handle_clear(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    parts = message.content.split(' ')
    if len(parts) > 1:
        if parts[1] == "all":
            try:
                await message.channel.purge(limit=None)
                await message.author.send('Сообщения успешно очищены.')
            except discord.errors.Forbidden:
                await message.author.send('У меня нет прав для очистки сообщений.')
        else:
            try:
                count = int(parts[1])
                await message.channel.purge(limit=count + 1)
                await message.author.send(f'Удалено {count} сообщений.')
            except ValueError:
                await message.author.send('Неверный формат. Используйте ".clear all" для очистки всех сообщений или ".clear [число] для очистки заданного количества сообщений.')
            except discord.errors.Forbidden:
                await message.author.send('У меня нет прав для очистки сообщений.')
    else:
        embed = discord.Embed(title=f"Ошибка", color=0xff0000)
        embed.add_field(name=" ", value='Не указано количество сообщений для очистки. Используйте ".clear all" для очистки всех сообщений или ".clear [число] для очистки заданного количества сообщений.')
        await message.channel.send(embed=embed)
async def handle_members(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    members_info = [f"{member.mention}-{member.name} (ID: {member.id})" for member in message.guild.members]
    embed = discord.Embed(title='Участники сервера', description='\n'.join(members_info), color=0xffffff)
    await message.channel.send(embed=embed)

async def handle_commands(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    embed = discord.Embed(title="Доступные команды сервера", color=0xffffff)
    embed.add_field(
    name="Ранг: Модерация", value=f"Блокировка: .ban @Нарушитель причина \nРазблокировка: .unban @Нарушитель причина \nУдаление: .kick @Нарушитель причина \nОтчистка: .clear количество(можно цифрой либо all для удаления всего \nСписок всех учатников: .members \nВывод информации о сервере: .serverinfo(писать только в канал статистика) \nЗаглушение участника: .mute @Нарушитель причина"f" \nРазглушение участника: .unmute @Нарушитель причина \nИнформация о участнике: .info @Участник \nАватар участника: .avatar @Участник \nИнформация о погоде: .weather Город(любой) \nВывод этого сообщения: .commands(в канал #bot-commands, не писать)", inline=False)
    channel_mod = discord.utils.get(message.guild.channels, name="bot-commands")
    async for msg in channel_mod.history(limit=1):
        await msg.delete()
    await channel_mod.send(embed=embed)
# async def handle_bot(message):
#
#     embed = discord.Embed(title="Доступные команды сервера", color=0xffffff)
#     embed.add_field(name="Ранг: Участник", value=f"Информация о участнике: .member @Участник \nАватар участника: .avatar @Участник \n Информация о погоде: .weather Город(любой)", inline=False)
#     await message.channel.send(embed=embed)
async def handle_mute(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    parts = message.content.split(' ')
    if len(parts) > 2 and len(message.mentions) == 1:
        target_user = message.mentions[0]
        reason = ' '.join(parts[2:])
        try:
            mute_role = discord.utils.get(message.guild.roles, name="Muted")
            if not mute_role:
                mute_role = await message.guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False, speak=False))
                await mute_role.edit(position=1)
            await target_user.add_roles(mute_role, reason=reason)
            embed = discord.Embed(title="Информация о заглушении", color=discord.Color.dark_purple())
            embed.add_field(name=" ", value=f"Администратор: {message.author.mention}\nПричина: {reason}\nЗаглушенный: {target_user.mention}", inline=False)
            await message.channel.send(embed=embed)
        except discord.errors.Forbidden:
            await message.channel.send(f'У меня нет прав для заглушения {target_user.mention}.')
    else:
        embed = discord.Embed(title=f"Ошибка", color=0xff0000)
        embed.add_field(name=" ", value='Неверный формат команды. Используйте: .mute @игрок причина')
        await message.channel.send(embed=embed)
async def handle_unmute(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    parts = message.content.split(' ')
    if len(parts) > 2 and len(message.mentions) == 1:
        target_user = message.mentions[0]
        reason = ' '.join(parts[2:])
        try:
            mute_role = discord.utils.get(message.guild.roles, name="Muted")
            if mute_role:
                await target_user.remove_roles(mute_role, reason=reason)
                embed = discord.Embed(title="Информация о разглушении", color=discord.Color.blue())
                embed.add_field(name=" ", value=f"Администратор: {message.author.mention}\nПричина:{reason}\nРазглушённый: {target_user.mention}", inline=False)
                await message.channel.send(embed=embed)
        except:
            await message.channel.send(f"У меня нет прав для разглушения {target_user.mention}.")
    else:
        embed = discord.Embed(title=f"Ошибка", color=0xff0000)
        embed.add_field(name=" ", value='Неверный формат команды. Используйте: .unmute @игрок причина')
        await message.channel.send(embed=embed)
async def handle_unban(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    parts = message.content.split(' ')
    if len(parts) > 2:
        user_id = parts[1].replace('<@!', '').replace('>', '').replace('@', '').replace('<', '')
        reason = ' '.join(parts[2:])
        try:
            await message.guild.unban(discord.Object(id=int(user_id)), reason=reason)
            embed = discord.Embed(title="Информация о разблокировке", color=discord.Color.blue())
            embed.add_field(name=" ", value=f"Администратор: {message.author}\nПричина: {reason}\nРазблокированный: <@{user_id}>", inline=False)
            await message.channel.send(embed=embed)
        except discord.errors.Forbidden:
            await message.channel.send(f'У меня нет прав для разблокировки пользователя.')
        except discord.errors.NotFound:
            await message.channel.send(f'Введённый пользователь не заблокирован.')
    else:
        embed = discord.Embed(title=f"Ошибка", color=0xff0000)
        embed.add_field(name=" ", value='Неверный формат команды. Используйте: .unban <@пользователь> причина')
        await message.channel.send(embed=embed)

async def handle_memberinfo(message):
    if message.author == client.user:
        return
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    parts = message.content.split(' ')
    try:
        if len(parts) > 1:
            # Ищем пользователя по упоминанию
            member = message.mentions[0]
        else:
            # Если пользователь не указан, используем автора сообщения
            member = message.author
    except IndexError:
        embed = discord.Embed(title=f"Ошибка", color=0xff0000)
        embed.add_field(name=" ", value="Команда была неправильно использованна. Используйте .info @Участник")
        await message.channel.send(embed=embed)
    # if isinstance(message.author, discord.Member):
    #     member = message.author
    # else:
    #     await message.channel.send(
    #         "Извини, я не могу получить информацию о пользователе, который не является членом сервера.")
    #     return
    # role_list = [role.name for role in member.roles]
    # role_string = ", ".join(role_list)
    # discriminator = member.discriminator
    # if discriminator == 0:
    #     discriminator = None
    embed = discord.Embed(title=f"Информация о {member.name}", color=0xffffff)
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="Никнейм:", value=member.name, inline=True)
    embed.add_field(name="Профиль:", value=member.mention, inline=True)
    # embed.add_field(name="Полное имя:", value=discriminator, inline=True)
    embed.add_field(name="ID:", value=member.id, inline=True)
    embed.add_field(name="Дата присоеденения:", value=member.joined_at.strftime("%Y-%m-%d %H-%M"), inline=True)
    embed.add_field(name="Роли:", value=member.top_role.name, inline=True)
    # embed.add_field(name="Статус:", value=member.status, inline=True)

    await message.channel.send(embed=embed)
async def handle_avatar(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    parts = message.content.split()
    try:
        if len(parts) > 1:
         member = message.mentions[0]
        else:
            member = message.author
    except IndexError:
        embed = discord.Embed(title=f"Ошибка", color=0xff0000)
        embed.add_field(name=" ", value="Команда была неправильно использованна. Используйте .avatar @Участник")
        await message.channel.send(embed=embed)

    embed = discord.Embed(title=f"Аватар {member.name}", color=0xffffff)
    embed.set_image(url=member.avatar.url)
    await message.channel.send(embed=embed)
async def handle_weather(message):
    global filtered_data
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    try:
        with open('weather_api.txt', 'r') as f:
            global API_Weather
            API_Weather = f.read().strip()
    except FileNotFoundError:
        API_Weather = input("Введите ваш API ключ для метеорологического сервиса: ")
        with open('weather_api.txt', 'w') as f:
            f.write(API_Weather)

    city = message.content.split(' ')[1]
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_Weather}&units=metric'
    response = requests.get(url)
    weather_data = response.json()
    time = datetime.datetime.now().replace(microsecond=0)
    try:
        filtered_data = {
            "X": weather_data['coord']['lon'],
            "Y": weather_data['coord']['lat'],
            "Temp_min": weather_data['main']['temp_min'],
            "Temp_max": weather_data['main']['temp_max'],
            "Temp": weather_data['main']['temp'],
            "Feels_like": weather_data['main']['feels_like'],
            "Country": weather_data['sys']['country'],
            "Wind_speed": weather_data['wind']['speed']
        }
    except KeyError:
        embed = discord.Embed(title=f"Ошибка", color=0xff0000)
        embed.add_field(name=f"Произошла ошибка!", value='')
    if response.status_code == 200:
        try:
            url_png = f"https://tile.openweathermap.org/map/temp_new/0/0/0.png?appid={API_Weather}"
            embed = discord.Embed(title=f"Погода в {city}", color=0x376abd)
            embed.set_thumbnail(url=url_png)
            embed.add_field(name=f"Город: {city}, Страна: {filtered_data['Country']}",
                            value=f"Средняя температура: {filtered_data['Temp']}°C \nМинимальная температура: {filtered_data['Temp_min']}°C \nМаксимальная температура: {filtered_data['Temp_max']}°C \nТемпература по ощущениям: {filtered_data['Feels_like']}°C \nСкорость ветра: {filtered_data['Wind_speed']}М/С \nЗапрос выполнен: {time} \nЗапросил: {message.author.mention}")

        except requests.exceptions.HTTPError:
            embed = discord.Embed(title=f"Ошибка", color=0xff0000)
            embed.add_field(name=f"Ошибка получения данных", value='')

        except requests.exceptions.RequestException:
            embed = discord.Embed(title=f"Ошибка", color=0xff0000)
            embed.add_field(name=f"Ошибка получения данных", value='')
    await message.channel.send(embed=embed)

client.run(TOKEN)
