import datetime
import json

def initialize_date(current_day, interval):
    today = datetime.date.today()
    while current_day < today:
        current_day += datetime.timedelta(days=interval)
    return current_day

def read_file(file_name):
  with open(file_name, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
  return data


def add_new_item_to_dict(offense_list, praise_list):
  dict = {'offenses': offense_list, 'praises': praise_list}
  with open('data.json', 'w+', encoding='utf-8') as outfile:
    json.dump(dict, outfile)
