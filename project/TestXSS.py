class TestXSS(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_xss_injection(self):
        response = self.client.post('/upload/', data={
            'user': 'Test User',
            'caption': '<script>alert(1)</script>',
            'description': 'Test Description',
            'fileToUpload': (io.BytesIO(b"dummy image data"), 'test.jpg')
        })
        self.assertNotIn(b'<script>', response.data)

if __name__ == '__main__':
    unittest.main()
