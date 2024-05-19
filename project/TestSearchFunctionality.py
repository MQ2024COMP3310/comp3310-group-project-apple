class TestSearchFunctionality(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            db.session.add(Photo(name="Test", caption="Test", file="test.jpg", description="Test photo"))
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_search_sql_injection(self):
        """Test for SQL injection vulnerability in search functionality"""
        response = self.client.get('/search?query=" OR "1"="1')
        self.assertNotIn(b"Internal Server Error", response.data)

if __name__ == '__main__':
    unittest.main()
