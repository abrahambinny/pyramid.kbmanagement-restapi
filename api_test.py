
import requests
import json

req_url = 'http://localhost:6543/kbm'

def test_api(cmd, note_id=None):

    if cmd == 'get':
        resp = requests.get(req_url)
        print(resp.text)

    elif cmd == 'post':

        resp = requests.post(req_url,
                    headers={'Content-Type': 'application/json'},
                    data=json.dumps({   "title": "python",
                                        "create_at": "2019-01-23 00:00",
                                        "create_by": "binny",
                                        "description": "python one",
                                        "priority": 3,
                                    }))
        print(resp)
    elif cmd == 'put':

        resp = requests.put('{}/{}'.format(req_url, note_id),
                    headers={'Content-Type': 'application/json'},
                    data=json.dumps({   "title": "python",
                                        "create_at": "2019-01-23 00:00",
                                        "create_by": "binny",
                                        "description": "python two",
                                        "priority": 4,
                                    }))
        print(resp)
    elif cmd == 'delete':
        resp = requests.delete('{}/{}'.format(req_url, note_id))
        print(resp)

    else:
        print("wrong input command")


if __name__ == "__main__":

    import sys
    cmd = sys.argv[1]
    note_id = None
    if len(sys.argv)>2:
        note_id = sys.argv[2]
    test_api(cmd, note_id)
