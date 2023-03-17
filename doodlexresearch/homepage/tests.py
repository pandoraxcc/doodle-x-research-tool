from django.test import Client, TestCase
from django.http import HttpResponse
import asyncio

# You can run this script in the terminal using following command: $python3 manage.py test

class ViewTestCase(TestCase):

    def test_get_requests_traceroute(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('index.html')

    def test_get_requests_traceroute(self):
        c = Client()
        response = c.get('/traceroute/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('traceroute.html')

    def test_get_requests_scanports(self):
        c = Client()
        response = c.get('/scanports/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('port-scan.html')

    def test_get_requests_discovery(self):
        c = Client()
        response = c.get('/discovery/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('network-discovery.html')

    def test_post_data_traceroute(self):
        c = Client()
        response = c.post('/traceroute/', {'ip': 'google.com'})
        self.assertEqual(response.status_code, 200)

    def test_post_data_scanports_closed(self):
        # You need to know which port is closed within your range
        c = Client()
        response = c.post('/scanports/', {'host': 'localhost', 'fromport': '0', 'endport': '2000'})
        self.assertContains(response, "The requested port 2000 is closed")
        self.assertEqual(response.status_code, 200)

    def test_post_data_many_scanports_closed(self):
        # You need to know which ports are closed within your range
        c = Client()
        response = c.post('/scanports/', {'host': 'localhost', 'fromport': '1', 'endport': '2000'})
        self.assertContains(response, "There are no open ports from the given range 1: 2000")
        self.assertEqual(response.status_code, 200)
        print(response)

    def test_post_data_discovery(self):
        c = Client()
        response = c.post('/discovery/', {'host': '127.0.0.1'})
        self.assertEqual(response.status_code, 200)
