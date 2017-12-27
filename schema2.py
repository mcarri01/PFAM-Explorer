from sqlalchemy import Column, Integer, String, Table, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

'''Protein2Family = Table('Protein2Family', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('Protein_id', Integer, ForeignKey('Protein.id')),
    Column('Family_id', Integer, ForeignKey('Family.id'))
)
ProteinFamilyLocation = Table('ProteinFamilyLocation',Base.metadata,
    Column('Protein2Family_id',Integer, ForeignKey('Protein2Family.id')),
    Column('start',Integer),
    Column('end',Integer)
)'''
Protein2GO = Table('protein_go', Base.metadata,
    Column('Protein_id', Integer, ForeignKey('protein.id')),
    Column('GO_id', Integer, ForeignKey('go.id'))
)
Protein2Species = Table('Protein2Species', Base.metadata,
    Column('Protein_id', Integer, ForeignKey('protein.id')),
    Column('Species_id', Integer, ForeignKey('species.id'))
)

'''
class Protein2GO(Base):
    __tablename__ = 'protein_go'
    Protein_id = Column(Integer, ForeignKey('protein.id'),primary_key=True)
    GO_id = Column(Integer, ForeignKey('go.id'),primary_key=True)
'''

class Location(Base):
    __tablename__ = "location"
    #id = Column(Integer, primary_key=True)
    id = Column(Integer, primary_key=True,autoincrement=True)
    Protein2Family_id = Column(Integer, ForeignKey('protein_family.id'))
    start = Column(Integer)
    end = Column(Integer)
    def __repr__(self):
        return '({0},{1})'.format(self.start,self.end)
    def get(self):
        return (self.start,self.end)

class Protein2Family(Base):
    __tablename__ = "protein_family"
    #id = Column(Integer, primary_key=True)
    id = Column(Integer, primary_key=True,autoincrement=True)
    Protein_id = Column(Integer, ForeignKey('protein.id'), primary_key=True)
    Family_id = Column(Integer, ForeignKey('family.id'), primary_key=True)
    protein = relationship("Protein", back_populates="families")
    family = relationship("Family", back_populates="proteins")
    locs = relationship("Location")
    #start = Column(Integer)
    #end = Column(Integer)
    #__table_args__ = (UniqueConstraint('Protein_id', 'Family_id'),)

class Species(Base):
    __tablename__ = 'species'
    id = Column(Integer, primary_key=True,autoincrement=True)
    NCBI_id = Column(Integer,unique=True)
    name = Column(String(100),unique=True)
    proteins = relationship("Protein", secondary=Protein2Species, back_populates="species")

class Protein(Base):
    __tablename__ = 'protein'
    #id = Column(Integer, primary_key=True)
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(100),unique=True)
    sequence = Column(Text)
    species = relationship("Species", secondary=Protein2Species, back_populates="proteins")
    families = relationship("Protein2Family", back_populates="protein")
    GOterms = relationship("GO", secondary=Protein2GO, back_populates="proteins")

class Family(Base):
    __tablename__ = 'family'
    #id = Column(Integer, primary_key=True)
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(100),unique=True)
    proteins = relationship("Protein2Family", back_populates="family")
    unionsize = Column(Integer)

class GO(Base):
    __tablename__ = 'go'
    #id = Column(Integer, primary_key=True)
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(100),unique=True)
    proteins = relationship("Protein", secondary=Protein2GO, back_populates="GOterms")

#dburl = 'sqlite+pysqlite:////home/dan/research/sqlite/pfamgo.db'
dburl = 'mysql+mysqldb://dmeyer04:proteins@mysql-user.eecs.tufts.edu/pfamgo'
engine = create_engine(dburl,pool_recycle=3600)
Session =  sessionmaker(bind=engine)
session = Session()

def init():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session.commit()

def loadGO(filename):
    from GOtree import GOtree
    gt = GOtree(filename)
    dbgoterms = set([])
    for term in session.query(GO).all():
        dbgoterms.add(term.name)
    go = {}
    for term in gt.getTerms():
        if term in dbgoterms:
            continue
        session.add(GO(name=term))
    session.commit()
