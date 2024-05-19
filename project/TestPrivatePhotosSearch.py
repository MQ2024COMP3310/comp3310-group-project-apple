class TestPrivatePhotosSearch(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            db.session.add(Photo(name="PublicPhoto", caption="Public", file="public.jpg", description="Public photo", private=False))
            db.session.add(Photo(name="PrivatePhoto", caption="Private", file="private.jpg", description="Private photo", private=True))
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_search_excludes_private_photos(self):
        """Test that private photos are not included in search results"""
        response = self.client.get('/search?query=photo')
        self.assertNotIn(b"PrivatePhoto", response.data)
        self.assertIn(b"PublicPhoto", response.data)

if __name__ == '__main__':
    unittest.main()
