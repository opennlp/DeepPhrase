from config import keys
from newsapi.articles import Articles
from newsapi.sources import Sources
import requests


class News:

    def __init__(self,api_key=keys.news['api_key']):
        self.api_key = api_key
        self.article = Articles(self.api_key)
        self.source = Sources(self.api_key)
        self.base_url = keys.news['base_everything_url']

    def get_data(self, query, from_date=None, to_date=None, page_size=100, sort_by='publishedAt', language='en', **kwargs):
        key_value_params = {
            'apiKey': self.api_key,
            'q': query,
            'from': from_date,
            'to': to_date,
            'sortBy': sort_by,
            'pageSize': page_size,
            'language': language
        }

        url = self._data_config(self.base_url, query_separator='?', key_value_params=key_value_params)
        response = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
        return self._parse_data(response.json())

    @staticmethod
    def _data_config(base_url, **kwargs):
        query_separator = None
        key_value_params = None
        join_sep = '&'
        url = base_url
        if 'query_separator' in kwargs.keys():
            query_separator = kwargs['query_separator']
        if 'key_value_params' in kwargs.keys():
            key_value_params = kwargs['key_value_params']
        if query_separator is not None:
            url = base_url + str(query_separator)
        if key_value_params is not None:
            for key in key_value_params.keys():
                if key_value_params[key] is not None:
                    url = url + str(key) + '=' + str(key_value_params[key]) + join_sep
        return url[:-1]

    @staticmethod
    def _parse_data(news_response_json):
        article_list = list([])
        if news_response_json['status'] == 'ok':
            article_list = news_response_json['articles']
        for article in article_list:
            try:
                article['source'] = article['source']['name']
            except:
                pass
        return article_list

    def get_articles(self,source_id,selection_type="popular"):
        if selection_type == 'latest':
            return self.article.get_by_latest(source_id)
        elif selection_type == 'top':
            return self.article.get_by_top(source_id)
        else:
            return self.article.get_by_popular(source_id)
