import discord


def get_client_token():
    f = open("client_token.txt", "r")
    s = f.read().strip()
    f.close()
    return s

# constant


client = discord.Client()
client.run(get_client_token())
