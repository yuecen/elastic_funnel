## Elastic Funnel

This is analysis tool for funnel visualization with log from Elasticsearch. Even though we have [Kibana] to display log very well, 
it can't fit our goal to analyze series log with context for funnel. 

[Kibana]:https://www.elastic.co/products/kibana

### Constraint

* You have to add at least a field with ```state_name``` into your index

### Quick Start CLI

Install

```
pip install elastic_funnel
```

Run with a funnel

```
elastic_funnel --host=<elasticsearch_ip> --port=<elasticsearch_port> --stages user viewTopic --start 2016-03-25T00:00:00
```

Funnel visualization

```
Funnel 
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
