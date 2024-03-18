from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from instance.config import Config


engine = create_engine(url='mysql://root:0@db:3306/db?charset=utf8&binary_prefix=true', echo=True)
session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine)) # Mysql@localhost::3306