from django.db import models
from util.base import BaseModel
from django.contrib.postgres.fields import JSONField


class Application(BaseModel):
    """ The highest level representation of the api being tested. """
    name = models.CharField(max_length=40)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Environment(BaseModel):
    name = models.CharField(max_length=40)
    url = models.URLField()
    application = models.ForeignKey(Application)

    def __str__(self):
        return self.name


class Endpoint(BaseModel):
    name = models.CharField(max_length=40)
    path = models.CharField(max_length=100)
    application = models.ForeignKey(Application)

    def __str__(self):
        return self.name


class Payload(BaseModel):
    name = models.CharField(max_length=40)
    data = JSONField()

    def __str__(self):
        return self.name


class Call(BaseModel):
    method = models.CharField(max_length=7, choices=(
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('PATCH', 'PATCH'),
        ('DELETE', 'DELETE'),
        ('HEAD', 'HEAD'),
        ('OPTIONS', 'OPTIONS'),
    ))
    endpoint = models.ForeignKey(Endpoint)
    payload = models.ForeignKey(Payload)

    def __str__(self):
        return "{}::{}::{}".format(self.endpoint, self.method, self.payload)
