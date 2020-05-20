import discord
import json
import asyncio
import sys
import messenger

sys.setrecursionlimit(10**6)

client = discord.Client()

CLIENT_TOKEN_FILE = "client_token.txt"
VOICE_CHANNEL_FILE = "voice_channel.txt"
USER_DATA_FILE = "user_data_file.json"
MENU_DATA = "role_menu.txt"
ITERATION = 1
UNIT_MONEY = 1

user_data = {}
voice_channel = {}
role_menu = {}


def get_client_token():
    f = open(CLIENT_TOKEN_FILE, "r")
    s = f.read().strip()
    f.close()
    return s


def load_user_data():
    global user_data
    f = open(USER_DATA_FILE, "r")
    s = f.read().strip()
    user_data = json.loads(s)
    f.close()


def load_voice_channel():
    global voice_channel
    f = open(VOICE_CHANNEL_FILE, "r")
    s = f.read().strip().split('\n')
    f.close()
    for line in s:
        voice_channel[int(line.strip())] = ""


def load_role_menu():
    global role_menu
    f = open(MENU_DATA, "r")
    s = f.read().strip().split('\n')
    f.close()
    for line in s:
        element = line.split(' ')
        if len(element) != 2:
            return
        role_id = int(element[0])
        role_price = int(element[1])
        role_menu[role_id] = role_price


def save_user_data():
    global user_data
    try:
        f = open(USER_DATA_FILE, "w")
        f.write(json.dumps(user_data))
        f.close()
    except:
        print("Can't save user data")


async def main_loop():
    await client.wait_until_ready()

    load_user_data()

    total = {}
    for channel_id in voice_channel:
        current_channel = client.get_channel(channel_id)
        for member in current_channel.members:
            total[str(member.id)] = {}

    for member_id in total:
        if member_id in user_data:
            user_data[member_id] += UNIT_MONEY
        else:
            user_data[member_id] = UNIT_MONEY

    save_user_data()

    await asyncio.sleep(ITERATION)
    await main_loop()


async def send_message(channel, content):
    try:
        await channel.send(content)
    except:
        print("Can't send message")


@client.event
async def on_ready():
    print("Bot is ready.")
    load_user_data()
    load_voice_channel()
    load_role_menu()
    messenger.load_help_message()
    await main_loop()


def to_int(x):
    try:
        return int(x)
    except ValueError:
        return -1


def to_user_id(s):
    s = s.replace("<", "")
    s = s.replace(">", "")
    s = s.replace("@", "")
    s = s.replace("!", "")
    s = s.replace("&", "")
    return to_int(s)


async def give_role(member, role):
    try:
        await member.add_roles(role)
    except:
        print("Can't give role")


@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return
    message.content = message.content.lower()
    args = message.content.split(' ')
    if args[0] != "coin":
        return

    if len(args) == 2 and args[1] == "rank":
        await send_message(message.channel, "```\n" + messenger.rank_list(client, user_data) + "```\n")

    if len(args) == 2 and args[1] == "account":
        user_id = message.author.id
        coin = 0
        if str(user_id) in user_data:
            coin = user_data[str(user_id)]
        await send_message(message.channel, "You have {} coins.".format(coin))

    if len(args) == 2 and args[1] == "menu":
        await send_message(message.channel, "```\n" + messenger.role_menu(message, role_menu) + "```\n")

    if len(args) == 3 and args[1] == "buy":
        role_index = to_int(args[2])
        if not (1 <= role_index <= len(role_menu)):
            return
        cnt = 0
        selected_role = None
        selected_role_id = None
        for role_id in role_menu:
            cnt += 1
            if cnt == role_index:
                selected_role_id = role_id
                selected_role = discord.utils.get(message.guild.roles, id=role_id)
                break

        price = role_menu[selected_role_id]
        if str(message.author.id) in user_data and user_data[str(message.author.id)] >= price:
            await give_role(message.author, selected_role)
            user_data[str(message.author.id)] -= price
            save_user_data()
            await send_message(message.channel, "Role granted.")
        else:
            await send_message(message.channel, "You do not have enough money.")

    if len(args) == 4 and args[1] == "give":
        if to_user_id(args[2]) != -1 and to_int(args[3]) >= 0:
            recipient_id = to_user_id(args[2])
            money = to_int(args[3])

            recipient = client.get_user(recipient_id)

            if recipient is None:
                await send_message(message.channel, "The user does not exist")
                return

            if str(message.author.id) in user_data and user_data[str(message.author.id)] >= money:
                user_data[str(message.author.id)] -= money
                if str(recipient_id) in user_data:
                    user_data[str(recipient_id)] += money
                else:
                    user_data[str(recipient_id)] = money

                await send_message(message.channel, "Money transferred.")
            else:
                await send_message(message.channel, "You do not have enough money.")

            save_user_data()

    if len(args) == 2 and args[1] == "help":
        await send_message(message.channel, messenger.help_message())


client.run(get_client_token())
