from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy import Column, DateTime, String, Integer, Boolean, Float, ForeignKey, func

from base import Base, inverse_relationship, create_tables

API_BASE = "https://api.propublica.org/congress/v1/"

class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)

    url = Column(String, unique=True)
    last_name = Column(String)
    first_name = Column(String)
    current_party = Column(String)
    in_office = Column(Boolean)
    most_recent_role = Column(String)
    end_date = Column(String)
    state = Column(String)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def parse_json(self, json_data):

        results = json_data['results'][0]
        self.url = API_BASE + "members/{}.json".format(results['member_id'])
        self.last_name = results['last_name']
        self.first_name = results['first_name']
        self.current_party = results['current_party']
        self.in_office = results['in_office']

        current_role=results['roles'][0]
        self.most_recent_role = current_role['chamber']
        self.end_date = current_role['end_date']
        self.state = current_role['state']

    "https://api.propublica.org/congress/v1/members/C001095.json"

class Congress(Base):
    __tablename__ = 'congresses'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)    
    congress = Column(Integer)
    chamber = Column(String)
    members = Column(String)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def parse_json(self, json_data):
        results = json_data['results'][0]
        self.congress = results['congress']
        self.chamber = results['chamber'].lower()
        self.url = API_BASE + "{}/{}/members.json".format(self.congress, self.chamber)

        member_list=[m['id'] for m in results['members']]
        self.members = " | ".join(member_list)

class Committee(Base):
    __tablename__ = 'committees'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    name = Column(String)
    chair = Column(String)
    chamber = Column(String)
    congress = Column(Integer)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def parse_json(self, json_data):
        results = json_data['results'][0]
        self.name = results['name']
        self.chair = results['chair']
        self.chamber = results['chamber'].lower()
        self.congress = results['congress']
        self.url = API_BASE + "{}/{}/committees/{}.json".format(self.congress, self.chamber, results['id'])

class SubCommittee(Base):
    __tablename__ = 'subcommittees'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    name = Column(String)
    chair = Column(String)
    chamber = Column(String)
    congress = Column(Integer)
    committee_id = Column(String)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def parse_json(self, json_data):
        results = json_data['results'][0]
        self.name = results['name']
        self.chair = results['chair']
        self.chamber = results['chamber'].lower()
        self.congress = results['congress']
        self.committee_id = results['committee_id']
        self.url = API_BASE + "{}/{}/committees/{}/subcommittees/{}.json".format(self.congress, self.chamber, self.committee_id, results['id'])


if __name__ != '__main__':
    create_tables()