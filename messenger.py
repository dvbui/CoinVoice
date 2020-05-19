NAME_HEADER = "Name"
SCORE_HEADER = "Score"
ID_HEADER = "Rank"


def fitting(s, length):
    return s + " " * max(0, (length - len(s)))


def rank_list(client, user_data, number_of_players=10, max_length_string=1992):
    result = ""
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
            max_score_length = max(max_score_length, len(str(user_list[current][1])))
            if inserted == number_of_players:
                break
        current += 1

    number_of_players = min(number_of_players, inserted)
    max_id_length = max(max_id_length, len(str(number_of_players)))

    name_header = fitting(NAME_HEADER, max_user_length)
    score_header = fitting(SCORE_HEADER, max_score_length)
    id_header = fitting(ID_HEADER, len(str(number_of_players)))

    header = id_header + " " + name_header + " " + score_header
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
            score_str = fitting(str(user_list[current][1]), max_score_length)
            res += id_str + " " + member_name + " " + score_str + "\n"
            if inserted == number_of_players:
                break
        current += 1

    return res[0:min(max_length_string, len(res))]




