import re

def find_min_hashtag(hashtags):
    min_hashtag = {"name": "", "count": -1}

    for hashtag,count in hashtags.items():
        if min_hashtag['count'] >= 0:
            if count < min_hashtag['count']:
                min_hashtag = {"name": hashtag, "count": count}
        else:
            min_hashtag = {"name": hashtag, "count": count}

    return min_hashtag

def top_10_hashtags(file_name, chunksize, max_amount_chunk):
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

    last_tweet = 0
    chunk_count = 0

    hashtags = {}

    for chunk in chunks:
        if chunk_count == max_amount_chunk:
            break
        for i in range(last_tweet, last_tweet + chunksize):
            content = chunk['content'][i]
            tweet_hashtags = re.findall(r"#(\w+)", content)

            for hashtag in tweet_hashtags:
                if hashtag not in hashtags:
                    hashtags[hashtag] = 1
                else:
                    hashtags[hashtag] += 1
        last_tweet += chunksize
        chunk_count += 1

    top_10_hashtags = {}
    total_hashtags = 0
    min_hashtag = {'name': '', 'count': 0}

    # Find the top 10 days
    for hashtag,count in hashtags.items():
        if count > min_hashtag['count']:
            if total_hashtags < 10:
                top_10_hashtags[hashtag] = count
                total_hashtags += 1

                if total_hashtags == 10:
                    min_hashtag = find_min_hashtag(top_10_hashtags)
            else:
                del top_10_hashtags[min_hashtag['name']]
                top_10_hashtags[hashtag] = count

                min_hashtag = find_min_hashtag(top_10_hashtags)

    # Sort a dict by value | Source: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    list_count = sorted(top_10_hashtags.items(), key=lambda item: item[1], reverse= True)

    return list_count
