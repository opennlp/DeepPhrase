import praw
from config import keys


class Reddit:

    def __init__(self,client_id=keys.reddit['client_id'],client_secret=keys.reddit['client_secret'],user_agent=keys.reddit['user_agent']):
        self.reddit_agent = praw.Reddit(client_id=client_id,client_secret=client_secret,user_agent=user_agent)

    def get_data(self, query, **kwargs):
        search_result_list = list([])
        subreddit_name = 'all'
        if 'subreddit_name' in kwargs.keys():
            subreddit_name = kwargs['subreddit_name']
        results = self.reddit_agent.subreddit(subreddit_name).search(query)
        for search_result in results:
            search_result_list.append(search_result)
        parsed_subreddit_data_list = list([])
        for subreddit in search_result_list:  # TODO - try-catch here
            try:
                subreddit_data = dict({'ups': subreddit.ups,
                                       'downs': subreddit.downs,
                                       'title': subreddit.title,
                                       'created': subreddit.created,
                                       'author': subreddit.author.name
                                       })
                parsed_subreddit_data_list.append(subreddit_data)
            except:
                pass
        return parsed_subreddit_data_list
