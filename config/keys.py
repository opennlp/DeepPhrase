'''
API access keys obtained from social channels
Replace this with your keys in order to make calls from the registered account and app
'''

twitter = {
    'consumer_key': "",
    'consumer_secret': "",
    'access_token': "",
    'access_token_secret': ""
}

reddit = {
    'client_id': '',
    'client_secret': '',
    'user_agent': 'praw-dev-1.0'
}

news = {
    'api_key': '',
    'base_everything_url': 'https://newsapi.org/v2/everything'
}

kafka = {
    'local_host_address': '127.0.0.1:9092',
    'twitter_topic_name': 'twitter_stream',
    'news_topic_name': 'news_stream',
    'reddit_topic_name': 'reddit_stream',
    'consumer_group_name_twitter': 'twitter_search',
    'consumer_group_name_news': 'news_search',
    'consumer_group_name_reddit':'reddit_search'
}