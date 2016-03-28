## Elastic Funnel

This is a web tool for funnel visualization with log from Elasticsearch. Even though we have [Kibana] to display log very well, 
it can't fit our goal to analyze series log with context for funnel.

[Kibana]:https://www.elastic.co/products/kibana

## Quick Start with Gunicorn and cRUL

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
