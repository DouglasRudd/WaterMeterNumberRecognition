from contextlib import contextmanager
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


@contextmanager
def session_scope():
    # later, some unit of code wants to create a
    # Session that is bound to a specific Connection
    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    engine = create_engine('postgresql://postgres:ivavedran@localhost:5432/utilitymeter')
    conn = engine.connect()
    session = Session(bind=conn)
    """Provide a transactional scope around a series of operations."""
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
