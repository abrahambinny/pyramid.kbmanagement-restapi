""" Cornice services.
"""
from cornice import Service
from cornice.resource import resource
import json
from kbm.models import Knowledge, DBSession
from sqlalchemy import text
from sqlalchemy.sql import func


@resource(collection_path='/kbm', path='/kbm/{id}')
class KnowledgeView(object):

    def __init__(self, request):
        self.request = request

    def collection_get(self):

        search_item = self.request.GET['search']
        search_data = None

        if (search_item):
            print(search_item)
            search_data = DBSession.query(Knowledge).from_statement(text("""SELECT * FROM "Knowledge" WHERE ("Knowledge".description @@ plainto_tsquery('python') AND "Knowledge".title @@ plainto_tsquery('python')) OR ("Knowledge".description @@ plainto_tsquery('microsoft') AND "Knowledge".title @@ plainto_tsquery('microsoft')) AND NOT ("Knowledge".description @@ plainto_tsquery('facebook') AND "Knowledge".title @@ plainto_tsquery('facebook'));"""))
            # search_data = DBSession.query(Knowledge).filter(
            #     Knowledge.title.op('@@')(func.plainto_tsquery(search_item)),
            #     Knowledge.description.op('@@')(func.plainto_tsquery(search_item))
            # )
        else:
            search_data = DBSession.query(Knowledge).order_by(Knowledge.id)

        return {
            'kbm': [
                {'id': kbm.id, 'title': kbm.title, 'description': kbm.description,
                'create_at': kbm.create_at, 'create_by': kbm.create_by, 'priority': kbm.priority}

                    for kbm in search_data

                    ]
            }

    def get(self):

        try:
            return DBSession.query(Knowledge).get(
                int(self.request.matchdict['id'])).to_json()
        except:
            return {}

    def collection_post(self):

        kbm = self.request.json
        DBSession.add(Knowledge.from_json(kbm))

    def put(self):
        try:
            obj=DBSession.query(Knowledge).filter(Knowledge.id==self.request.matchdict['id'])
            obj.update(self.request.json)
            return {'kbm': [
                    {'id': kbm.id, 'title': kbm.title, 'description': kbm.description,
                    'create_at': kbm.create_at, 'create_by': kbm.create_by, 'priority': kbm.priority}

                        for kbm in DBSession.query(Knowledge)

                        ]
                    }
        except:
            return {'result': 'No object found'}


    def delete(self):
        obj=DBSession.query(Knowledge).filter(Knowledge.id==self.request.matchdict['id']).first()
        DBSession.delete(obj)

        return {'kbm': [
                {'id': kbm.id, 'title': kbm.title, 'description': kbm.description,
                'create_at': kbm.create_at, 'create_by': kbm.create_by, 'priority': kbm.priority}

                    for kbm in DBSession.query(Knowledge)

                    ]
                }

    # @view_config(route_name='hello_json', renderer='json')
    # def hello(self):
    #     return {'name': 'Hello View'}
