from datetime import datetime

def find_min_day(days):
    min_day = {"day": "", "count": -1}

    for day,count in days.items():
        if min_day['count'] >= 0:
            if count < min_day['count']:
                min_day = {"day": day, "count": count}
        else:
            min_day = {"day": day, "count": count}

    return min_day

def top_10_days(file_name, chunksize, max_amount_chunk):
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

    last_tweet = 0

    # Information that will be saved from each user
    keys = ("id", "username", "url", "description")

    days = {}

    for chunk in chunks:
        if chunk_count == max_amount_chunk:
            break
        for i in range(last_tweet, last_tweet + chunksize):
            # We only care about the month/day/year of the tweet
            day = chunk['date'][i].strftime("%m/%d/%Y")

            # We store the date in the dict if it's the first time we cross it
            if day not in days:
                days[day] = 1
            else:
                days[day] += 1

        last_tweet += chunksize
        chunk_count += 1

    top_10_days = {}
    total_days = 0
    min_day = {'day': '', 'count': 0}

    # Find the top 10 days
    for day,count in days.items():
        if count > min_day['count']:
            if total_days < 10:
                top_10_days[day] = count
                total_days += 1

                if total_days == 10:
                    min_day = find_min_day(top_10_days)
            else:
                del top_10_days[min_day['day']]
                top_10_days[day] = count

                min_day = find_min_day(top_10_days)

    # Sort a dict by value | Source: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    list_count = sorted(top_10_days.items(), key=lambda item: item[1], reverse= True)

    return list_count
