import json, requests
from pprint import pprint

from base import DbManager

API_BASE = "https://api.propublica.org/congress/v1/"
API_KEY = "CDIz4elnUMmkTmHt6rZnNpJTYBElWYbDoG1tAd4o"
DEFAULT_HEADER = {"X-API-Key":API_KEY}

class CDC():
    def __init__(self):
        self.db_Manager = DbManager()

    def get_data(self, url):
        resp = requests.get(url, headers=DEFAULT_HEADER)
        if resp.status_code!=200:
            print(resp.status_code)
            return None
        return json.loads(resp.text)

    def get_entity(self, obj, url):
        json_data= self.get_data(url)
        entity = obj()
        entity.parse_json(json_data)
        
        results = self.db_Manager.open().query(obj).filter(obj.url == url).all()
        print(results)
        if len(results)==0:
            print("===================no results")
            self.db_Manager.save(entity)
        else:
            print("should be here")

        return entity

    