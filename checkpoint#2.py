import pandas as pd
import numpy as np
import json
import requests
import random
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

CSV_FILE_PATH = "C:/Users/Korisnik/Downloads/ElectionData_PROCESSED.csv"
df = pd.read_csv(CSV_FILE_PATH, delimiter=',')
print("CSV size: ", df.shape)
print(df.head())

Base = declarative_base()
print("start")
class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

class Election(Base):
    __tablename__ = 'election'
    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(DateTime, nullable=False)
    total_mandates = Column(Integer, nullable=False)
    available_mandates = Column(Integer, nullable=False)
    num_parishes = Column(Integer, nullable=False)
    num_parishes_approved = Column(Integer, nullable=False)
    blank_votes = Column(Integer, nullable=False)
    blank_votes_percentage = Column(Float, nullable=False)
    null_votes = Column(Integer, nullable=False)
    null_votes_percentage = Column(Float, nullable=False)
    voters_percentage = Column(Float, nullable=False)
    subscribed_voters = Column(Integer, nullable=False)
    total_voters = Column(Integer, nullable=False)
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship('Country')

class Party(Base):
    __tablename__ = 'party'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

class Result(Base):
    __tablename__ = 'result'
    id = Column(Integer, primary_key=True, autoincrement=True)
    election_id = Column(Integer, ForeignKey('election.id'))
    party_id = Column(Integer, ForeignKey('party.id'))
    mandates = Column(Integer, nullable=False)
    percentage = Column(Float, nullable=False)
    valid_votes_percentage = Column(Float, nullable=False)
    votes = Column(Integer, nullable=False)
    final_mandates = Column(Integer, nullable=False)

    election = relationship('Election')
    party = relationship('Party')

class ElectionHistory(Base):
    __tablename__ = 'election_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    election_id = Column(Integer, ForeignKey('election.id'))
    pre_blank_votes = Column(Integer, nullable=False)
    pre_null_votes = Column(Integer, nullable=False)
    historical_turnout = Column(Float, nullable=False)

    election = relationship('Election')

print("Starting database setup...")
engine = create_engine('mysql+pymysql://root:root@localhost:3306/elections_brazil', echo=False)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
print("Database schema created successfully")

df = pd.read_csv(CSV_FILE_PATH)
print("df defined")
Session = sessionmaker(bind=engine)
session = Session()

countries = {name: Country(name=name) for name in df['territoryName'].unique()}
session.add_all(countries.values())
session.commit()
print("commit1 ok")
parties = {name: Party(name=name) for name in df['Party'].unique()}
session.add_all(parties.values())
session.commit()
print("commit2 ok")
for _, row in df.iterrows():
    country = countries[row['territoryName']]
    election = Election(
        year=row['time'],
        total_mandates=row['totalMandates'],
        available_mandates=row['availableMandates'],
        num_parishes=row['numParishes'],
        num_parishes_approved=row['numParishesApproved'],
        blank_votes=row['blankVotes'],
        blank_votes_percentage=row['blankVotesPercentage'],
        null_votes=row['nullVotes'],
        null_votes_percentage=row['nullVotesPercentage'],
        voters_percentage=row['votersPercentage'],
        subscribed_voters=row['subscribedVoters'],
        total_voters=row['totalVoters'],
        country=country
    )
    session.add(election)
    session.commit()

    history = ElectionHistory(
        election_id=election.id,
        pre_blank_votes=row.get('preBlankVotes', 0),
        pre_null_votes=row.get('preNullVotes', 0),
        historical_turnout=row.get('historicalTurnout', 0.0)
    )
    session.add(history)

    party = parties[row['Party']]
    result = Result(
        election_id=election.id,
        party_id=party.id,
        mandates=row['Mandates'],
        percentage=row['Percentage'],
        valid_votes_percentage=row['validVotesPercentage'],
        votes=row['Votes'],
        final_mandates=row['FinalMandates']
    )
    session.add(result)
    print("add done")
session.commit()
print("commit3 ok")
session.close()

print("Data successfully loaded into the database!")

