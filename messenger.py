import discord

NAME_HEADER = "Name"
SCORE_HEADER = "Coins"
ID_HEADER = "Rank"
ROLE_MENU_HEADER = "Role Menu"
HELP_MESSAGE_FILE = "help_message.txt"


help_message_data = ""


def load_help_message():
    f = open(HELP_MESSAGE_FILE, "r")
    global help_message_data
    help_message_data = f.read().strip()


def fitting(s, length):
    return s + " " * max(0, (length - len(s)))


def rank_list(client, user_data, number_of_players=10, max_length_string=1992, deliminator=" | "):
    number_of_players = min(number_of_players, len(user_data))
    user_list = [[x, y] for x, y in user_data.items()]
    user_list.sort(key=lambda u: -u[1])

    max_user_length = len(NAME_HEADER)
    max_score_length = len(SCORE_HEADER)
    max_id_length = len(ID_HEADER)

    inserted = 0
    current = 0
    while current < len(user_list):
        member = client.get_user(int(user_list[current][0]))
        if not (member is None):
            inserted += 1
            max_user_length = max(max_user_length, len(str(member)))
            max_score_length = max(max_score_length, len("{:.2f}".format(user_list[current][1])))
            if inserted == number_of_players:
                break
        current += 1

    number_of_players = min(number_of_players, inserted)
    max_id_length = max(max_id_length, len(str(number_of_players)))

    name_header = fitting(NAME_HEADER, max_user_length)
    score_header = fitting(SCORE_HEADER, max_score_length)
    id_header = fitting(ID_HEADER, len(str(number_of_players)))

    header = id_header + deliminator + name_header + deliminator + score_header
    barrier = "-" * len(header)
    res = header + "\n" + barrier + "\n"

    inserted = 0
    current = 0
    while current < len(user_list):
        member = client.get_user(int(user_list[current][0]))
        if not (member is None):
            inserted += 1
            id_str = fitting(str(inserted), max_id_length)
            member_name = fitting(str(member), max_user_length)
            score_str = fitting("{:.2f}".format(user_list[current][1]), max_score_length)
            res += id_str + deliminator + member_name + deliminator + score_str + "\n"
            if inserted == number_of_players:
                break
        current += 1

    return res[0:min(max_length_string, len(res))]


def role_menu(message, role_data, max_length_string=1992):
    res = ROLE_MENU_HEADER+"\n"
    cnt = 0
    for role_id in role_data:
        role = discord.utils.get(message.guild.roles, id=role_id)
        cnt += 1
        res += str(cnt)+". "+role.name+" ({} coins)".format(role_data[role_id])+"\n"
    return res[0:min(max_length_string, len(res))]


def help_message():
    return "```\n"+help_message_data+"```\n"
