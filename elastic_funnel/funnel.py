# -*- coding: utf-8 -*-

import pandas as pd
from ascii_graph import Pyasciigraph
from elasticsearch_data import LogData, es_identity, es_fields

pd.set_option('display.width', 1000)


def ascii_funnel(info, funnel_data):
    """Return ascii graph by funnel data.

    Parameters
    ----------
    info: string
    funnel_data: list of tuple

    Returns list of ascii string.
    -------

    """
    graph = Pyasciigraph()
    return graph.graph(info, funnel_data)


class FunnelData(LogData):

    def __init__(self, host=None, port=None, index_name=None, start_time=None, end_time=None, add_query=None):
        LogData.__init__(self, host, port, index_name, start_time, end_time, add_query)

        self.dataframe = None
        self.integrate_data()
        self.stages = None
        """list: stages is a list.
        Example:
            [[0, True, {"state_name": "index"}], [0, False, {"state_name": explore}]]
        """

        self.stages_count = None

    def integrate_data(self):
        df = []
        size = 50
        pages = self.total / size
        print "Integrating data from Elasticsearch..."
        for i in range(0, pages + 1):
            res = self.result(start=(i * size), size=size)
            for hit in res:
                df.append({field: hit['fields'][field][0] for field in es_fields})

        self.dataframe = pd.DataFrame(df, columns=es_fields)

    def set_stages(self, stages):
        """Set funnel stages before you calculating it

        :param stages: a list of dict
        :return: a list of list
        """
        self.stages = [[0, False, stage] for stage in stages]
        self.stages[0][1] = True
        return self.stages

    def calculate_funnel(self):
        if self.stages is None:
            raise ValueError("stages cannot be empty.")

        for browser_id in self.browser_ids:
            # print "Browser ID: " + browser_id
            user_data_set = self.dataframe.loc[self.dataframe[es_identity] == browser_id]
            self.stages[0][1] = True
            for index, record in user_data_set.iterrows():
                self._count_stage(record)

        return self.stages_percentage()

    def _count_stage(self, record_stage):
        stage_idx = 0
        while stage_idx < len(self.stages):
            """Search flag using while loop"""
            if self.stages[stage_idx][1]:
                stage_key = self.stages[stage_idx][2].keys()[0]
                stage_val = self.stages[stage_idx][2].values()[0]

                record_stage_val = record_stage[stage_key]
                # print stage_val + " @ " + record_stage_val + " " + record_stage['@timestamp']

                if stage_val == record_stage_val:
                    # print "^^^^^^^^^^^^^^^^^^^^^^ MATCH"
                    self.stages[stage_idx][0] += 1
                    self.stages[stage_idx][1] = False
                    if (stage_idx + 1) >= len(self.stages):
                        self.stages[0][1] = True
                    else:
                        self.stages[stage_idx + 1][1] = True
                    break
                else:
                    self.stages[stage_idx][1] = False
                    self.stages[0][1] = True

                    first_stage_val = self.stages[0][2].values()[0]
                    # print first_stage_val + " @ " + record_stage_val
                    if first_stage_val == record_stage_val:
                        # print "^^^^^^^^^^^^^^^^^^ MATCH"
                        self.stages[0][0] += 1
                        self.stages[0][1] = False
                        self.stages[1][1] = True
                        break
            stage_idx += 1

    def stages_percentage(self):
        for idx, stage in enumerate(self.stages):
            if idx == 0:
                stage.append({'trend': 100})
            else:
                if self.stages[idx - 1][0 ] == 0:
                    stage.append({'trend': 0.0})
                else:
                    trend = (stage[0] * 100.0) / (self.stages[idx - 1][0])
                    stage.append({'trend': trend})

        return self.stages


if __name__ == '__main__':
    import sys
    funnel_data = FunnelData(host=sys.argv[1], index_name='beta-backend-socketlog-*')
    print funnel_data.total
    funnel_data.set_stages([{'state_name': 'index'}, {'state_name': 'newTopic'}, {'state_name': 'PlaygroundTopic'}])
    print funnel_data.calculate_funnel()
