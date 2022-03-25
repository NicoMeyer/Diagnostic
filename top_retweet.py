
def top_10_retweet(file_name, chunksize, max_amount_chunk):
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

    top_tweets = {}
    total_list = 0
    min_tweet = 0

    last_tweet = 0

    # Tuple with the important labels to store the tweet's information
    columns = ('url', 'date', 'content', 'id', 'retweetCount', 'likeCount', 'quoteCount')

    chunk_count = 0

    for chunk in chunks:
        if chunk_count == max_amount_chunk:
            break
        for i in range(last_tweet, last_tweet + chunksize):
            # If retweetCount is bigger than the min retweetCount known
            # so far, then it should be added to the dict
            if chunk['retweetCount'][i] > min_tweet:
                tweet = {column: chunk[column][i] for column in columns}
                # If the retweetCount is not already in the dict, then it will
                # replace the existing one, so the amount of tweet won't increase
                exists = chunk['retweetCount'][i] in top_tweets.keys()

                if total_list < 10:
                    if not exists:
                        total_list += 1
                    top_tweets[chunk['retweetCount'][i]] = tweet

                    # We will only compare to the min retweetCount when we
                    # have at least 10 tweets in the dict (top_tweets)
                    if total_list == 10:
                        keys = top_tweets.keys()
                        min_tweet = min(keys)
                else:
                    if not exists:
                        del top_tweets[min_tweet]
                        top_tweets[chunk['retweetCount'][i]] = tweet
                        keys = top_tweets.keys()
                        min_tweet = min(keys)

        last_tweet += chunksize
        chunk_count += 1

    list_count = sorted(top_tweets.keys(), reverse=True)
    return_list = []

    for i in range(len(list_count)):
        return_list.append(top_tweets[list_count[i]])

    return return_list
