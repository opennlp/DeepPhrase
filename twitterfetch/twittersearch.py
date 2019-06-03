from tweepy import OAuthHandler
import tweepy
from config import keys


consumer_key = keys.twitter['consumer_key']
consumer_secret = keys.twitter['consumer_secret']
access_token = keys.twitter['access_token']
access_token_secret = keys.twitter['access_token_secret']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


class Twitter:

    def __init__(self):
        pass

    @staticmethod
    def get_filtered_json(status_model):
        search_result_json = dict({})
        if status_model is not None:
            search_result_json['text'] = status_model.text
            search_result_json['id'] = status_model.id
            search_result_json['source'] = status_model.source
            search_result_json['retweet_count'] = status_model.retweet_count
            search_result_json['created_at'] = status_model.created_at
            search_result_json['lang'] = status_model.lang
            search_result_json['place'] = status_model.place
            search_result_json['geo'] = status_model.geo
        return search_result_json

    def get_data(self, search_term, **kwargs):
        self.api = tweepy.API(auth)
        parsed_search_list = []
        count = 100
        lang = 'en'
        if 'count' in kwargs.keys():
            count = kwargs['count']
        if 'lang' in kwargs.keys():
            lang = kwargs['lang']
        search_result_list = self.api.search(q=search_term, count=count, lang=lang)
        for search_result in search_result_list:
            parsed_search_list.append(self.get_filtered_json(search_result))
        return parsed_search_list
