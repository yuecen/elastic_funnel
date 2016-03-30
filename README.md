## Elastic Funnel

This is an analysis tool for funnel visualization with log from Elasticsearch. Even though we have [Kibana] can display log very well, 
it can't fit our goal that to analyze series log with context. 

### Prerequisites

In order to run elastic_funnel, some works have to prepare.

  ** You have to add at least a field with name ```state_name``` into your index **

### Quick Start with CLI

#### Install

  ** [Pandas] is one of core requirements and it could take a few minutes to complete. **

```
pip install elastic_funnel
```

#### Add Essential Config File

Add the argument file ```~/.elastic_funnel``` to your home path, with

```
[elastic]
host = 127.0.0.1
port = 9200
index = user-behavior-*
query = action:log_state_change AND -token_username:* AND sessionid:* 
fields = @timestamp, sessionid, state_name, action
timefield = @timestamp
stagefield = state_name
identity = sessionid
```

#### Arguments

```
usage: elastic_funnel [-h] [--host HOST] [--port PORT] [--index INDEX]
                      --stages STAGES [STAGES ...] [--start START] [--end END]
                      [--add_query ADD_QUERY]

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           Host of Elasticsearch
  --port PORT           Port of Elasticsearch
  --index INDEX         Index name of Elasticsearch, e.g., user-behavior-log-*
  --stages STAGES [STAGES ...]
                        Set a path of stages , e.g., index explore user
                        explore
  --start START         Start time of log, e.g., 2016-03-24T00:00:00
  --end END             End time of log, e.g., 2016-03-28T00:00:00
  --add_query ADD_QUERY
                        Additional query using syntax of Lucene, https://lucen
                        e.apache.org/core/2_9_4/queryparsersyntax.html. You
                        can narrow you search target by syntax, e.g.,
                        country:US
```

#### Run for a Funnel

```
elastic_funnel --stages index newTopic playgroundTopic --start 2016-03-25T00:00:00
```

#### Funnel Visualization with ASCII Characters

You could get a response looks like follows, the percentage means trend from one stage to the next.

```
Funnel: index --> newTopic --> playgroundTopic 
############################################################################### 
██████████████████████████████████████████████████  27          100.0%  index          
██████████████                                       8          29.6%   newTopic        
█                                                    1          12.5%   playgroundTopic
```

### Quick Start with Gunicorn and cRUL ( *DEVELOPING...* )

To run this script, a Gunicorn server will be run on your host:

```
$ ./funnel_web.sh
```

[Kibana]:https://www.elastic.co/products/kibana
[Pandas]:http://pandas.pydata.org/