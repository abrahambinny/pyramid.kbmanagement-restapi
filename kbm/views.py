""" Cornice services.
"""
from cornice import Service
from cornice.resource import resource
import json
from kbm.models import Knowledge, DBSession


@resource(collection_path='/kbm', path='/kbm/{id}')
class KnowledgeView(object):

    def __init__(self, request):
        self.request = request

    def collection_get(self):

        return {
            'kbm': [
                {'id': kbm.id, 'title': kbm.title, 'description': kbm.description,
                'create_at': kbm.create_at, 'create_by': kbm.create_by, 'priority': kbm.priority}

                    for kbm in DBSession.query(Knowledge).order_by(Knowledge.id)

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
