# Task 9 Part B

import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, request, url_for, flash, redirect, render_template
from myapp import app, db
from myapp.models import Photo
from project.main import search_photos

class TestSearchPhotos(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('myapp.routes.request')
    @patch('myapp.routes.flash')
    @patch('myapp.routes.redirect')
    @patch('myapp.routes.url_for')
    def test_no_query(self, mock_url_for, mock_redirect, mock_flash, mock_request):
        # Test case where no query is provided
        mock_request.args.get.return_value = None
        mock_url_for.return_value = '/'

        response = search_photos()

        mock_flash.assert_called_with("Please enter a search term.", "error")
        mock_redirect.assert_called_with(url_for('main.homepage'))
        self.assertEqual(response, mock_redirect.return_value)

    @patch('myapp.routes.request')
    @patch('myapp.routes.db.session.query')
    def test_sql_injection(self, mock_query, mock_request):
        # Test case to ensure SQL injection is not possible
        mock_request.args.get.return_value = "test'; DROP TABLE photos; --"
        mock_query.return_value.filter.return_value.order_by.return_value.all.return_value = []

        response = search_photos()

        # Ensure that the query method was called with a safe, parameterized query
        search = "%test'; DROP TABLE photos; --%"
        mock_query.assert_called_once_with(Photo)
        mock_query.return_value.filter.assert_called_once()
        called_args, _ = mock_query.return_value.filter.call_args
        self.assertTrue(any(search in str(arg) for arg in called_args))
    
    @patch('myapp.routes.request')
    @patch('myapp.routes.db.session.query')
    @patch('myapp.routes.render_template')
    def test_valid_query(self, mock_render_template, mock_query, mock_request):
        # Test case where a valid query is provided
        mock_request.args.get.return_value = "sunset"
        mock_query.return_value.filter.return_value.order_by.return_value.all.return_value = ["photo1", "photo2"]

        response = search_photos()

        mock_query.assert_called_once_with(Photo)
        search = "%sunset%"
        mock_query.return_value.filter.assert_called_once()
        called_args, _ = mock_query.return_value.filter.call_args
        self.assertTrue(any(search in str(arg) for arg in called_args))
        mock_render_template.assert_called_with('index.html', photos=["photo1", "photo2"])

if __name__ == '__main__':
    unittest.main()
