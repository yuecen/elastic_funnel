## Elastic Funnel

This is an analysis tool for funnel visualization with log from Elasticsearch. Even though we have [Kibana] to display log very well, 
it can't fit our goal to analyze series log with context. 

[Kibana]:https://www.elastic.co/products/kibana

### Constraint

  ** You have to add at least a field with name ```state_name``` into your index **

### Quick Start with CLI

#### Install

  ** Pandas is one of core requirements and it can take a few minutes to complete. **

```
pip install elastic_funnel
```

#### Add local config file

Add argument file to your home path ```~/.elastic_funnel``` with

```
[elastic]
host = 127.0.0.1
port = 9200
index = beta-backend-socketlog-*
```

#### Arguments

```
usage: elastic_funnel [-h] [--host HOST] [--port PORT] [--index INDEX]
                      --stages STAGES [STAGES ...] [--start START] [--end END]
                      [--query QUERY]

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
  --query QUERY         Additional query using syntax of Lucene, https://lucen
                        e.apache.org/core/2_9_4/queryparsersyntax.html. You
                        can narrow you search target by syntax, e.g.,
                        country:US
```

#### Run for a funnel

```
elastic_funnel --host=<elasticsearch_ip> --port=<elasticsearch_port> --stages index newTopic playgroundTopic --start 2016-03-25T00:00:00
```

#### Funnel visualization

```
Funnel: index newTopic playgroundTopic
############################################################################### 
██████████████████████████████████████████████████  27          100.0%  index          
██████████████                                       8          29.6%   newTopic        
█                                                    1          12.5%   playgroundTopic
```

### Quick Start with Gunicorn and cRUL (Developing)

To run this script, a Gunicorn server will be run on your host:

```
$ ./funnel_web.sh
```

```
curl -XPOST  -H "Content-Type: application/json" http://localhost:5578/funnel -d '
{
    "start_time": "2016-03-24T00:00:00", 
    "end_time": "2016-03-26T00:00:00"
}'
```

```
Funnel 
############################################################################### 
███████████████████████████████████████████████████  30         100.0%  index         
██████                                                4         13.3%   newTopic       
                                                      0         0.0%    playgroundTopic
```
