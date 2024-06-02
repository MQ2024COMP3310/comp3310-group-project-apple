import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, request, url_for, flash, redirect, render_template
from myapp import app, db
from myapp.models import Photo, User

class TestPrivatePhotos(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('myapp.routes.current_user')
    @patch('myapp.routes.db.session.query')
    @patch('myapp.routes.flash')
    @patch('myapp.routes.redirect')
    @patch('myapp.routes.url_for')
    def test_search_excludes_private_photos(self, mock_url_for, mock_redirect, mock_flash, mock_query, mock_current_user):
        # Test that private photos are not included in search results
        mock_current_user.is_authenticated = True
        public_photo = Photo(private=False)
        private_photo = Photo(private=True)
        mock_query.return_value.filter.return_value.filter.return_value.order_by.return_value.all.return_value = [public_photo]

        with self.app as client:
            response = client.get(url_for('main.search_photos', query='test'))

        mock_query.assert_called_once_with(Photo)
        self.assertNotIn(private_photo, response.data)

    @patch('myapp.routes.current_user')
    @patch('myapp.routes.db.session.query')
    @patch('myapp.routes.flash')
    @patch('myapp.routes.redirect')
    @patch('myapp.routes.url_for')
    def test_access_private_photo_via_url(self, mock_url_for, mock_redirect, mock_flash, mock_query, mock_current_user):
        # Test that a private photo can only be accessed via direct URL by its owner
        mock_current_user.is_authenticated = True
        mock_current_user.id = 1
        private_photo = Photo(user_id=1, private=True, file='private_photo.jpg')
        mock_query.return_value.filter_by.return_value.one.return_value = private_photo

        with self.app as client:
            response = client.get(url_for('main.display_file', name='private_photo.jpg'))

        self.assertEqual(response.status_code, 200)
        mock_query.assert_called_once_with(Photo)
        self.assertIn(b'private_photo.jpg', response.data)

    @patch('myapp.routes.current_user')
    @patch('myapp.routes.db.session.query')
    @patch('myapp.routes.flash')
    @patch('myapp.routes.redirect')
    @patch('myapp.routes.url_for')
    def test_access_private_photo_denied(self, mock_url_for, mock_redirect, mock_flash, mock_query, mock_current_user):
        # Test that a private photo is not accessible by users other than the owner
        mock_current_user.is_authenticated = True
        mock_current_user.id = 2
        private_photo = Photo(user_id=1, private=True, file='private_photo.jpg')
        mock_query.return_value.filter_by.return_value.one.return_value = private_photo

        with self.app as client:
            response = client.get(url_for('main.display_file', name='private_photo.jpg'))

        self.assertEqual(response.status_code, 302)
        mock_query.assert_called_once_with(Photo)
        mock_flash.assert_called_with("You do not have permission to view this photo.", "error")
        mock_redirect.assert_called_with(url_for('main.homepage'))

if __name__ == '__main__':
    unittest.main()
