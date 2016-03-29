# -*- coding: utf-8 -*-
import json

from elasticsearch_data import es_index, es_port, es_host
from flask import Flask, Response, request
from funnel import FunnelData, ascii_funnel

app = Flask(__name__)


@app.route('/funnel', methods=['POST'])
def handler():
    data = request.data
    data_dict = json.loads(data)
    funnel_data = FunnelData(host=es_host, port=es_port, index_name=es_index,
                             start_time=data_dict['start_time'],
                             end_time=data_dict['end_time'])
    funnel_data.set_stages([{'state_name': 'index'},
                           {'state_name': 'newTopic'},
                           {'state_name': 'playgroundTopic'}])

    fd = funnel_data.calculate_funnel()
    fd = [('\t' + '{0:.1f}'.format(d[3].values()[0]) + '% \t' + d[2].values()[0], d[0]) for d in fd]
    return Response(' \n'.join(ascii_funnel('Funnel', fd)), mimetype='text/plain')


@app.route('/funnel_list', methods=['POST'])
def funnel_list():
    funnels = ['1. index -> newTopic -> playgroundTopic',
               '2. viewTopic -> user -> explore -> index -> newTopic -> playgroundTopic',
               '3. viewTopic -> user -> newTopic -> playgroundTopic',
               '-----------------------------------------------------------------------',
               'An example for send request with time format: 1, 2016-03-06, 2016-03-28']
    return Response(' \n'.join(funnels), mimetype='text/plain')


if __name__ == '__main__':
    app.run('0.0.0.0', 5578, debug=True)