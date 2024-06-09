import discord
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

@client.event
async def on_ready():
    print(f'{client.user} запущен')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Обработка команд
    if message.content.startswith('.hello'):
        await message.channel.send(f'Привет, {message.author.mention}!')

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

    if message.content.startswith('.member') and any(role.name == "Администратор" for role in message.author.roles):
        await handle_memberinfo(message)

    if message.content.startswith('.help') and any(role.name == "Администратор" for role in message.author.roles):
        await handle_help(message)

    if message.content.startswith('.mute') and any(role.name == 'Администратор' for role in message.author.roles):
        await handle_mute(message)

    if message.content.startswith('.unmute') and any(role.name == 'Администратор' for role in message.author.roles):
        await handle_unmute(message)

    if message.content.startswith('.unban') and any(role.name == 'Администратор' for role in message.author.roles):
        await handle_unban(message)

    if message.content.startswith('.avatar') and any(role.name == 'Администратор' for role in message.author.roles):
        await handle_avatar(message)
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
        await message.channel.send('Неверный формат команды. Используйте: .ban @игрок причина')

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
        await message.channel.send('Неверный формат команды. Используйте: .kick @игрок причина')

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
        print("Канал 'статистика' не найден")

# Функция для обработки команды .clear
async def handle_clear(message):
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
        await message.author.send(
            'Не указано количество сообщений для очистки. Используйте ".clear all" для очистки всех сообщений или ".clear [число] для очистки заданного количества сообщений.')
async def handle_members(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    members_info = [f"{member.mention}-{member.name} (ID: {member.id})" for member in message.guild.members]
    embed = discord.Embed(title='Участники сервера', description='\n'.join(members_info), color=0xffffff)
    await message.channel.send(embed=embed)

async def handle_help(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    embed = discord.Embed(title="Доступные команды сервера", color=0xffffff)
    embed.add_field(
    name="Модерация", value=f"Блокировка: .ban @Нарушитель причина \nРазблокировка: .unban @Нарушитель причина \nУдаление: .kick @Нарушитель причина \nОтчистка: .clear количество(можно цифрой либо all для удаления всего \nСписок всех учатников: .members \nВывод информации о сервере: .serverinfo(писать только в канал статистика) \nЗаглушение участника: .mute @Нарушитель причина"f" \nРазглушение участника: .unmute @Нарушитель причина \nИнформация о участнике: .member @Участник \nАватар участника: .avatar @Участник", inline=False
    )
    chanel_mod = discord.utils.get(message.guild.channels, name="bot-commands")
    async for msg in chanel_mod.history(limit=1):
        await msg.delete()
    await chanel_mod.send(embed=embed)
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
        await message.channel.send('Неверный формат команды. Используйте: .mute @игрок причина')
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
        await message.channel.send('Неверный формат команды. Используйте: .unmute @игрок причина')
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
            await message.channel.send(f'Пользователь с ID {user_id} не найден.')
    else:
        await message.channel.send('Неверный формат команды. Используйте: .unban <@пользователь> причина')

async def handle_memberinfo(message):
    async for msg in message.channel.history(limit=1):
        await msg.delete()
    parts = message.content.split(' ')
    if len(parts) > 1:
        # Ищем пользователя по упоминанию
        member = message.mentions[0]
    else:
        # Если пользователь не указан, используем автора сообщения
        member = message.author
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

    if len(parts) > 1:
        member = message.mentions[0]
    else:
        member = message.author

    embed = discord.Embed(title=f"Аватар {member.name}", color=0xffffff)
    embed.set_image(url=member.avatar.url)
    await message.channel.send(embed=embed)
client.run('MTI0NjY1Mzg3MjQyMDY4Mzg4Ng.G1N5gg.2vL4aj8ZWornQxSTKwNgjG9aBvQ6CNL_az9tOg')
