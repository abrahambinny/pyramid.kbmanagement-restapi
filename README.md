
## REST API using Python, Pyramid, SqlAlchemy, Postgres

### Prerequisites
```
sudo apt-get install postgresql
sudo apt-get install python-psycopg2
sudo apt-get install libpq-dev
```

### Login to psql
```
psql -d kbmdb -U  binny -w
Password:
psql> CREATE DATABASE kbmdb OWNER binny;
psql> GRANT ALL PRIVILEGES ON DATABASE kbmdb TO binny;
psql> GRANT CONNECT ON DATABASE kbmdb TO binny;

```

### Project Installation
```
cd kbmanagement/
export VENV=~/workspace/personal/pyramid_projects/kbmanagement/env
python3 -m venv $VENV
$VENV/bin/pip install --upgrade pip setuptools
$VENV/bin/pip install "pyramid==1.10.4" waitress
$VENV/bin/pip install -r requirements.txt
$VENV/bin/python setup.py develop
$VENV/bin/pip install psycopg2 --upgrade
$VENV/bin/initialize_kbm_db kbm.ini
```

### Run the server
```
$VENV/bin/pserve kbm.ini --reload
```

### Unit testing
```
$VENV/bin/pytest kbm/tests.py -q
```

### REST API Testing

### Run below scripts for GET, POST, PUT, DELETE
```
$VENV/bin/python api_test.py get
$VENV/bin/python api_test.py post
$VENV/bin/python api_test.py put 1
$VENV/bin/python api_test.py post
$VENV/bin/python api_test.py put 2
$VENV/bin/python api_test.py delete 2

```

### OR

### Send requests through python shell or postman

```
import requests
```

### GET operation
```
requests.get('http://localhost:6543/kbm')
```

### POST operation
```
requests.post(
  'http://localhost:6543/kbm',
  headers={'Content-Type': 'application/json'},
  data=json.dumps({   "title": "python",
                      "create_at": "2019-01-23 00:00",
                      "create_by": "binny",
                      "description": "python one",
                      "priority": 3,
                  }))
```

### PUT operation
```
requests.put(
  'http://localhost:6543/kbm/1',
  headers={'Content-Type': 'application/json'},
  data=json.dumps({   "title": "python",
                      "create_at": "2019-01-23 00:00",
                      "create_by": "binny",
                      "description": "python two",
                      "priority": 4,
                  }))
```

### DELETE operation
```
requests.delete('http://localhost:6543/kbm/1')
```
