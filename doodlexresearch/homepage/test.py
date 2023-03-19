from django.test import Client, TestCase
from django.http import HttpResponse
from homepage.models import Traceroute, Discovery, Ports
import json
import asyncio

# Most of the tests I completed by manually testing each implemented tool.
# You can run this script in the terminal using following command: $python3 manage.py test

# Objects from the DB Models
db_trace = Traceroute()
db_discovery = Discovery()
db_ports = Ports()

class ViewTestCase(TestCase):

    # Testing views with POST and GET requests

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


class TestDbModels(TestCase):

    def test_write_read_traceroute(self):
        # Create a record
        db_trace.set_data('xyz.com', json.dumps(['dummy data1', 'dummy data2', 'dummy data3' ]))
        db_trace.save()

        #Read from the database
        data = db_trace.get_data()
        self.assertEqual('xyz.com', data[0][0])
    
    def test_write_read_portscanner(self):
        # Create a record
        db_ports.set_data('verycoolhost3', json.dumps(['Very coooool host has no open ports']))
        db_ports.save()
        
        #Read from the database
        data = db_ports.get_data()
        self.assertEqual('verycoolhost3', data[0][0])

    def test_write_read_hostdiscovery(self):
        # Create a record
        db_discovery.set_data('anothercoolhost', json.dumps(['data', 'data1', 'data2']))
        db_discovery.save()

        #Read from the database
        data = db_discovery.get_data()
        self.assertEqual('anothercoolhost', data[0][0])


