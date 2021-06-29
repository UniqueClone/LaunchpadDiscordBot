from keep_alive import keep_alive
import discord
from discord.utils import get
import os
import random

bot_replies = open("bot_replies.json", 'r')

# bot_to_ryan and bot_to_gavin are a series of silly replies to two users the bot sends after every message sent
# by these two users. It can be switched on and off but only by the Admin 'UniqueClone2'
bot_to_ryan_on = False
bot_to_gavin_on = False

help_string = "Hi there! My name is Launchpad Bot. Welcome to the Launchpad Discord." + "\n" + ""

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #for i in client.get_all_channels():
    #  print(i, i.id)

    # Reaction Code:
    message = await client.get_channel(c_id).send(
        "React to be given a role:\n\n{} - Operations Team\n\n{} - Teams Team\n\n{} - Communications Team\n\n{} - Development Team\n\n{} - Tech Team\n\n{} - Clear Roles"
        .format(discord.PartialEmoji(name='🗓️'),
                discord.PartialEmoji(name='👨\u200d👨\u200d👧\u200d👦'),
                discord.PartialEmoji(name='📢'),
                discord.PartialEmoji(name='❤'),
                discord.PartialEmoji(name='⚙'),
                discord.PartialEmoji(name='❌')))
    for role in roles:
        await message.add_reaction(role)
    await message.add_reaction(discord.PartialEmoji(name='❌'))
    global m_id
    m_id = message.id


@client.event
async def on_message(message):
    global bot_to_ryan_on
    global bot_to_gavin_on
    print(message.author, message.author.id)
    if message.author == client.user:
        return
    elif message.author.name == "UniqueClone" and bot_to_ryan_on:
        await bot_to_ryan_function(message)
        #await message.channel.send(random.choice(bot_to_ryan))
    elif message.author.name == 'Gavin Fanning' and bot_to_gavin_on:
        await message.channel.send(random.choice(bot_to_gavin))

    if message.content.startswith('$hello'):
        await message.channel.send('Hello {0}!'.format(message.author.name))
    elif message.content == "$help":
        await message.channel.send(help_string)

    if message.content.startswith(
            "!bot_to_ryan") and message.author.name == "UniqueClone":
        await message.channel.send("loud and clear")
        if bot_to_ryan_on == True:
            bot_to_ryan_on = False
            await message.channel.send("bot_to_ryan turning off....")
        else:
            bot_to_ryan_on = True
            await message.channel.send("bot_to_ryan turning on....")

    if message.content.startswith(
            "!bot_to_gavin") and message.author.name == "UniqueClone":
        await message.channel.send("loud and clear")
        if bot_to_gavin_on == True:
            bot_to_gavin_on = False
            await message.channel.send("bot_to_gavin turning off....")
        else:
            bot_to_gavin_on = True
            await message.channel.send("bot_to_gavin turning on....")

    if message.content.startswith('!poll'):
        poll_list = message.content.split()
        print(poll_list)
        await message.channel.send(
            'Feature being built... Check console for output')

    if message.content.startswith('are my parents getting a divorce?'):
        if message.author.name == "Gavin Fanning":
            await message.channel.send("Yes and it's your fault")
        else:
            await message.channel.send(
                "How would I know? Ryan's not THAT good at coding")

    if message.content == 'new role please':
        role = get(message.guild.roles, name='test role')
        await message.author.add_roles(role)

    if message.content == '!resources':
        resources_channel = client.get_channel(851803693166755853)
        await message.channel.send(
            "You can find any resources here: {}".format(
                resources_channel.mention))


@client.event
async def on_reaction_add(reaction, user):
    return


async def bot_to_ryan_function(message):
    await message.channel.send(random.choice(bot_to_ryan))


@client.event
async def bot_switch(bot_to_ryan_on, message):
    if bot_to_ryan_on == True:
        await message.channel.send("bot_to_ryan turning off....")
        return False
    else:
        await message.channel.send("bot_to_ryan turning on....")
        return True


# Reaction to Channel Assignment
c_id = 858049154730557481 # Currently reactions-channel
m_id = 0
clear = discord.PartialEmoji(name='❌')
roles = {
    discord.PartialEmoji(name='🗓️'): 853696779160649788,
    discord.PartialEmoji(name='👨\u200d👨\u200d👧\u200d👦'): 853696967212793948,
    discord.PartialEmoji(name='📢'): 853697032745254913,
    discord.PartialEmoji(name='❤'): 853697150047617075,
    discord.PartialEmoji(name='⚙'): 853697475935076423
}


@client.event
async def on_raw_reaction_add(react):
    if react.message_id != m_id:
        return

    guild = client.get_guild(react.guild_id)

    if react.emoji == clear:
        for role in roles.values():
            await react.member.remove_roles(guild.get_role(role))
        return

    if react.emoji in roles:
        role_id = roles[react.emoji]
    else:
        print("panic1")

    role = guild.get_role(role_id)
    if role is None:
        print("panic2")
        return
    await react.member.add_roles(role)


keep_alive()

client.run(os.environ['TOKEN'])
