class TestPrivatePhotos(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            db.session.add(Photo(name="PrivatePhoto", caption="Private", file="private.jpg", description="Private photo", private=True))
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_private_photo_access(self):
        """Test that private photos cannot be accessed without a URL"""
        response = self.client.get('/photo/1')
        self.assertEqual(response.status_code, 403)

    def test_public_photo_access(self):
        """Test that public photos can be accessed normally"""
        response = self.client.get('/photo/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
