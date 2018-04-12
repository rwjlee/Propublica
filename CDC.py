import json, requests
from pprint import pprint

from base import DbManager
from congress_entity import Member, Congress, Committee, SubCommittee


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
        
        try:
            entity.parse_json(json_data)
        except:
            entity=None
            print("bad link: {}".format(url))
            return entity

        results = self.db_Manager.open().query(obj).filter(obj.url == url).all()
        if len(results)==0:
            self.db_Manager.save(entity)
            print("new add: {}".format(entity.url))
        else:
            print("already added: {}".format(entity.url))

        return entity

    def populate_committee(self, congress, chamber):
        
        chamber = chamber.lower()
        url = API_BASE + "{}/{}/committees.json".format(congress, chamber)

        json_data = self.get_data(url)

        try:
            results = json_data['results'][0]
        except:
            print("Bad Link")
            return "Bad Link"

        committee_list = [c['api_uri'] for c in results['committees']]
        subcommittee_list = [c['subcommittees'] for c in results['committees'] if c.get('subcommittees')]
        sc_url_list = [sc for sc in subcommittee_list if len(sc)>0]

        for sc_url in sc_url_list:
            for sc in sc_url:
                pprint(sc)
                self.get_entity(SubCommittee, sc['api_uri'])

        for com_url in committee_list:
            self.get_entity(Committee, com_url)


        return "Good Link"

    def populate_members(self, congress, chamber):
        
        chamber=chamber.lower()
        url = API_BASE + "{}/{}/members.json".format(congress, chamber)

        json_data = self.get_data(url)

        try:
            results = json_data['results'][0]
        except:
            return "Bad Link"

        member_list = [m['id'] for m in results['members']]

        for mid in member_list:
            member_url = API_BASE + "members/{}.json".format(mid)
            self.get_entity(Member, member_url)
        
        return "Good Link"

    def populate_house(self, congress):
        url = API_BASE + "{}/{}/members.json".format(congress, "house")
        self.get_entity(Congress, url)

    def populate_senate(self, congress):
        url = API_BASE + "{}/{}/members.json".format(congress, "senate")
        self.get_entity(Congress, url)