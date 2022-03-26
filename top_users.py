def get_count(user):
    return user['count']

def find_min_user(users):
    min_id = 0
    min_user = {"count": -1}

    for value in users.values():
        if min_user['count'] >= 0:
            if value['count'] < min_user['count']:
                min_user = value
        else:
            min_user = value

    return min_user

def top_10_users(file_name, chunksize, max_amount_chunk):
    """
    file_name: path's file.
    chunksize: size of the chunks in which the file will be separately read.
    max_amount_chunk: cause of the large size of the json file, this parameter
    will restric how many chunks will be read.

    The amount of lines (tweets) that will be read follows the following equation:
    number = chunksize * max_amount_chunk
    """

    # Importing required libraries
    import pandas as pd

    # Read JSON file containing tweets data
    # Cause of the large size of the dataset, we will read it by chunks of a determinate size
    chunks = pd.read_json(file_name, lines=True, chunksize=chunksize)

    chunk_count = 0

    last_user = 0

    # Information that will be saved from each user
    keys = ("id", "username", "url", "description")

    users = {}

    for chunk in chunks:
        if chunk_count == max_amount_chunk:
            break
        for i in range(last_user, last_user + chunksize):
            user = {key: chunk['user'][i][key] for key in keys}

            # We store the user in the dict if it's the first time we cross them
            if user['id'] not in users:
                users[user['id']] = user
                users[user['id']]['count'] = 1
            else:
                users[user['id']]['count'] += 1

        last_user += chunksize
        chunk_count += 1

    top_10_users = {}
    total_users = 0
    min_user = {'count': 0}

    # Find the top 10 users
    for key,value in users.items():
        if value['count'] > min_user['count']:
            if total_users < 10:
                top_10_users[key] = value
                total_users += 1
                if total_users == 10:
                    min_user = find_min_user(top_10_users)
            else:
                del top_10_users[min_user['id']]
                top_10_users[value['id']] = value

                min_user = find_min_user(top_10_users)

    # Sort top user
    return_list = []
    max_count = 0

    current_max_user = None
    # Sort dict according to tweets count
    while top_10_users.keys():
        for id,user in top_10_users.items():
            if user['count'] > max_count:
                current_max_user = user
                max_count = user['count']

        return_list.append(current_max_user)
        top_10_users.pop(current_max_user['id'], None)
        max_count = 0

    return return_list
