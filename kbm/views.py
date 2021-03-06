""" Cornice services.
"""
from cornice import Service
from cornice.resource import resource
import json
from kbm.models import Knowledge, DBSession
from sqlalchemy import text
from sqlalchemy.sql import func
import re
import json
import requests


@resource(collection_path='/kbm', path='/kbm/{id}')
class KnowledgeView(object):

    def __init__(self, request):
        self.request = request

    def collection_get(self):

        search_item = self.request.GET.get('search','')
        query_type = self.request.GET.get('type','')
        search_data = None

        if (search_item):
            """
            # Newly implemented functionality for search in title and description fields.
            Creating query string according to the search query and search the keyword
            on the index created in postgres models using tsvector
            """

            search_item = search_item.upper()
            search_words = re.split('OR|AND|NOT', search_item)
            query_string = self.generate_query_string(search_item, search_words)

            if (query_type and query_type == 'elastic'):
                return self.generate_elastic_data(search_item)
            else:
                search_data = DBSession.query(Knowledge).from_statement(text(query_string))

        else:
            # Normal GET query based on id
            search_data = DBSession.query(Knowledge).order_by(Knowledge.id)

        # Generating python dictionary from the result
        return {
            'kbm': [
                {'id': kbm.id, 'title': kbm.title, 'description': kbm.description,
                'create_at': kbm.create_at, 'create_by': kbm.create_by, 'priority': kbm.priority}

                for kbm in search_data

            ]
        }

    def generate_query_string(self, search_item, search_words):
        """
        Generate query string for search query
        """
        final_sub_query = search_item
        if len(search_words) > 1:
            for word in search_words:
                clean_word = word.replace('(','').replace(')','').replace(' ','').strip()
                print(clean_word)
                if (clean_word):
                    sub_query = """("Knowledge".description @@ plainto_tsquery('{}') OR "Knowledge".title @@ plainto_tsquery('{}'))""".format(clean_word.lower(), clean_word.lower())
                    final_word = clean_word.replace(clean_word, sub_query)
                    final_sub_query = final_sub_query.replace(clean_word, final_word)
            query_string = """SELECT * FROM "Knowledge" WHERE {};""".format(final_sub_query)
        else:
            query_string = """SELECT * FROM "Knowledge" WHERE ("Knowledge".description @@ plainto_tsquery('{}') OR "Knowledge".title @@ plainto_tsquery('{}'));""".format(final_sub_query, final_sub_query)
        return query_string

    def generate_elastic_data(self, search_item):
        """
        Generate the search data from elastic search
        """

        resp = requests.get('http://localhost:9200/kbmindex/_search?q={}'.format(search_item))
        search_data = json.loads(resp.text)

        return {
            'kbm': [
                {'id': kbm['_id'], 'title': kbm['_source']['title'], 'description': kbm['_source']['description'],
                'create_at': kbm['_source']['create_at'], 'create_by': kbm['_source']['create_by'], 'priority': kbm['_source']['priority']}

                for kbm in search_data['hits']['hits']

            ]
        }

    def get(self):
        """
        GET the data from the db and converting to json
        """
        try:
            return DBSession.query(Knowledge).get(
                int(self.request.matchdict['id'])).to_json()
        except:
            return {}

    def collection_post(self):
        """
        POST or add the data to db
        """
        kbm = self.request.json
        DBSession.add(Knowledge.from_json(kbm))

    def put(self):
        """
        PUT or update the data to db
        """
        try:
            obj=DBSession.query(Knowledge).filter(Knowledge.id==self.request.matchdict['id'])
            obj.update(self.request.json)
            return {
                'kbm': [
                    {'id': kbm.id, 'title': kbm.title, 'description': kbm.description,
                    'create_at': kbm.create_at, 'create_by': kbm.create_by, 'priority': kbm.priority}

                    for kbm in DBSession.query(Knowledge)

                ]
            }
        except:
            return {'result': 'No object found'}


    def delete(self):
        """
        DELETE the data from db based on id
        """
        obj=DBSession.query(Knowledge).filter(Knowledge.id==self.request.matchdict['id']).first()
        DBSession.delete(obj)

        return {
            'kbm': [
                {'id': kbm.id, 'title': kbm.title, 'description': kbm.description,
                'create_at': kbm.create_at, 'create_by': kbm.create_by, 'priority': kbm.priority}

                for kbm in DBSession.query(Knowledge)

            ]
        }
