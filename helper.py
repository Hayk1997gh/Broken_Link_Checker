import json


def read_json_keys():
    with open('file.json') as json_file:
        json_data = json.load(json_file)
        json_data = dict(json_data)
        for key in list(json_data.keys()):
            if len(json_data[key]) == 0:
                json_data.pop(key)
        return dict(json_data)


def broken_links_count():
    broken_links = read_json_keys()
    count = 0
    for link in broken_links.keys():
        count += len(broken_links.get(link))
    return count
