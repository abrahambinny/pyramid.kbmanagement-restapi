
## Implemented search query language search using NOT, AND, OR using elasticsearch and pyramid

### Prerequisites
### Install Java & configure
```
sudo apt install openjdk-11-jdk
java -version
echo $JAVA_HOME
```

### Install elasticsearch
```
sudo apt-get install apt-transport-https
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
add-apt-repository "deb https://artifacts.elastic.co/packages/7.x/apt stable main"
sudo apt-get update
sudo apt-get install elasticsearch
```

### Configure elasticsearch
```
sudo nano /etc/elasticsearch/elasticsearch.yml
# change the following values
network.host: 0.0.0.0
cluster.name: myCluster1
node.name: "myNode1"
```

### Launch elasticsearch
```
sudo /bin/systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service
OR
sudo service elasticsearch start
```

### Test Setup
```
curl -X GET "http://localhost:9200/?pretty"
{
  "name" : "mynode1",
  "cluster_name" : "mycluster1",
  "cluster_uuid" : "bhPkp16FSnWpg4U0e6L-OQ",
  "version" : {
    "number" : "7.5.2",
    "build_flavor" : "default",
    "build_type" : "deb",
    "build_hash" : "8bec50e1e0ad29dad5653712cf3bb580cd1afcdf",
    "build_date" : "2020-01-15T12:11:52.313576Z",
    "build_snapshot" : false,
    "lucene_version" : "8.3.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

### Indexing the data
```
curl -X PUT 'localhost:9200/kbmindex' -H 'Content-Type: application/json' -d' {"settings" : {"number_of_shards" : 3, "number_of_replicas" : 2 }, "mappings" : {"properties"
 : {"title" : { "type" : "text" }, "description" : { "type" : "text" }, "create_by" : { "type" : "text" }, "priority" : { "type" : "integer" }}}}'
```

### Mapping the data with fields in database
```
 curl -H "Content-Type: application/json" -X POST "http://localhost:9200/kbmindex/_doc/_bulk?pretty" --data-binary "@kbm_data.json"
 ```

### Testing the backend data using special query, elasticsearch and curl
```
curl -H "Content-Type: application/json" -X GET "http://localhost:9200/kbmindex/_search?q=(facebook OR microsoft) AND NOT (python)"
curl -H "Content-Type: application/json" -X GET "http://localhost:9200/kbmindex/_search?q=(facebook AND microsoft) AND NOT (python)"
curl -H "Content-Type: application/json" -X GET "http://localhost:9200/kbmindex/_search?q=(facebook OR microsoft)"
curl -H "Content-Type: application/json" -X GET "http://localhost:9200/kbmindex/_search?q=python"

```

### SEARCH operation using elasticsearch and pyramid
```
requests.get('http://localhost:6543/kbm?search=(facebook OR microsoft) AND NOT (python)&type=elastic')
requests.get('http://localhost:6543/kbm?search=(facebook AND microsoft) AND NOT (python)&type=elastic'')
requests.get('http://localhost:6543/kbm?search=(facebook OR microsoft)&type=elastic'')
requests.get('http://localhost:6543/kbm?search=python&type=elastic'')
```
