from django.db import models
import json

class Ports(models.Model):
    host = models.CharField(max_length=255)
    data = models.JSONField()
    date = models.DateTimeField(auto_now_add=True)

    def set_data(self, host, data):
        self.host = json.dumps(host)
        self.data = data

    def get_data(self):
        queries = Ports.objects.all()
        dataset = [[json.loads(query.host), json.loads(query.data), query.date] for query in queries ]

        return dataset


class Traceroute(models.Model):
    domain = models.CharField(max_length=255)
    data = models.JSONField()
    date = models.DateTimeField(auto_now_add=True)

    def set_data(self, domain, data):
        self.domain = json.dumps(domain)
        self.data = data

    def get_data(self):
        queries = Traceroute.objects.all()
        dataset = [[json.loads(query.domain), json.loads(query.data), query.date] for query in queries ]

        return dataset


class Discovery(models.Model):
    host = models.CharField(max_length=255)
    data = models.JSONField()
    date = models.DateTimeField(auto_now_add=True)

    def set_data(self, host, data):
        self.host = json.dumps(host)
        self.data = data

    def get_data(self):
        queries = Discovery.objects.all()
        dataset = [[json.loads(query.host), json.loads(query.data), query.date] for query in queries ]

        return dataset
