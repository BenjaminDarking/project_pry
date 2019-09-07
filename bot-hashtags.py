
from twitterapi import run_twitter_query


def bio_bot():
    results = run_twitter_query()

    print(results)

# with open("usertester", "r") as read_file:
#     data = json.load(read_file)


# def bio_hashtags():

#     for user in data:

#         bot_bio = ''.join(user.split())

#     print(bot_bio)

#     # hashtags = list(filter(lambda x: "#" in bio_bot))

#     # print(data)


# bio_hashtags()
bio_bot()
