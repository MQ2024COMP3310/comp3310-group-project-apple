# Task 3 Part D

import unittest
from project import create_app, db
from project.models import Photo
from flask import url_for

class TestSQLInjection(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            db.session.add(Photo(name="Test", caption="Test", file="test.jpg"))
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_sql_injection_delete(self):
        response = self.client.post('/photo/1/delete/', data={'photo_id': '1 OR 1=1'})
        self.assertNotIn(b"Successfully Deleted", response.data)

    def test_sql_injection_edit(self):
        # Test edit endpoint
        response = self.client.post('/photo/1/edit/', data={
            'user': 'Test User',
            'caption': 'Caption',
            'description': 'Desc',
            'photo_id': '1 OR 1=1'
        })
        self.assertNotIn(b"Successfully Edited", response.data)

    def test_sql_injection_upload(self):
        # Test upload endpoint
        with self.app.app_context():
            response = self.client.post('/upload/', data={
                'user': 'InjectedUser', 
                'caption': 'InjectedCaption', 
                'description': 'InjectedDesc',
                'fileToUpload': (open('test.jpg', 'rb'), 'test.jpg')
            })
            self.assertNotIn(b"Successfully Created", response.data)

    def test_sql_injection_select(self):
        # Test for injection in select queries
        with self.app.app_context():
            response = self.client.get('/?sort="; DROP TABLE photo;--')
            self.assertNotIn(b"Internal Server Error", response.data)

if __name__ == '__main__':
    unittest.main()
