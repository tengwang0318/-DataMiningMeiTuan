import requests
import csv
import json
import xmltodict


def xmlToJson(xml_str):
    try:
        json_dict = xmltodict.parse(xml_str, encoding='utf-8')
        json_str = json.dumps(json_dict, indent=2)
        return json_str
    except:
        pass


response = requests.get(
    "https://restapi.amap.com/v3/place/text?key=9013e06e0781b4f712e29a674d2c0d2f&type=050100&city=%E8%A5%BF%E5%AE%89&output=json").text
total_dict = json.loads(response)
for loc in total_dict['pois']:
    print(loc['location'])


