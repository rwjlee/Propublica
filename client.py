import json, requests
from pprint import pprint

from CDC import CDC
from congress_entity import Member, Congress, Committee, SubCommittee

# entity_tuple = [(Member, "http://data.coding.kitchen/api/companies/1"), 
#     (Club, "http://data.coding.kitchen/api/clubs/1"),
#     (Person, "http://data.coding.kitchen/api/people/1"),
#     (League, "http://data.coding.kitchen/api/leagues/"),
#     (City, "http://data.coding.kitchen/api/cities/1"),
#     (Department, "http://data.coding.kitchen/api/departments/1"),
#     (State,"http://data.coding.kitchen/api/states/"),
#     (Exchange, "http://data.coding.kitchen/api/exchanges/")]

# for value in entity_tuple:
#     obj, next_url = value
#     dck.populate_table(obj, next_url)

API_BASE = "https://api.propublica.org/congress/v1/"

def get_senate(chamber):
    if 80 <= chamber and chamber <= 115:
        return get_data(API_BASE + ENDPOINT_SENATE.format(chamber)) 
    else:
        return None

def get_house(chamber):
    if 102 <= chamber and chamber <= 115:
        return get_data(API_BASE + ENDPOINT_HOUSE.format(chamber))
    else:
        return None

def get_members(chamber, branch):
    pass




# senate=get_senate(115)
# print(len(senate['results']))

cdc = CDC()

# senator_url="https://api.propublica.org/congress/v1/members/C001095.json"
# cdc.get_entity(Member, senator_url)

# subcommittee_url = "https://api.propublica.org/congress/v1/115/senate/committees/SSAS/subcommittees/SSAS13.json"
# cdc.get_entity(SubCommittee, subcommittee_url)

#committee_url = "https://api.propublica.org/congress/v1/115/senate/committees/SSAS.json"
#cdc.get_entity(Committee, committee_url)

# senate_url = "https://api.propublica.org/congress/v1/115/senate/members.json"
# cdc.get_entity(Congress, senate_url)

results=cdc.get_data("https://api.propublica.org/congress/v1/115/joint/committees.json")

pprint(results)