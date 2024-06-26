import discord
import requests
import datetime
import os
from discord.ext import commands
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
client_discord = discord.Client(intents=intents)

# Список запрещённых слов в чате
Forbidden_words = ['даун', 'пидор', 'шлюха', 'гей', 'еблан', 'пидорас', 'хуйня', 'хуйни', 'шлюхи', 'пидрила', 'пидорасина', 'блять', 'блядь', 'блядина', 'ебланище', 'сука', 'негр', 'уёбище', 'шмара', 'хуесос', 'пиздализ', 'пизда', 'жопа', 'член', 'ссанина', ]

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
@client_discord.event
async def on_ready():
    print(f'{client_discord.user} запущен')
    print(' ')
    print(f'Блокировка: .ban @Нарушитель причина \nРазблокировка: .unban @Нарушитель причина \nУдаление: .kick @Нарушитель причина \nОтчистка: .clear количество(можно цифрой либо all для удаления всего \nСписок всех учатников: .members \nВывод информации о сервере: .serverinfo(писать только в канал статистика) \nЗаглушение участника: .mute @Нарушитель причина"f" \nРазглушение участника: .unmute @Нарушитель причина \nИнформация о участнике: .member @Участник \nАватар участника: .avatar @Участник \nИнформация о погоде: .weather Город(любой)')

@client_discord.event
async def on_message(message):
    if message.author == client_discord.user:
        return

    for word in Forbidden_words:
        if word in message.content:
            if any(role.name == "Администратор" for role in message.author.roles):
                return
            else:
                async for msg in message.channel.history(limit=1):
                    await msg.delete()
                await message.channel.send(f'{message.author.mention}. В вашем сообщении обнаружено запрещённое слово. Просьба больше не нарушать.')
                return

    # Обработка команд
    if message.content.startswith('.ban'):
        await handle_ban(message)

    if message.content.startswith('.serverinfo'):
        await handle_serverinfo(message)

    if message.content.startswith('.clear'):
        await handle_clear(message)

    if message.content.startswith('.kick'):
        await handle_kick(message)

    if message.content.startswith('.members'):
        await handle_members(message)

    if message.content.startswith('.info'):
        await handle_memberinfo(message)

    if message.content.startswith('.commands'):
        await handle_commands(message)

    # if message.content.split('.help'):
    #     await handle_help(message)

    if message.content.startswith('.mute'):
        await handle_mute(message)

    if message.content.startswith('.unmute'):
        await handle_unmute(message)

    if message.content.startswith('.unban'):
        await handle_unban(message)

    if message.content.startswith('.avatar'):
        await handle_avatar(message)

    if message.content.startswith('.weather'):
        await handle_weather(message)



