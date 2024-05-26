class TestUserPhotoManagement(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            # Add a regular user
            self.user_id = self.add_user("user1", "password")
            # Add an administrator
            self.admin_id = self.add_user("admin", "password", admin=True)
            # Add photos for the users
            self.photo_id_user = self.add_photo("UserPhoto", "user1")
            self.photo_id_admin = self.add_photo("AdminPhoto", "admin")

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def add_user(self, username, password, admin=False):
        user = User(username=username, password=password, is_admin=admin)
        db.session.add(user)
        db.session.commit()
        return user.id

    def add_photo(self, name, username):
        user = User.query.filter_by(username=username).first()
        photo = Photo(name=name, caption="Test", file="test.jpg", description="Test photo", user_id=user.id)
        db.session.add(photo)
        db.session.commit()
        return photo.id

    def login(self, username, password):
        return self.client.post('/login', data=dict(username=username, password=password), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_user_can_edit_own_photo(self):
        self.login("user1", "password")
        response = self.client.post(f'/photo/{self.photo_id_user}/edit/', data={
            'user': 'user1', 'caption': 'Updated Caption', 'description': 'Updated Desc'
        })
        self.assertIn(b"Successfully Edited", response.data)
        self.logout()

    def test_user_cannot_edit_others_photo(self):
        self.login("user1", "password")
        response = self.client.post(f'/photo/{self.photo_id_admin}/edit/', data={
            'user': 'admin', 'caption': 'Malicious Update', 'description': 'Malicious Desc'
        })
        self.assertEqual(response.status_code, 403)
        self.logout()

    def test_admin_can_edit_any_photo(self):
        self.login("admin", "password")
        response = self.client.post(f'/photo/{self.photo_id_user}/edit/', data={
            'user': 'user1', 'caption': 'Admin Updated Caption', 'description': 'Admin Updated Desc'
        })
        self.assertIn(b"Successfully Edited", response.data)
        self.logout()

if __name__ == '__main__':
    unittest.main()
