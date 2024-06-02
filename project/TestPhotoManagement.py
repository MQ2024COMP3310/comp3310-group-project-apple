import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, request, url_for, flash, redirect, render_template
from myapp import app, db
from myapp.models import Photo, User

class TestPhotoManagement(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('myapp.routes.current_user')
    @patch('myapp.routes.db.session.query')
    @patch('myapp.routes.flash')
    @patch('myapp.routes.redirect')
    @patch('myapp.routes.url_for')
    def test_edit_own_photo(self, mock_url_for, mock_redirect, mock_flash, mock_query, mock_current_user):
        # Test case for editing one's own photo
        mock_current_user.is_authenticated = True
        mock_current_user.id = 1
        mock_query.return_value.filter_by.return_value.one.return_value = Photo(user_id=1)

        with self.app as client:
            response = client.post(url_for('main.editPhoto', photo_id=1), data={
                'name': 'New Name',
                'caption': 'New Caption',
                'description': 'New Description'
            })

        mock_query.assert_called_once_with(Photo)
        mock_flash.assert_called_with('Photo Successfully Edited New Name')
        mock_redirect.assert_called_with(url_for('main.homepage'))

    @patch('myapp.routes.current_user')
    @patch('myapp.routes.db.session.query')
    @patch('myapp.routes.flash')
    @patch('myapp.routes.redirect')
    @patch('myapp.routes.url_for')
    def test_edit_other_users_photo(self, mock_url_for, mock_redirect, mock_flash, mock_query, mock_current_user):
        # Test case for trying to edit someone else's photo
        mock_current_user.is_authenticated = True
        mock_current_user.id = 1
        mock_query.return_value.filter_by.return_value.one.return_value = Photo(user_id=2)

        with self.app as client:
            response = client.post(url_for('main.editPhoto', photo_id=1), data={
                'name': 'New Name',
                'caption': 'New Caption',
                'description': 'New Description'
            })

        mock_query.assert_called_once_with(Photo)
        mock_flash.assert_called_with('You do not have permission to edit this photo.', 'error')
        mock_redirect.assert_called_with(url_for('main.homepage'))

    @patch('myapp.routes.current_user')
    @patch('myapp.routes.db.session.query')
    @patch('myapp.routes.flash')
    @patch('myapp.routes.redirect')
    @patch('myapp.routes.url_for')
    def test_delete_own_photo(self, mock_url_for, mock_redirect, mock_flash, mock_query, mock_current_user):
        # Test case for deleting one's own photo
        mock_current_user.is_authenticated = True
        mock_current_user.id = 1
        mock_query.return_value.filter_by.return_value.one.return_value = Photo(user_id=1)

        with self.app as client:
            response = client.post(url_for('main.deletePhoto', photo_id=1))

        mock_query.assert_called_once_with(Photo)
        mock_flash.assert_called_with('Photo id 1 Successfully Deleted')
        mock_redirect.assert_called_with(url_for('main.homepage'))

    @patch('myapp.routes.current_user')
    @patch('myapp.routes.db.session.query')
    @patch('myapp.routes.flash')
    @patch('myapp.routes.redirect')
    @patch('myapp.routes.url_for')
    def test_delete_other_users_photo(self, mock_url_for, mock_redirect, mock_flash, mock_query, mock_current_user):
        # Test case for trying to delete someone else's photo
        mock_current_user.is_authenticated = True
        mock_current_user.id = 1
        mock_query.return_value.filter_by.return_value.one.return_value = Photo(user_id=2)

        with self.app as client:
            response = client.post(url_for('main.deletePhoto', photo_id=1))

        mock_query.assert_called_once_with(Photo)
        mock_flash.assert_called_with('You do not have permission to delete this photo.', 'error')
        mock_redirect.assert_called_with(url_for('main.homepage'))

    @patch('myapp.routes.current_user')
    @patch('myapp.routes.db.session.query')
    @patch('myapp.routes.flash')
    @patch('myapp.routes.redirect')
    @patch('myapp.routes.url_for')
    def test_admin_edit_photo(self, mock_url_for, mock_redirect, mock_flash, mock_query, mock_current_user):
        # Test case for an admin editing any photo
        mock_current_user.is_authenticated = True
        mock_current_user.is_admin = True
        mock_query.return_value.filter_by.return_value.one.return_value = Photo(user_id=2)

        with self.app as client:
            response = client.post(url_for('main.editPhoto', photo_id=1), data={
                'name': 'Admin Edited Name',
                'caption': 'Admin Edited Caption',
                'description': 'Admin Edited Description'
            })

        mock_query.assert_called_once_with(Photo)
        mock_flash.assert_called_with('Photo Successfully Edited Admin Edited Name')
        mock_redirect.assert_called_with(url_for('main.homepage'))

    @patch('myapp.routes.current_user')
    @patch('myapp.routes.db.session.query')
    @patch('myapp.routes.flash')
    @patch('myapp.routes.redirect')
    @patch('myapp.routes.url_for')
    def test_admin_delete_photo(self, mock_url_for, mock_redirect, mock_flash, mock_query, mock_current_user):
        # Test case for an admin deleting any photo
        mock_current_user.is_authenticated = True
        mock_current_user.is_admin = True
        mock_query.return_value.filter_by.return_value.one.return_value = Photo(user_id=2)

        with self.app as client:
            response = client.post(url_for('main.deletePhoto', photo_id=1))

        mock_query.assert_called_once_with(Photo)
        mock_flash.assert_called_with('Photo id 1 Successfully Deleted')
        mock_redirect.assert_called_with(url_for('main.homepage'))

if __name__ == '__main__':
    unittest.main()
