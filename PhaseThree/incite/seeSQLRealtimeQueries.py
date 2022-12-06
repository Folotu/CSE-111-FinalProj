import json

def writeSQLJson2file(lst):
    filepath = 'realtimeQueries.json'
    json_str = json.dumps(lst, indent=4, sort_keys=True)
    
    with open(filepath, 'w') as f:
        f.write(json_str)