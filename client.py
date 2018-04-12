import json, requests
from pprint import pprint

from CDC import CDC
from congress_entity import Member, Congress, Committee, SubCommittee

cdc = CDC()

for i in range(110, 116):
    cdc.populate_committee(i, "senate")
    cdc.populate_committee(i, "house")
    cdc.populate_committee(i, "joint")

for i in range(80, 116):
    cdc.populate_senate(i)
    cdc.populate_members(i, "senate")

for i in range(102, 116):
    cdc.populate_house(i)
    cdc.populate_members(i, "house")