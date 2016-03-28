# -*- coding: utf-8 -*-
import os
import ConfigParser

from elasticsearch_data import LogData
from flask import Flask, Response
from funnel import FunnelData

from ascii_graph import Pyasciigraph

app = Flask(__name__)

config = ConfigParser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'funnel.ini'))

es_host = os.environ['ELASTIC_HOST'] if os.environ.get('ELASTIC_HOST') else config.get('elastic', 'host')
es_port = os.environ['ELASTIC_PORT'] if os.environ.get('ELASTIC_PORT') else config.get('elastic', 'port')
es_index = os.environ['ELASTIC_INDEX'] if os.environ.get('ELASTIC_INDEX') else config.get('elastic', 'index')


@app.route('/f', methods=['GET'])
def handler():
    funnel_data = FunnelData(LogData(host=es_host,
                            index_name=es_index,
                            day=10))
    print funnel_data.total
    funnel_data.set_stages({'state_name': 'index'},
                   {'state_name': 'newTopic'},
                   # {'state_name': 'index'},
                   # {'state_name': 'newTopic'},
                   {'state_name': 'playgroundTopic'})
    fd = funnel_data.calculate_funnel()
    fd = [('\t' + '{0:.1f}'.format(d[3].values()[0]) + '% \t' + d[2].values()[0], d[0]) for d in fd]

    return Response(' \n'.join(ascii_graph(fd)), mimetype='text/plain')


def ascii_graph(funnel_data):
    """
    test = [('long_label', 423), ('sl', 1234), ('line3', 531),
        ('line4', 200), ('line5', 834)]

    graph = Pyasciigraph()
    for line in graph.graph('test print', test):
        print line
    """
    graph = Pyasciigraph()
    return graph.graph('Funnel', funnel_data)


if __name__ == '__main__':
    app.run('0.0.0.0', 5577, debug=True)