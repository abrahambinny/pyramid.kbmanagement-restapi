import unittest
import transaction

from pyramid import testing


def _initTestingDB():
    from sqlalchemy import create_engine
    from .models import (
        DBSession,
        Knowledge,
        Base
        )
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    with transaction.manager:
        model = Knowledge(
            title='Postgres',
            description='This is the postgres page',
            create_at="2017-08-23 00:00",
            create_by="binny",
            priority=3
        )
        DBSession.add(model)
    return DBSession


class KnowledgeViewTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def test_wiki_view(self):
        from kbm.views import KnowledgeView

        request = testing.DummyRequest()
        inst = KnowledgeView(request)
        response = inst.collection_get()
        self.assertEqual(response['kbm'][0]['title'], 'Postgres')


class KnowledgeFunctionalTests(unittest.TestCase):
    def setUp(self):
        from pyramid.paster import get_app
        app = get_app('kbm.ini')
        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        from .models import DBSession
        DBSession.remove()

    def test_it(self):
        res = self.testapp.get('/kbm', status=200)
        print(res.body)
        if(res.body):
            self.assertIn(b'python', res.body)
