from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

engine = create_engine('sqlite:///search_history.db', echo = True)
meta = MetaData()

search_history = Table(
   'search_history', meta, 
   Column('id', Integer, primary_key = True), 
   Column('user', String), 
   Column('search_key', String),
)
meta.create_all(engine)