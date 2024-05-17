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

    def test_sql_injection(self):
        response = self.client.post('/photo/1/delete/', data={
            'photo_id': '1 OR 1=1'
        })
        self.assertNotIn(b"Successfully Deleted", response.data)

if __name__ == '__main__':
    unittest.main()
