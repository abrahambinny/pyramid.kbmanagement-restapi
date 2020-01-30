# kbm/models.py

from pyramid.security import Allow, Everyone
from sqlalchemy import Column, Integer, String, Index, Text, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import func
# from zope.sqlalchemy import ZopeTransactionExtension

from zope.sqlalchemy import register
DBSession = scoped_session(sessionmaker())
register(DBSession)
Base = declarative_base()

def to_tsvector_ix(*columns):
    s = " || ' ' || ".join(columns)
    return func.to_tsvector('english', text(s))


class Knowledge(Base):
    __tablename__ = 'Knowledge'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    description = Column(Text)
    create_at = Column(Text)
    create_by = Column(Text)
    priority = Column(Integer)

    __table_args__ = (
        Index(
            'ix_knowledge_tsv',
            to_tsvector_ix('title', 'description'),
            postgresql_using='gin'
        ),
    )

    def __init__(self, title, description, create_at ,create_by, priority):
        self.title = title
        self.description = description
        self.create_at = create_at
        self.create_by = create_by
        self.priority = priority

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self):
        to_serialize = ['id', 'title', 'description', 'create_at', 'create_by', 'priority']
        d = {}
        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)
        return d

class Root(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'group:editors', 'edit')]

    def __init__(self, request):
        pass
