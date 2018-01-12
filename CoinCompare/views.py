from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from django.views import View
import requests
import json

class HomePage(TemplateView):
    template_name = "index.html"


#next is convert numbers into readable stuff
def index(request):

    url = "https://api.coinmarketcap.com/v1/ticker/?convert=AUD&limit=10"
    respo =  requests.get(url)
    print (respo)
    data = json.loads(respo.content.decode('utf-8'))

    with open('JSONdata.JSON', 'w') as f:
        json.dump(data, f, ensure_ascii=False)
    f.close()
    datalist = []
    '''
    for i in data:
        datalist.append(i["name"])
        datalist.append(i["symbol"])
        datalist.append("_______________")
    '''
    context = {'data': data}
    return render(request, 'index.html', context)


def view_All(request):
    pass




