import unittest
from main import MyHTTPServer,Middleware,MyHandler
import threading

import requests


class MyFrameworkTestCase(unittest.TestCase):
    def setUp(self):
        self.server = MyHTTPServer(('localhost', 8000), MyHandler, Middleware(MyHandler))
        self.server.timeout = 0.01  # Set a low timeout for faster test execution
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server_thread.join()

    def test_home_view(self):
        response = requests.get('http://localhost:8000/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Welcome to the Home Page</h1>', response.content)

    def test_about_view(self):
        response = requests.get('http://localhost:8000/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>About Us</h1>', response.content)

    def test_contact_view(self):
        response = requests.get('http://localhost:8000/contact')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Contact Us</h1>', response.content)

    def test_submit_view(self):
        data = {'name': 'John', 'email': 'john@example.com'}
        response = requests.post('http://localhost:8000/submit', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Thank You!</h1>', response.content)


if __name__ == '__main__':
    unittest.main()