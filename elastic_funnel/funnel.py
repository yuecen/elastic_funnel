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


class Stage(object):
    def __init__(self, total=0, flag=False, name=None):
        self.total = total
        self.flag = flag
        # name -> {"state_name": "index"}
        self.name = name
        self.trend = 0.0


class FunnelData(LogData):

    def __init__(self, host=None, port=None, index_name=None, start_time=None, end_time=None, add_query=None):
        LogData.__init__(self, host, port, index_name, start_time, end_time, add_query)

        self.dataframe = None
        self.integrate_data()
        """list: stages is a list.
        Example:
            [Stage(name={"state_name": "index"}), Stage(name={"state_name": explore})]
        """
        self.stages = None

    def integrate_data(self):
        df = []
        size = 50
        pages = self.total / size
        print "Integrating data from Elasticsearch..."
        for i in range(0, pages + 1):
            res = self.result(start=(i * size), size=size)
            for hit in res:
                df.append({field: hit['fields'][field][0] for field in es_fields})
        self.dataframe = pd.DataFrame(df, columns=es_fields).sort(['@timestamp'], ascending=True)

    def set_stages(self, stages):
        """Set funnel stages before you calculating it

        :param stages: a list of dict
        :return: a list of list
        """

        # First is for count, so the initial value is zero.
        # Second is a True or False flag for calculating.
        # Third is a dict of stage name.
        self.stages = [Stage(name=stage) for stage in stages]
        # Init first flag
        (self.stages[0]).flag = True
        return self.stages

    def count_funnel(self):
        if self.stages is None:
            raise ValueError("stages cannot be empty.")

        for browser_id in self.browser_ids:
            # print "Browser ID: " + browser_id

            # Select data set by browser_id
            user_data_set = self.dataframe.loc[self.dataframe[es_identity] == browser_id]
            (self.stages[0]).flag = True
            for index, record in user_data_set.iterrows():
                self._calculate(record)

        return self.stages_percentage()

    def _calculate(self, record):
        """
        Calculate stages count by each record.

        The record input looks like:

            @timestamp          2016-08-24T12:15:10.558791129Z
            sessionid                      3929-45d7-9f53-af87
            action                                state_change
            state                                   searchpage
        """
        stage_idx = 0
        while stage_idx < len(self.stages):
            # Search flag using while loop

            # If a stage flag with a switch true
            if (self.stages[stage_idx]).flag:
                stage_key = (self.stages[stage_idx]).name.keys()[0]
                stage_val = (self.stages[stage_idx]).name.values()[0]

                record_stage_val = record[stage_key]

                # Match!!
                if stage_val == record_stage_val:
                    (self.stages[stage_idx]).total += 1
                    (self.stages[stage_idx]).flag = False
                    if (stage_idx + 1) >= len(self.stages):
                        # Restart a traversal
                        (self.stages[0]).flag = True
                    else:
                        # Go to next stage for a check
                        (self.stages[stage_idx + 1]).flag = True
                    break
                else:
                    # Mismatched, set current stage into False,
                    # and set first stage is True for restart a traversal.
                    (self.stages[stage_idx]).flag = False
                    (self.stages[0]).flag = True

                    # Although current record stage don't match current stage,
                    # it still can compare with the first stage for traversal.
                    first_stage_val = (self.stages[0]).name.values()[0]

                    # Match!!
                    if first_stage_val == record_stage_val:
                        (self.stages[0]).total += 1
                        (self.stages[0]).flag = False
                        (self.stages[1]).flag = True
                        break

            stage_idx += 1

    def stages_percentage(self):
        for idx, stage in enumerate(self.stages):
            if idx == 0:
                stage.trend = 100
            else:
                if (self.stages[idx - 1]).total == 0:
                    stage.trend = 0.0
                else:
                    trend = (stage.total * 100.0) / (self.stages[idx - 1]).total
                    stage.trend = trend

        return self.stages
