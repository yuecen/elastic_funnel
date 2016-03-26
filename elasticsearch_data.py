from elasticsearch import Elasticsearch


def search_syntax(start=0, size=0, day=1):
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
                                "gte": "now-" + str(day) + "d",
                                "lt":  "now"
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

    def __init__(self, host=None, index_name=None, day=1):
        print "init logdata"
        if not host:
            raise ValueError("Elasticsearch host cannot be empty.")
        else:
            self.host = host
        if not index_name:
            raise ValueError("index name cannot be empty.")
        else:
            self.index_name = index_name
        if not day:
            raise ValueError("day cannot be empty.")
        else:
            self.day = day

        self.es = Elasticsearch(['http://' + self.host + ':9200'])
        self.total, self.browser_ids = self._total_log_browser_ids()

    def _total_log_browser_ids(self):
        search_result = self.es.search(index=self.index_name, body=search_syntax(start=0, size=0, day=self.day))
        return search_result['hits']['total'], [bucket['key'] for bucket in search_result['aggregations']['browserid_tag']['buckets']]

    def result(self, start=0, size=0):
        search_result = self.es.search(index=self.index_name, body=search_syntax(start=start, size=size, day=self.day))
        return search_result['hits']['hits']