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
ITERATION = 1
UNIT_MONEY = 1

user_data = {}
voice_channel = {}


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


def save_user_data():
    global user_data
    f = open(USER_DATA_FILE, "w")
    f.write(json.dumps(user_data))
    f.close()


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

    print(messenger.rank_list(client, user_data, 10))
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
    await main_loop()

def to_int(x):
    try:
        return int(x)
    except ValueError:
        return -1

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
        pass

    if len(args) == 3 and args[1] == "buy":
        pass


client.run(get_client_token())
