# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch


def search_syntax(start=0, size=0, start_time='2016-03-24T00:00:00', end_time=None):
    return {
        "from": start,
        "size": size,
        "fields": [
           "@timestamp", "browserid", "action", "state_name"
        ],
        "query": {
            "bool": {
                "must": [
                    {
                        "query_string": {
                            "query": "action:log_state_change AND -token_username:* AND browserid:*"
                        }
                    },
                    {
                        "range": {
                            "@timestamp": {
                                # "gte": "now-" + str(day) + "d",
                                "gte": start_time,
                                "lte": end_time,
                                "time_zone": "+08:00"
                            }
                        }
                    }
                ]
            }
        },
        "sort": [
           {
              "@timestamp": {
                 "order": "asc"
              }
           }
        ],
        "aggs": {
            "browserid_tag": {
                "terms": {
                    "field": "browserid"
                }
            }
        }
    }


class LogData(object):

    def __init__(self, host=None, index_name=None, start_time=None, end_time=None):
        """LogData is a class to collect log from Elasticsearch.

        Parameters
        ----------
        host: string, Elasticsearch IP
        index_name: string, index name in Elasticsearch
        start_time: date string, format looks like '2016-03-24T00:00:00'
        end_time: date string, format looks like '2016-03-24T00:00:00'
                  if empty this field, 'now' will use.

        Returns
        -------

        """
        if host:
            self.host = host
        else:
            raise ValueError("Elasticsearch host cannot be empty.")

        if index_name:
            self.index_name = index_name
        else:
            raise ValueError("index name cannot be empty.")

        if start_time:
            self.start_time = start_time
        else:
            self.start_time = '2016-03-24T00:00:00'

        if end_time:
            self.end_time = end_time
        else:
            self.end_time = 'now'

        self.es = Elasticsearch(['http://' + self.host + ':9200'])
        self.total, self.browser_ids = self._total_log_browser_ids()

    def _total_log_browser_ids(self):
        search_result = self.es.search(index=self.index_name, body=search_syntax(start=0, size=0,
                                                                                 start_time=self.start_time,
                                                                                 end_time=self.end_time))
        return search_result['hits']['total'], [bucket['key'] for bucket in search_result['aggregations']['browserid_tag']['buckets']]

    def result(self, start=0, size=0):
        search_result = self.es.search(index=self.index_name, body=search_syntax(start=start, size=size,
                                                                                 start_time=self.start_time,
                                                                                 end_time=self.end_time))
        return search_result['hits']['hits']