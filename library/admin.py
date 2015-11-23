from django.http import HttpResponse
from django.contrib import admin
from library import models
import requests
import json


def execute_call(modeladmin, request, queryset):
    s = requests.Session()
    e = models.Environment.objects.get()
    response_body = ''
    for c in queryset:
        if e.url.endswith('/'):
            url = e.url[:-1]+c.endpoint.path
        else:
            url = e.url+c.endpoint.path
        response_body += "{}::{}::{}::{}\n".format(e.name, c.endpoint, c.method, c.payload)
        r = requests.Request(c.method, url, json=c.payload.data)
        resp = s.send(s.prepare_request(r))
        response_body += "status code: {}\n".format(resp.status_code)
        response_body += "call duration (ms): {}\n".format(resp.elapsed.microseconds//1000)
        response_body += "{}\n{}\n\n".format(
            json.dumps(dict(resp.headers), indent=2),
            json.dumps(resp.json(), indent=2)
        )
    return HttpResponse(response_body, content_type='text/plain')

execute_call.short_description = "Execute the selected calls"


class CallAdmin(admin.ModelAdmin):
    actions = [execute_call]


admin.site.register(models.Application)
admin.site.register(models.Environment)
admin.site.register(models.Endpoint)
admin.site.register(models.Payload)
admin.site.register(models.Call, CallAdmin)
