'''
Skripta za generiranje dimenzijskog modela podataka (Star Schema)
Case: Oprema d.d.

Ova skripta generira shemu baze podataka u zvjezdastom modelu (Star Schema).

Sadrži:
- Tablicu činjenica sa mjerama
- 5 dimenzijskih tablica (s hijerarhijama i SCD)
- Degeneriranu dimenziju u fact tablici
'''

# NEKI PODACI SU KVANTITATIVNI PO FORMATU, ALI KVALITATIVNI PO ZNAČENJU...npr. birth_year

from sqlite3 import Date
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, DateTime, ForeignKey, Float  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore
from datetime import date
from sqlalchemy import Date


# Define the database connection
engine = create_engine('mysql+pymysql://root:root@localhost:3306/zadnji', echo=True)
print("engine OK")
Session = sessionmaker(bind=engine)
session = Session()
print("Session started")
Base = declarative_base()
print("Base-done")

# ---------------------
# DIMENZIJE
# ---------------------



class DimCountry(Base):
    __tablename__ = 'dim_country'
    __table_args__ = {'schema': 'zadnji'}

    country_tk = Column(BigInteger, primary_key=True)
    country_id = Column(Integer, index=True)
    name = Column(String(100))


class DimParty(Base):
    __tablename__ = 'dim_party'
    __table_args__ = {'schema': 'zadnji'}

    party_tk = Column(BigInteger, primary_key=True)
    party_id = Column(Integer, index=True)
    name = Column(String(100))


# Hijerarhija: party → person → title
class DimPerson(Base):
    __tablename__ = 'dim_person'
    __table_args__ = {'schema': 'zadnji'}

    person_tk = Column(BigInteger, primary_key=True)
    person_id = Column(Integer, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    birth_year = Column(Integer)
    title = Column(String(50))
    party_id = Column(BigInteger, ForeignKey('zadnji.dim_party.party_tk'))



# Hijerarhija: election → date → weekday (samo godina, za jednostavnost)
class DimDate(Base):
    __tablename__ = 'dim_date'
    __table_args__ = {'schema': 'zadnji'}

    date_tk = Column(BigInteger, primary_key=True)
    full_date = Column(Date, unique=True)  # Use SQLAlchemy's Date type
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    weekday = Column(String(10))



class DimElection(Base):
    __tablename__ = 'dim_election'
    __table_args__ = {'schema': 'zadnji'}

    election_tk = Column(BigInteger, primary_key=True)
    election_id = Column(Integer, index=True)
    date_tk = Column(BigInteger, ForeignKey('zadnji.dim_date.date_tk'))
    country_id = Column(BigInteger, ForeignKey('zadnji.dim_country.country_tk'))



# izborna povijest => SADRŽI SPORO MIJENJAJUĆE DIMENZIJE (MIJENJAJU SE PROTOKOM VREMENA)
class DimElectionHistory(Base):
    __tablename__ = 'dim_election_history'
    __table_args__ = {'schema': 'zadnji'}

    election_history_tk = Column(BigInteger, primary_key=True)
    version = Column(Integer)
    date_from = Column(DateTime)
    date_to = Column(DateTime)
    election_id = Column(Integer, index=True)
    pre_blank_votes = Column(Integer)
    pre_null_votes = Column(Integer)
    historical_turnout = Column(Float)


# ---------------------
# TABLICA ČINJENICA
# ---------------------
class FactElectionResult(Base):
    __tablename__ = 'fact_election_result'
    __table_args__ = {'schema': 'zadnji'}

    fact_id = Column(BigInteger, primary_key=True)

    # Strani ključevi prema dimenzijama
    election_tk = Column(BigInteger, ForeignKey('zadnji.dim_election.election_tk'))
    party_tk = Column(BigInteger, ForeignKey('zadnji.dim_party.party_tk'))
    election_history_tk = Column(BigInteger, ForeignKey('zadnji.dim_election_history.election_history_tk'))

    # MJERE
    total_mandates = Column(Integer)
    available_mandates = Column(Integer)
    num_parishes = Column(Integer)
    num_parishes_approved = Column(Integer)
    blank_votes = Column(Integer)
    blank_votes_percentage = Column(Float)
    null_votes = Column(Integer)
    null_votes_percentage = Column(Float)
    voters_percentage = Column(Float)
    subscribed_voters = Column(Integer)
    total_voters = Column(Integer)
    mandates = Column(Integer)
    votes = Column(Integer)
    percentage = Column(Float)
    valid_votes_percentage = Column(Float)
    final_mandates = Column(Integer)
    result_type = Column(String(20))  # Degenerirana dimenzija: 'preliminary', 'official' => NAPRAVIT NA SHEMU DA JE SVAKI RESULT PRELIMINARY OSIM FINALNOG KOJI ĆE BIT OFFICIAL :)


# ---------------------
# CREATE TABLES
# ---------------------
Base.metadata.create_all(engine)
print("Dimenzijski model (Star Schema) uspješno kreiran.")
