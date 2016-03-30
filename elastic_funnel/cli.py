# -*- coding: utf-8 -*-

import argparse

from funnel import FunnelData, ascii_funnel
from elasticsearch_data import es_host, es_port, es_index, es_stagefield


class CliArgs:
    def __init__(self):
        p = argparse.ArgumentParser(prog='elastic_funnel')
        p.add_argument('--host', help='Host of Elasticsearch')
        p.add_argument('--port', type=int, help='Port of Elasticsearch')
        p.add_argument('--index', help='Index name of Elasticsearch, e.g., user-behavior-log-*')
        p.add_argument('--stages', required=True, nargs='+', help='Set a path of stages , '
                                                                  'e.g., index explore user explore')
        p.add_argument('--start', help='Start time of log, e.g., 2016-03-24T00:00:00')
        p.add_argument('--end', help='End time of log, e.g., 2016-03-28T00:00:00')
        p.add_argument('--add_query', help='Additional query using syntax of Lucene, '
                                       'https://lucene.apache.org/core/2_9_4/queryparsersyntax.html. '
                                       'You can narrow you search target by syntax, e.g., country:US')
        args = p.parse_args()

        self.host = args.host if args.host else es_host
        self.port = args.port if args.port else es_port
        self.index = args.index if args.index else es_index
        self.stages = args.stages
        self.start = args.start
        self.end = args.end
        self.add_query = args.add_query


def main():
    cli_args = CliArgs()

    funnel_data = FunnelData(host=cli_args.host, port=cli_args.port, index_name=cli_args.index,
                             start_time=cli_args.start, end_time=cli_args.end, add_query=cli_args.add_query)
    funnel_data.set_stages([{es_stagefield: stage} for stage in cli_args.stages])

    fd = funnel_data.calculate_funnel()

    fd = [('\t' + '{0:.1f}'.format(d[3].values()[0]) + '% \t' + d[2].values()[0], d[0]) for d in fd]

    print ' \n'.join([g.encode('utf-8') for g in ascii_funnel('Funnel: ' + ' --> '.join(cli_args.stages), fd)])


if __name__ == '__main__':
    main()
