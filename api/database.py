from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

def init_db(app, base):

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                           convert_unicode=True)

    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))


    base.query = db_session.query_property()

    base.metadata.create_all(bind=engine)
    return db_session