# Функция для обработки команды .ban
async def handle_ban(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    if discord.utils.get(message.author.roles, name="Администратор") is not None:
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
    else:
        await message.channel.send(f'{message.author.mention}. У вас недостаточно прав для использования этой команды!')
#функция для обработки команды .kick

async def handle_kick(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    if discord.utils.get(message.author.roles, name="Администратор") is not None:
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
    else:
        await message.channel.send(f'{message.author.mention}. У вас недостаточно прав для использования этой команды!')
# Функция для обработки команды .serverinfo

async def handle_serverinfo(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    if discord.utils.get(message.author.roles, name="Администратор") is not None:
        guild = discord.utils.get(client_discord.guilds, id=1171462603260821585)
        bots = sum(1 for member in guild.members if member.bot)
        count_messages = 0
        for channel in guild.text_channels:
            messages = []
            async for message in channel.history(limit=None):
                messages.append(message)
            count_messages += len(messages)
        admin_role = discord.utils.get(guild.roles, name="Администратор")
        admin_count = len([member for member in guild.members if admin_role in member.roles])
        verify_role = discord.utils.get(guild.roles, name="Верифицирован✅️")
        verify_count = len([member for member in guild.members if verify_role in member.roles])
        server_creation_date_full = f'{guild.created_at}'
        server_creation_date = server_creation_date_full[:19]
        time = datetime.datetime.now().replace(microsecond=0)

        embed = discord.Embed(title="Информация о сервере", color=0xffffff)
        embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="Дата создания: ", value=server_creation_date, inline=False)
        embed.add_field(name="Создан: ", value=guild.owner.mention, inline=False)
        embed.add_field(name="Участники", value=f"Всего участников: {len(message.guild.members)} \nБотов: {str(bots)} \nАдминистраторов: {admin_count} \nВерифицировались: {verify_count}", inline=False)
        embed.add_field(name="Каналы", value=f"Текстовых каналов: {len(message.guild.text_channels)}\nГолосовых каналов: {len(message.guild.voice_channels)}\nКатегорий: {len(message.guild.categories)} \nТекстовых сообщений: {count_messages} ", inline=False)
        embed.add_field(name="Ссылки", value=f"📲Telegram-канал: https://t.me/UnicUm_Colabarations \n👾Discord-сервер: https://discord.gg/hW39qmju \n \nВызвано: {time}")

        channel_stat = discord.utils.get(message.guild.channels, name="статистика")
        if channel_stat:
            async for msg in channel_stat.history(limit=1):
                await msg.delete()
            await channel_stat.send(embed=embed)
        else:
            embed = discord.Embed(title=f"Ошибка", color=0xff0000)
            embed.add_field(name=" ", value="Канал 'статистика' не найден")
            await message.channel.send(embed=embed)
    else:
        await message.channel.send(f'{message.author.mention}. У вас недостаточно прав для использования этой команды!')
# Функция для обработки команды .clear
async def handle_clear(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    if discord.utils.get(message.author.roles, name="Администратор") is not None:
        parts = message.content.split(' ')
        if len(parts) > 1:
            if parts[1] == "all":
                try:
                    await message.channel.purge(limit=None)
                except discord.errors.Forbidden:
                    await message.channel.send('У меня нет прав для очистки сообщений.')
            else:
                try:
                    count = int(parts[1])
                    await message.channel.purge(limit=count)
                except ValueError:
                    await message.channel.send('Неверный формат. Используйте ".clear all" для очистки всех сообщений или ".clear [число] для очистки заданного количества сообщений.')
                except discord.errors.Forbidden:
                    await message.channel.send('У меня нет прав для очистки сообщений.')
        else:
            embed = discord.Embed(title=f"Ошибка", color=0xff0000)
            embed.add_field(name=" ", value='Не указано количество сообщений для очистки. Используйте ".clear all" для очистки всех сообщений или ".clear [число] для очистки заданного количества сообщений.')
            await message.channel.send(embed=embed)
    else:
        await message.channel.send(f'{message.author.mention}. У вас недостаточно прав для использования этой команды!')
async def handle_members(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    if discord.utils.get(message.author.roles, name="Администратор") is not None:
        members_info = [f"{member.mention}-{member.name} (ID: {member.id}) (Высшая роль: {member.top_role})" for member in message.guild.members]
        embed = discord.Embed(title='Участники сервера', description='\n'.join(members_info), color=0xffffff)
        await message.channel.send(embed=embed)
    else:
        await message.channel.send(f'{message.author.mention}. У вас недостаточно прав для использования этой команды!')

async def handle_commands(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    if discord.utils.get(message.author.roles, name="Администратор") is not None:
        embed = discord.Embed(title="Доступные команды сервера", color=0xffffff)
        embed.add_field(
        name="Ранг: Модерация", value=f"Блокировка: .ban @Нарушитель причина \nРазблокировка: .unban @Нарушитель причина \nУдаление: .kick @Нарушитель причина \nОтчистка: .clear количество(можно цифрой либо all для удаления всего) \nСписок всех учатников: .members \nВывод информации о сервере: .serverinfo(писать только в канал статистика) \nЗаглушение участника: .mute @Нарушитель причина"f" \nРазглушение участника: .unmute @Нарушитель причина \nИнформация о участнике: .info @Участник \nАватар участника: .avatar @Участник \nИнформация о погоде: .weather Город(любой) \nВывод этого сообщения: .commands(в канал #bot-commands, не писать)", inline=False)
        channel_mod = discord.utils.get(message.guild.channels, name="bot-commands")
        async for msg in channel_mod.history(limit=1):
            await msg.delete()
        await channel_mod.send(embed=embed)
    else:
        await message.channel.send(f'{message.author.mention}. У вас недостаточно прав для использования этой команды!')
# async def handle_help(message):
#     async for msg in message.channel.history(limit=1):
#         await msg.delete()
#     embed = discord.Embed(title="Доступные команды сервера", color=0xffffff)
#     embed.add_field(name="Ранг: Участник", value=f"Информация о участнике: .info @Участник \nАватар участника: .avatar @Участник \n Информация о погоде: .weather Город(любой)", inline=False)
#     await message.channel.send(embed=embed)
async def handle_mute(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    if discord.utils.get(message.author.roles, name="Администратор") is not None:
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
    else:
        await message.channel.send(f'{message.author.mention}. У вас недостаточно прав для использования этой команды!')
async def handle_unmute(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    if discord.utils.get(message.author.roles, name="Администратор") is not None:
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
    else:
        await message.channel.send(f'{message.author.mention}. У вас недостаточно прав для использования этой команды!')
async def handle_unban(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    if discord.utils.get(message.author.roles, name="Администратор") is not None:
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
    else:
        await message.channel.send(f'{message.author.mention}. У вас недостаточно прав для использования этой команды!')
async def handle_memberinfo(message):
    if message.author == client_discord.user:
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
    excepted_roles = ["@everyone", "Member"]
    role_count = len([role.name for role in member.roles if role.name not in excepted_roles])
    roles = member.roles
    role_names = [role.name for role in roles if role.name not in excepted_roles]
    role_list = ' '.join(role_names)
    discriminator = member.discriminator
    if discriminator == 0:
         discriminator = None
    embed = discord.Embed(title=f"Информация о {member.name}", color=0xffffff)
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="Никнейм:", value=member.name, inline=True)
    embed.add_field(name="Профиль:", value=member.mention, inline=True)
    embed.add_field(name="Полное имя:", value=f'{member.name}#{discriminator}', inline=True)
    embed.add_field(name="ID:", value=member.id, inline=True)
    embed.add_field(name="Дата присоеденения:", value=member.joined_at.strftime("%Y-%m-%d %H-%M"), inline=True)
    embed.add_field(name="Роль:", value=member.top_role.name, inline=True)
    embed.add_field(name="Роли:", value=role_list)
    embed.add_field(name='Количество ролей:', value=role_count)

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
            "Wind_speed": weather_data['wind']['speed'],
            "Humidity": weather_data['main']['humidity'],
            "City_id": weather_data['id']
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
                            value=f"Средняя температура: {filtered_data['Temp']}°C \nМинимальная температура: {filtered_data['Temp_min']}°C \nМаксимальная температура: {filtered_data['Temp_max']}°C \nТемпература по ощущениям: {filtered_data['Feels_like']}°C \nСкорость ветра: {filtered_data['Wind_speed']}М/С \nВлажность: {filtered_data['Humidity']}% \nЗапрос выполнен: {time} \nЗапросил: {message.author.mention} \n Источник: https://openweathermap.org/city/{filtered_data['City_id']}")

        except requests.exceptions.HTTPError:
            embed = discord.Embed(title=f"Ошибка", color=0xff0000)
            embed.add_field(name=f"Ошибка получения данных", value='')

        except requests.exceptions.RequestException:
            embed = discord.Embed(title=f"Ошибка", color=0xff0000)
            embed.add_field(name=f"Ошибка получения данных", value='')
    await message.channel.send(embed=embed)
client_discord.run(TOKEN)
