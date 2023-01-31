import json
from datetime import date


def get_history():
    count = 1
    with open('history.json', 'r') as f:
        json_data = json.loads(f.read())
    if json_data == []:
        data = {"date": date.today().strftime('%d-%m-%Y'), "count": 1}
        json_data.append(data)
    else:
        for day in json_data:
            if day['date'] != date.today().strftime('%d-%m-%Y'):
               json_data.remove(day)
            else:
                day['count'] += 1;
                count = day['count']
    with open('history.json', 'w') as f:
        json.dump(json_data,f)
    return "{} #{}".format(date.today().strftime('%d-%m-%Y'), count)