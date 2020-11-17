import discord
from discord.ext import commands, tasks
import asyncio

client = discord.Client()

bot = commands.Bot(command_prefix = "~", description = " Bot de la CdC")

#events

@bot.event
async def on_ready():
    print("Ready !")

@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(775155750557188156)
    await channel.send(f"La CDC accueille {member.mention} comme nouveau membre.")

@bot.event
async def on_member_remove(member):
    channel = member.guild.get_channel(775155750557188156)
    await channel.send(f"{member.mention} a quitté la cdc")

@bot.event
async def createMutedRole(blabla):
    mutedRole = await blabla.guild.create_role(name = "Muted", permissions = discord.Permissions(send_messages = False, speak = False), reason = "Commande faite pour muter les gens")
    for channel in blabla.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole

@bot.event
async def getMutedRole(blabla):
    roles = blabla.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role

    return await createMutedRole(blabla)

@bot.event
async def on_command_error(blabla, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await blabla.send("Il manque un argument")
    elif isinstance(error, commands.MissingPermissions):
        await blabla.send("Erreur dans la matrice, tu n'es qu'un gueux, comment daignes-tu effectuer cette commande? ")
    elif isinstance(error, commands.CheckFailure):
        await blabla.send("Tu ne peux pas utiliser cette commande dans ce channel. Va la faire sur commande-bot")
    elif isinstance(error, commands.BotMissingPermissions):
        await blabla.send("Seul les admins ont la permission de faire cette commande. Même le bot de la CDC est impuissant face à cela...")

def commande_bot_channel(blabla):
    return blabla.message.channel.id == 775155750557188156

@bot.command()
@commands.check(commande_bot_channel)
async def info(blabla):
    server = blabla.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    numberOfPerson = server.member_count
    serverName = server.name
    message = f"{serverName} a actuellement {numberOfPerson} utilisateurs. \nLa CDC possede {numberOfTextChannels} salons textuels et {numberOfVoiceChannels} salons vocaux. "
    await blabla.send(message)

@bot.command()
@commands.check(commande_bot_channel)
@commands.has_permissions(manage_messages = True)
async def clear(blabla, nombre : int):
    await blabla.channel.purge(limit = nombre + 1)


@bot.command()
@commands.check(commande_bot_channel)
@commands.has_permissions(ban_members = True)
async def ban(blabla, user : discord.User, *, reason = "Sans raison"):
    reason = "".join(reason)
    await blabla.guild.ban(user, reason = reason)
    await blabla.send(f"{user} a été ban du serveur pour la raison suivante : {reason}.")

@bot.command()
@commands.check(commande_bot_channel)
@commands.has_permissions(kick_members = True)
async def kick(blabla, user : discord.User, *, reason = "Sans raison"):
    reason = "".join(reason)
    await blabla.guild.kick(user, reason = reason)
    await blabla.send(f"{user} a été kick du serveur pour la raison suivante : {reason}.")

@bot.command()
@commands.check(commande_bot_channel)
@commands.has_permissions(ban_members = True)
async def unban(blabla, user, *, reason = "Sans raison"):
    reason = "".join(reason)
    userName, userId = user.split("#")
    bannedUsers = await blabla.guild.bans()
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userId:
            await blabla.guild.unban(i.user, reason = reason)
            await blabla.send(f"{user} a été unban du serveur pour la raison suivante : {reason}.")
            return
    await blabla.send(f"{UserName} n'est pas dans la liste des bans")

@bot.command()
@commands.check(commande_bot_channel)
@commands.has_permissions(ban_members = True)
async def deban(blabla, user, *, reason = "Sans raison"):
    reason = "".join(reason)
    userName, userId = user.split("#")
    bannedUsers = await blabla.guild.bans()
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userId:
            await blabla.guild.unban(i.user, reason = reason)
            await blabla.send(f"{user} a été déban du serveur pour la raison suivante : {reason}.")
            return
    await blabla.send(f"{UserName} n'est pas dans la liste des bans")

@bot.command()
@commands.check(commande_bot_channel)
@commands.has_permissions(mute_members = True)
async def mute(blabla, user, *, reason = "Sans raison"):
    mutedRole = await getMutedRole(blabla)
    await member.add_roles(mutedRole, reason = reason)
    await blabla.send(f"{member.mention} a été mute pour la raison suivante : {reason}.")

@bot.command()
@commands.check(commande_bot_channel)
@commands.has_permissions(mute_members = True)
async def unmute(blabla, user, *, reason = "Sans raison"):
    mutedRole = await getMutedRole(blabla)
    await member.remove_roles(mutedRole, reason = reason)
    await blabla.send(f"{member.mention} a été unmute pour la raison suivante : {reason}.")

@bot.command()
@commands.check(commande_bot_channel)
@commands.has_permissions(mute_members = True)
async def demute(blabla, user, *, reason = "Sans raison"):
    mutedRole = await getMutedRole(blabla)
    await member.remove_roles(mutedRole, reason = reason)
    await blabla.send(f"{member.mention} a été démute pour la raison suivante : {reason}.")

client.run('Nzc4MzIyNzkxMTU3NTk2MTkw.X7QTlQ.6wFAI_UInZkwIW9ClpCs5UvKTaE')