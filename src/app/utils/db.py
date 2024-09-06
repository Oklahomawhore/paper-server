from sqlalchemy.orm import scoped_session, sessionmaker
from . import db

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db.engine))
